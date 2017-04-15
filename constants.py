class Constant(object):
	def __init__(self):
		# Size in bytes
		self.IV_SIZE = 16
		self.SALT_SIZE = 8
		self.AESKEY_SIZE = 32
		self.HASH_SIZE = 64
		self.FILENAME_SIZE = 255
		self.FILE_START_OFFSET_SIZE = 19		# ('%0*x'%(19, 2**64)).encode()
		self.FILE_END_OFFSET_SIZE = 19 		# File size offset = 64 bits
		self.HEADER_SIZE = 410
		self.HEADERS_NUMBER = 2
	
	
