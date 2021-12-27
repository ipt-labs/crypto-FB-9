import numpy as np
from Text_Container import Text_Container as TK


class lab_2_Cryptor(TK):
	def __init__(self, filename, keys=None):
		"""		:param filename: path to the file ot read
		"""
		super().__init__(filename)


	def encrypt(self, key, copy=0, mode="characters"):
		key = self.forwardTrans(np.array(list(key)))
		if copy == 1:
			arr = np.copy(self.getNumbers())
		else:
			arr = self.getNumbers()
		for z in range(0, len(key)):
			for x in np.nditer(arr[z::len(key)], op_flags=['readwrite']):
				x[...] = (x + key[z]) % 32
		if mode == "characters":
			return self.backwardTrans(arr)
		elif mode == "numbers":
			return arr
