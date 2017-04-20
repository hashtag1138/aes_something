from aes_utils import *
from files_utils import *
from constants import * 
from commandline import CmdLineParser as Cli

if __name__== "__main__":
	#PARSE CLI
	in_file = open(Cli().get('--if=', 'if.test.txt'), 'rb')
	try:
		host_file =  open(Cli().get('--host-file=', 'of.test.x'), 'rb')
	except:
		host_file = False
	b64_mode = True if Cli().get('--b64=', 'False') == 'True' else False
	password = Cli().get('--psswd', 'password')
	
	#OPEN FILE
	txt_clear = readClear(in_file)
	host_content = readClear(host_file) if host_file else b''
	
	#ENCRYPT FILE
	ivf = rndIv()
	keyf = rndKey()
	txt_encrypted = aesEncrypt(ivf, keyf, txt_clear)
	
	
	
	
