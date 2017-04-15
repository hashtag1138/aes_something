import sys
class CmdLineParser(object):
	"""
	usage:
		self.get('--option-name', default_value, cli_string)
	"""
	def __init__(self):
		super().__init__()
		pass
		
	def get(self, option, defaut, cmdline=" ".join(sys.argv)):
		start = cmdline.find(option)
		start = start + len(option) if start != -1 else False
		if start :
			end = cmdline[start:].find(" ")
			end = start + end if end != -1 else len(cmdline)
			value = cmdline[start + 1:end]
		try:
			return type(defaut)(value)
		except:
			return defaut
