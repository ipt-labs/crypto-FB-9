import numpy as np
from Text_Container import Text_Container as TK
import os

class lab_2_Decryptor(TK):

	def __init__(self, filename):
		"""
		:param filename: path to the file ot read
		"""
		super().__init__(filename)
		self.__monogr_freq = None
		self.__monogr_quan = None
		self.__most_freq = "оаеин"

		# Monograms
		monogr_list = np.array([self.getText()[i:i + 1] for i in range(0, len(self.getText()), 1)])
		self.__monogr_quan, self.__monogr_freq = self.createNgram(monogr_list)

	@staticmethod
	def createNgram(array):
		ngrames, counts = np.unique(array, return_counts=True)
		counts2 = np.array([item / np.sum(counts) for item in counts])
		return np.asarray((ngrames, counts), dtype=object).T, np.asarray((ngrames, counts2), dtype=object).T

	def getAll(self):
		return self.__monogr_freq, self.__monogr_quan

	# Індекс відповідності
	@staticmethod
	def getIndex(i_t_len, mono_q):
		quan = mono_q[:, 1]
		return np.sum(quan * quan - 1) / (i_t_len * (i_t_len - 1))

	def getTextIndex(self):
		iters = ["All"]
		values = [self.getIndex(len(self.getText()), self.__monogr_quan)]
		return np.asarray((iters, values), dtype=object).T

	def getResult(self):
		while True:
			key_length = int(input("\n::-1 exit\n::0 skip\nВведіть можливу довжину ключа: "))
			if key_length == -1:
				break
			if key_length == 0:
				continue
			arr = []
			for start in range(0, key_length):
				temp_text = np.array(list(self.getText()[start::key_length]))
				temp_array = self.createNgram(temp_text)[1]
				temp_array = temp_array[temp_array[:, 1].argsort()[::-1]]
				arr.append(temp_array[0, 0])
			# print(self.toStr(arr))
			arr = np.array(arr)
			while True:
				print(f"default text: {self.toStr(arr)}")
				for x in self.__most_freq:
					print(f"'{x}': {self.toStr(self.decrypt(arr, x))}")
				possible_key = np.array(list(input(f"\n::press 'F' to exit loop\nВведіть можливий ключ (довжина {key_length}) : ")))
				if self.toStr(possible_key) == "F":
					break
				print(self.toStr(self.decrypt(self.getText()[:key_length], possible_key)))
				save = input("Сохранить? ('да' to save): ")
				if save == 'да':
					f = open(f"./{self.toStr(possible_key)}.txt", "wb")
					f.write(self.toStr(self.decrypt(self.getText(), possible_key)).encode("utf-8"))
					f.close()
				os.system("pause")

	def decrypt(self, arr, key, copy=0, mode="characters"):
		key = self.forwardTrans(np.array(list(key)))
		if copy == 1:
			arr = np.copy(arr)
		else:
			arr = arr
		arr = self.forwardTrans(arr)
		for z in range(0, len(key)):
			for x in np.nditer(arr[z::len(key)], op_flags=['readwrite']):
				x[...] = (x - key[z]) % 32
		if mode == "characters":
			return self.backwardTrans(arr)
		elif mode == "numbers":
			return arr

	# Всі індекси відпповідності
	def getIndexes(self, key_length):
		iters = [f"{x}" for x in range(0, key_length)]
		values = []
		for start in range(0, key_length):
			# key_length == step
			temp_text = np.array(list(self.getText()[start::key_length]))
			temp_array = self.createNgram(temp_text)[0]
			values.append(self.getIndex(len(temp_text), temp_array))

		iters = np.array(iters)
		values = np.array(values)
		return np.asarray((iters, values), dtype=object).T
