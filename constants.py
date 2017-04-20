class Constant(object):
	def __init__(self):
		# Size in bytes
		self.IV_SIZE = 16
		self.SALT_SIZE = 8
		self.AESKEY_SIZE = 32
		self.HASH_SIZE = 64
		self.FILENAME_SIZE = 255
		self.FILE_START_OFFSET_SIZE = 17		# ('%0*x'%(19, 2**64)).encode()
		self.FILE_END_OFFSET_SIZE = 17 		# File size offset = 64 bits
		self.META_SIZE = 401
		self.HEADER_SIZE = self.META_SIZE + self.HASH_SIZE +self.IV_SIZE +self.SALT_SIZE
		self.HEADERS_NUMBER = 2
class ConstantSize(object):
	def __init__(self):
		super().__init__()
		self.IV = 16
		self.SALT = 8
		self.AESKEY = 32
		self.HASH = 64
		self.FILENAME = 255
		self.FILE_START_OFFSET = 17		# ('%0*x'%(19, 2**64)).encode()
		self.FILE_END_OFFSET = 17 		# File size offset = 64 bits
		self.META = 401
		self.HEADER = self.META + self.HASH +self.IV +self.SALT
		self.HEADERS_NUMBER = 2
	
