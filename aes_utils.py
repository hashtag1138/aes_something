from Crypto import Random
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from constants import ConstantSize as size
def rndIv():
	return Random.new().read(AES.block_size)
	#Return bytes()

def rndSalt():
	return Random.new().read(8)
	#Return bytes()
	
def rndKey(salt= None, password=None):
	salt = rndSalt() if not salt else salt
	password = Random.new().read(16) if not password else password
	return KDF.PBKDF1(password, salt, 32, 10000, SHA512)
	#Return bytes()
	
def getHash(txt):
	h = SHA512.new()
	h.update(txt) # bytes expected
	return h.digest()
	#Return bytes()

def addHash(txt):
	return getHash(txt) + txt

def removeHash(txt):
	hs = size().HASH
	hash_given = txt[:hs]
	return txt[hs:] if hash_given == getHash(txt[hs:]) else False

def enlarge255(filename):
	fns = size().FILENAME
	padding = "".join([chr(0)] * (fns - len(filename) - 1)).encode()
	return chr(len(filename)).encode() + filename.encode() + padding

def aesEncrypt(iv, key, txt):
	return AES.new(key, AES.MODE_CFB, iv).encrypt(addHash(txt))

def aesDecrypt(iv, key, xtx):
	return removeHash(AES.new(key, AES.MODE_CFB, iv).decrypt(xtx))
	
def packMeta(filename, iv, key, start_f, end_f):
	start_f = ('%0*x'%(17,start_f)).encode()
	end_f = ('%0*x'%(17,end_f)).encode()
	filename = enlarge255(filename)
	return filename + iv + key + start_f + end_f

def depackMeta(meta):
	iv_s = size().IV
	k_s = size().AESKEY
	fn_s = size().FILENAME
	s_s = size().FILE_START_OFFSET
	e_s = size().FILE_END_OFFSET
	filenamelen = meta[0]
	filename = meta[1:meta[0] + 1 ]
	iv = meta[fn_s: fn_s + iv_s ]
	key = meta[fn_s + iv_s : fn_s + iv_s + k_s ]
	start_f = meta[fn_s + iv_s + k_s: fn_s + iv_s + k_s + s_s]
	end_f = meta[ fn_s + iv_s + k_s + s_s:  fn_s + iv_s + k_s + s_s + e_s]
	return  (filename, iv, key, start_f , end_f)
