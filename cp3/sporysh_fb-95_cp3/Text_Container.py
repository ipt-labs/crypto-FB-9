import re
import numpy as np


class Text_Container:

	def __init__(self, filename):
		"""
		:param filename:
		"""
		# if valid name of file
		try:
			with open(filename, encoding="utf8")as file:
				self.__text = re.sub('[^абвгдежзийклмнопрстуфхцчшщьыэюя]', '', file.read().lower())
		# filename is a string
		except:
			self.__text = re.sub('[^абвгдежзийклмнопрстуфхцчшщьыэюя]', '', filename)
		self.__text = re.sub('[ё]', 'е', self.__text)
		self.__text = re.sub('[ъ]', 'ь', self.__text)
		self.__chars = np.array(list(self.getText()))
		self.__alplabet = np.array(list("абвгдежзийклмнопрстуфхцчшщьыэюя"))
		self.__alpth_len = len(self.__alplabet)
		self.__indexes = np.arange(0, len(self.__alplabet), 1)
		self.__trans_table = np.asarray((self.__alplabet, self.__indexes), dtype=object).T
		self.__numbers = self.forwardTrans(self.__chars)

	def get_A(self):
		return self.__alplabet

	def get_A_len(self):
		return self.__alpth_len

	def getNumbers(self):
		return self.__numbers

	def getTT(self):
		return self.__trans_table

	def forwardTrans(self, chars, copy=0, single=False):
		if single:
			for y in range(0, self.__trans_table.shape[0]):
				if chars == self.__trans_table[y, 0]:
					return self.__trans_table[y, 1]
			return
		retVal = []
		if not isinstance(chars, np.ndarray):
			chars = np.array(list(chars))

		for x in chars:
			for y in range(0, self.__trans_table.shape[0]):
				if x == self.__trans_table[y, 0]:
					retVal.append(self.__trans_table[y, 1])
		if copy == 1:
			return np.copy(np.array(retVal))
		return np.array(retVal)

	def backwardTrans(self, numbers, copy=0, single=False):
		if single:
			for y in range(0, self.__trans_table.shape[0]):
				if numbers == self.__trans_table[y, 1]:
					return self.__trans_table[y, 0]
			return
		retVal = []
		for x in numbers:
			for y in range(0, self.__trans_table.shape[0]):
				if x == self.__trans_table[y, 1]:
					retVal.append(self.__trans_table[y, 0])
		if copy == 1:
			return np.copy(np.array(retVal))
		return np.array(retVal)

	def getText(self):
		return self.__text

	@staticmethod
	def toStr(notStr):
		return ''.join(map(str, notStr))

# def getTextW(self): return self.__text_w
