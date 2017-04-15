from aes_2key_altername import *
from files_utils import *
from constants import *
from aes_utils import *

if __name__ == "__main__":
	print('From constants.Constant():\n')
	for elm in Constant().__dict__:
		print('{}: {}'.format(elm, Constant().__dict__[elm]))
	print('------------------------------------')

	
	print('From aes_utils.py:\n')
	ivf = rndIv()
	print('rndIv(): %s: %s\n'%(ivf, len(ivf)))
	salt = rndSalt()
	print('rndSalt(): %s: %s\n'%(salt, len(salt)))
	keyf = rndKey()
	print('rndKey(): %s: %s\n'%(keyf, len(keyf)))
	
	txt = b'hello world!'
	print('source text: %s: %s\n'%(txt, len(txt)))
	hash_ = getHash(txt)
	print('getHash(txt): %s: %s\n'%(hash_, len(hash_)))
	xtx = aesEncrypt(ivf, keyf, txt)
	print('aesEncrypt(iv, key, txt): %s: %s\n'%(xtx, len(xtx)))
	txt = aesDecrypt(ivf, keyf, xtx)
	print('aesDecrypt(iv, key, xtx): %s: %s\n'%(txt, len(txt)))
	filename = 'test.txt'
	start_f = 0
	end_f = 2**64
	
	meta = packMeta(filename, ivf, keyf, start_f, end_f)
	print('packMeta(filename, iv, key, start_f, end_f): %s: %s\n'%(meta, len(meta)))
	print('len: filename = meta[0] : %s'%int(meta[0]))
	
	print('Meta encrypt section:\n')
	ivm = rndIv()
	print('rndIv(): %s\n'%ivm)
	saltm = rndSalt()
	print('rndSalt(): %s\n'%saltm)
	keym = rndKey(salt= saltm, password ='paswword')
	print('rndKey(): %s\n'%keym)
	atem = aesEncrypt(ivm, keym, meta)
	print('aesEncrypt(iv, key, meta): %s: %s\n'%(atem, len(atem)))
	meta = aesDecrypt(ivm, keym, atem)
	print('aesDecrypt(iv, key, atem): %s: %s\n'%(meta, len(meta)))
	print('------------------------------------')
