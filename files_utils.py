def writeFile(outfilename, txt):
	with open(outfilename,'wb') as f:
		f.write(txt)
		return True
	return False

def writeFile_b64(outfilename, txt):
	with open(outfilename,'wb') as f:
		f.write(b64encode(txt))
		return True
	return False

def getAllHeaders(filename):
	with open(filename, 'rb'):
		headers = [] * Constant().HEADER_NUMBER
		for i in range(len(headers) -1):
			head = f.read(Constant().HEADER_SIZE)
			if len(head) == 0:
				break
			else:
				headers[i] = head
		return headers
	return False
	
