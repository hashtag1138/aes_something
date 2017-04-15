from Crypto import Random
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from constants import Constant as const
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
	hs = const().HASH_SIZE
	hash_given = txt[:hs]
	return txt[hs:] if hash_given == getHash(txt[hs:]) else False

def enlarge384(meta):
	ms = const().HEADER_SIZE
	hs = const().HASH_SIZE
	padding = "".join([chr(0)] * ms - hs - len(meta) - 2).encode()
	return chr(len(padding)).encode() + meta + padding

def enlarge255(filename):
	fns = const().FILENAME_SIZE
	padding = "".join([chr(0)] * (fns - len(filename) - 1)).encode()
	return chr(len(filename)).encode() + filename.encode() + padding

def aesEncrypt(iv, key, txt):
	return AES.new(key, AES.MODE_CFB, iv).encrypt(addHash(txt))

def aesDecrypt(iv, key, xtx):
	return removeHash(AES.new(key, AES.MODE_CFB, iv).decrypt(xtx))
	
def packMeta(filename, iv, key, start_f, end_f):
	start_f = ('%0*x'%(19,start_f)).encode()
	end_f = ('%0*x'%(19,end_f)).encode()
	filename = enlarge255(filename)
	return filename + iv + key + start_f + end_f

def depackMeta(meta):
	f_len = Constant().FILENAME_SIZE
	iv_len = Constant().IV_SIZE
	key_len = Constant().AESKEY_SIZE
	s_offset_len = Constant().FILE_START_OFFSET_SIZE
	e_offset_len = Constant().FILE_END_OFFSET_SIZE
	filename = deflateFilename(meta[:f_len])
	iv = meta[f_len : iv_len]
	key = meta[f_len + iv_len : key_len]
	start_f = meta[f_len + iv_len + key_len: s_offset_len ]
	end_f = meta[f_len + iv_len + key_len + s_offset_len: ]
	return (deflateFilename(filename), iv, key, start_f, end_f)

