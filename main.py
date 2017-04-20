from files_utils import *
from aes_utils import *
from constants import *
from commandline import CmdLineParser as Cli
from time import time
import sys

def randomString():
	""" Return string from 512SHA(time.time()) """
	return "".join([chr(c) for c in getHash(str(time).encode())])
	
def newVolume():
	size = Cli().get('--size=',0 ,int)
	if not size > 0:
		print(' Error, volume size must be > 0. Exiting ')
		sys.exit(1)
			
	print('Type a password for the outer volume')
	outer_pass = getPassword(3)
	if not outer_pass:
		print('Error, to many try. Exiting')
		sys.exit(1)
	
	print('Type a password for the inner volume')
	inner_pass = getPassword(3)		
	if not inner_pass:
		print('Error, to many try. Exiting')
		sys.exit(1)
	
	name = Cli().get('--file-name=',randomString() ,str)	
	volume_info = ShadowVolume().new(size, name, outer_pass, inner_pass)
	if not volume_info:
		print('Error, you failed dick head')
		sys.exit(1)
	else:
		print('Volume {} succesfully created. Exiting.'.format(volume_infos['name']))
		sys.exit(0)
				
def printHelp():
	help_text = """ help text """
	print(help_text)
	
if __name__ == "__main__":
	if Cli().isset('--new'):			# Nouveau volume
		newVolume()
	elif Cli().isset('--add'):			# Ajout d'un fichier
		pass
	elif Cli().isset('--del'):			# Suppression d'un fichier
		pass
	elif Cli().isset('--get'):			# Extraction d'un fichier
		pass
	elif Cli().isset('--list'):			# Liste les fichier du volume
		pass
	elif Cli().isset('--update-psswd'):	# Change le mot de passe
		pass							
	elif Cli().isset('--help'):			# Affiche l'aide
		printHelp()
	else:								# Affiche l'aide
		printHelp()
