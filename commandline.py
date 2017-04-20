import sys
class CmdLineParser(object):
	"""
	usage:
		self.get('--option-name', default_value, cli_string)
	"""
	def __init__(self,cmdline=" ".join(sys.argv)):
		super().__init__()
		self.cmdline = cmdline
		pass
		
	# PUBLIC SECTION #		
	def isset(self, option)
		""" Return True if option is in command line """
		return True if self.cmdline.find(option) != -1 else False
			
	def get(self, option, defaut, option_type):
		""" Return the option value after type convertion if there is a 
			value. Return defaut if not. Return False if option 
			not found
		"""
		if not self.isset(option):
			return False
		try:
			return option_type(extract_value(option))
		except:
			return defaut
	
	def test(self, option, option_type):
		""" Return True if the option value can be converted into
			option_type type. Return False if not. """
		try:
			option_type(extract_value(option))
			return True
		except:
			return False
			
	# PRIVATE SECTION #
	def extract_value(self, option):
		""" Return the option value if there is a value. 
			Return False if not."""
		start = self.cmdline.find(option)
		start = start + len(option) if start != -1 else False
		if start :
			end = self.cmdline[start:].find(" ")
			end = start + end if end != -1 else len(self.cmdline)
			return self.cmdline[start + 1:end]
		else:
			return False
