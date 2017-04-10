from Crypto.Cipher import AES, Blowfish
from Crypto.Protocol import KDF
from Crypto import Random
from Crypto.Random import random
from Crypto.Hash import SHA512
from string import printable, hexdigits
from base64 import b64encode, b64decode
class AesCipher(object):
	"""
		Encrypt/Decrypt files using AES256/192/128 with hash based integrity check.
		It can export in base64 printable mode, overwrite source file and wipe password 
		memory location.
		Usage:
			cipher = AesCipher(password='', aes_key_lenght=256, base64_inout=True, derivation_round=1000)
			cipher.encryptFile(input_filename, output_filename, overwrite= False)
				if overwrite=True so the output file will be the same as the input file
			cipher.decryptFile(input_filename, output_filename, check=True, overwrite= False)
				if check=False then messages finger print comparaison will be passed. if the
				encrypted text has been modified the unencrypted message will make non sense.
			cipher.wipe(pranoiac=False, round1=100)
				this method will pass self.password to keyderivation function and then store the
				resulte in self.password and the redo again and again.
	"""
	def __init__(self, password='' , aes_key_lenght=256, base64_inout=True, derivation_round=1000):
		self.password = password if isinstance(password, str) else ''
		self.aes_key_lenght = aes_key_lenght if aes_key_lenght == 128 else 256
		self.base64_inout = base64_inout if isinstance(base64_inout, bool) else True
		if isinstance(derivation_round, int) and derivation_round > 0:
			self.derivation_round = derivation_round
		else:
			self.derivation_round = 1000
		 
	def encryptFile(self, input_filename, output_filename, check=True, overwrite= False):
		output_filename = input_filename if overwrite else output_filename
		(clear_text, hash) = self.readUnEncrypted(input_filename)
		(aes_key, aes_key_salt) = self.keyDerivation(self.password, 
						derivation_round=self.derivation_round, 
						aes_key_lenght=self.aes_key_lenght)
		(encrypted_text, init_vector) = self.encrypt(clear_text, hash
																,aes_key, check)
		succes = self.writeEncrypted(output_filename, aes_key_salt,
						init_vector, encrypted_text, self.base64_inout)
		if succes:
			return True
		else:
			return False
						
	def decryptFile(self, input_filename, output_filename, check=True, overwrite= False):
		output_filename = input_filename if overwrite else output_filename
		(aes_key_salt, init_vector, encrypted_text) = self.readEncrypted(
										input_filename,self.base64_inout)
		(aes_key, _) = self.keyDerivation(self.password, 
						derivation_round=self.derivation_round, 
						aes_key_lenght=self.aes_key_lenght, aes_key_salt = aes_key_salt)
		(unencrypted_text) = self.decrypt(encrypted_text, aes_key, 
															init_vector)
		(unencrypted_text) = self.removeHeader(unencrypted_text, check)
		succes =  self.writeUnEncrypted(output_filename, unencrypted_text)
		if succes:
			return True
		else:
			return False
		
	def wipe(self, paranoiac=False, round1=100):
		if paranoiac :
			round1 = 1000
			round2 = 1000
		else:
			round2=10
		for i in range(round1):
			#print('.'*(i%100), end='\r')
			(self.password, _) = self.keyDerivation(self.password, derivation_round=round2)
			
	def readUnEncrypted(self, input_filename):
		with open(input_filename, 'rb') as f:
			clear_text = f.read()
			h = SHA512.new()
			h.update(clear_text)
			hash = h.digest()
			return (clear_text, hash ) # Hash + txt
		return False
		
	def readEncrypted(self, input_filename, base64_inout):
		with open(input_filename, 'rb') as f:
			if base64_inout: encrypted_text = b64decode(f.read())
			else: encrypted_text = f.read()
			aes_key_salt = encrypted_text[:8]
			init_vector = encrypted_text[8:8+16]
			encrypted_text = encrypted_text[8+16:]
			return (aes_key_salt, init_vector, encrypted_text)
		return False
		
	def removeHeader(self, unencrypted_text, check):
		if not check:
			header_size = 3
			try:
				padding_lenght = int(unencrypted_text[:3],0)
			except:
				padding_lenght = 0
			return unencrypted_text[header_size:len(unencrypted_text)-padding_lenght]	
		padding_lenght = int(unencrypted_text[:3],0)
		hash_in_file = unencrypted_text[3:64+3]	
		h = SHA512.new()
		header_size = 3+64
		h.update(unencrypted_text[header_size:len(unencrypted_text)-padding_lenght])
		if  hash_in_file == h.digest():
			return unencrypted_text[header_size:len(unencrypted_text)-padding_lenght]
		else: 
			return False	
			
	def writeUnEncrypted(self, output_filename, unencrypted_text):
		with open(output_filename, 'wb') as f:
			f.write(unencrypted_text)
			return True
		return False	
		
	def writeEncrypted(self, output_filename, aes_key_salt, 
						init_vector, encrypted_text, base64_inout):
		with open(output_filename, 'wb') as f:
			output = bytes(aes_key_salt) + bytes(init_vector) + encrypted_text
			if base64_inout : f.write(b64encode(output))
			else: f.write(output)
			return True
		return False
		
	def keyDerivation(self, password, aes_key_salt=None, derivation_round=1000, aes_key_lenght=256):
		if not aes_key_salt : 
			random_string = [printable[random.randint(0,len(printable)-1)] for _ in range(8)]
			aes_key_salt = "".join(random_string).encode()
		return (KDF.PBKDF2(password, aes_key_salt, count=derivation_round,
				dkLen=int(aes_key_lenght/8), prf=None), aes_key_salt)
				
	def encrypt(self, unencrypted_text, hash, aes_key, check):
		init_vector = Random.new().read(AES.block_size)
		aes_cipher = AES.new(aes_key, AES.MODE_CFB, init_vector)
		padding = bytes("".join(['.']*((len(unencrypted_text)+1)%16)).encode())
		if check:
			encrypted_text = aes_cipher.encrypt(bytes(hex(len(padding)).encode())+ hash + unencrypted_text + padding)
		else:
			encrypted_text = aes_cipher.encrypt(bytes(hex(len(padding)).encode()) + unencrypted_text + padding)
		return (encrypted_text, init_vector)
		
	def decrypt(self, encrypted_text, aes_key, init_vector):
		aes_cipher = AES.new(aes_key, AES.MODE_CFB, init_vector)
		unencrypted_text = aes_cipher.decrypt(encrypted_text)
		return unencrypted_text
		
def testAesCipher():
	txt = 'Ceci est un texte de test.'
	with open('test.txt', 'w') as f:
		f.write(txt)
	a = AesCipher(password='password',base64_inout=True ,aes_key_lenght=256)
	ret1 = a.encryptFile('test.txt', 'test.txt_aes256.b64encrypted')
	ret2 = a.decryptFile('test.txt_aes256.b64encrypted','test.txt_aes256.b64decrypted', check=True)
	
	
	a = AesCipher(password='m', aes_key_lenght=256, base64_inout=True)
	ret5 = a.encryptFile('test.txt', 'test.txt_aes256_nocheck.b64encrypted', check=False)
	a = AesCipher(password='m', aes_key_lenght=256, base64_inout=True)
	ret6 = a.decryptFile('test.txt_aes256_nocheck.b64encrypted','test.txt_aes256_b64nocheck.decrypted', check=False)

	if ret1 : print('Chiffrement AES256_base64 réussi')
	if ret2 : print('Déchiffrement AES256_base64 réussi')
	
	if ret5 : print('Chiffrement AES256_base64 réussi')
	if ret6 : print('Déchiffrement AES256_base64 réussi')

	print(a.password)
	
if __name__ == "__main__":
	testAesCipher()
