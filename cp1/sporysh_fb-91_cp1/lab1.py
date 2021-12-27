import numpy as np
import re
import time
import os
import pandas as pd


class Text_Container:

	def __init__(self, filename):
		"""
		:param filename:
		"""
		self.__text = re.sub('[^абвгдёэъежзийклмнопрстуфхцчшщыьюя ]', '',   #Тут читаєм і філтруєм текст
							 open(filename, encoding="utf8").read().lower())
		self.__text = re.sub('[ёэ]', 'е', self.__text)
		self.__text = re.sub('[ъ]', 'ь', self.__text)
		self.__text_w = re.sub('[ ]', '', self.__text)
		self.__text, self.__text_w = self.__text_w, self.__text

	def getText(self):
		return self.__text #no whitespaces

	def getTextW(self):# whitespaces
		return self.__text_w


class lab_1_Text_Container(Text_Container):

	def __init__(self, filename):
		"""

		:param filename: path to the file ot read
		"""
		super().__init__(filename)

		def createNgram(array):
			'''
			[1 1 2 2 2 3 3 3 3 3]
			:param array:
			ngrames is an array of unique values [1 2 3]
			counts is an array of thier occurnces [2 3 5]
			then
			counts is an array of thier freq. [2/len(array) 3/len(array) 5/len(array)]
			[1 2 3]
			[2 3 5]

			(1, 2) (2,3) (3,5)
			:return:
			'''
			ngrames, counts = np.unique(array, return_counts=True)
			counts = np.array([item / np.sum(counts) for item in counts])
			# counts = np.array([np.round(item / np.sum(counts),5) for item in counts])
			return np.asarray((ngrames, counts), dtype=object).T

		# Monograms
		ngram_len = 1
		monogr_list = np.array([self.getText()[i:i + ngram_len] for i in range(0, len(self.getText()), ngram_len)])
		monogr_list_w = np.array([self.getTextW()[i:i + ngram_len] for i in range(0, len(self.getTextW()), ngram_len)])
		self.__monogr = createNgram(monogr_list)
		self.__monogr_w = createNgram(monogr_list_w)

		# Bigrams Noncrossing 123456 12 34 56
		ngram_len = 2
		bigr_n_list = np.array([self.getText()[i:i + ngram_len] for i in range(0, len(self.getText()), ngram_len)])
		bigr_n_list_w = np.array([self.getTextW()[i:i + ngram_len] for i in range(0, len(self.getTextW()), ngram_len)])
		self.__bigr_n = createNgram(bigr_n_list)
		self.__bigr_n_w = createNgram(bigr_n_list_w)

		# Bigrams Crossing 12 23 34 45 56
		bigr_c_list = np.array([self.getText()[i:i + ngram_len] for i in range(0, len(self.getText()))])
		bigr_c_list_w = np.array([self.getTextW()[i:i + ngram_len] for i in range(0, len(self.getTextW()))])
		self.__bigr_c = createNgram(bigr_c_list)
		self.__bigr_c_w = createNgram(bigr_c_list_w)

	def selfSort(self):
		# print(self.__monogr.shape)
		self.__monogr = self.__monogr[self.__monogr[:, 1].argsort()[::-1]]
		self.__monogr_w = self.__monogr_w[self.__monogr_w[:, 1].argsort()[::-1]]
		self.__bigr_n = self.__bigr_n[self.__bigr_n[:, 1].argsort()[::-1]]
		self.__bigr_n_w = self.__bigr_n_w[self.__bigr_n_w[:, 1].argsort()[::-1]]
		self.__bigr_c = self.__bigr_c[self.__bigr_c[:, 1].argsort()[::-1]]
		self.__bigr_c_w = self.__bigr_c_w[self.__bigr_c_w[:, 1].argsort()[::-1]]

	def getEntropy(self):
		# P * log_2(P) / log_2(2*len(2))
		def count_e(item):
			x = item[1] * np.math.log(item[1], 2) / np.math.log(len(item[0] * 2), 2)
			return x

		print(f"Entropy of Monograms ", -1 * np.sum(np.apply_along_axis(count_e, axis=1, arr=self.__monogr)))

		print(f"Entropy of Monograms with Spaces ",
			  -1 * np.sum(np.apply_along_axis(count_e, axis=1, arr=self.__monogr_w)))
		print(f"Entropy of Bigrams (NonCrossing) ",
			  -1 * np.sum(np.apply_along_axis(count_e, axis=1, arr=self.__bigr_n)))
		print(f"Entropy of Bigrams with Spaces (NonCrossing) ",
			  -1 * np.sum(np.apply_along_axis(count_e, axis=1, arr=self.__bigr_n_w)))
		print(f"Entropy of Bigrams (Crossing) ", -1 * np.sum(np.apply_along_axis(count_e, axis=1, arr=self.__bigr_c)))
		print(f"Entropy of Bigrams with Spaces (Crossing) ",
			  -1 * np.sum(np.apply_along_axis(count_e, axis=1, arr=self.__bigr_c_w)))

	def getMonogrs(self):
		"""
		:return:
		"""
		return self.__monogr, self.__monogr

	def getBigrs(self):
		"""
		:return:
		"""
		return self.__bigr_n, self.__bigr_n_w, self.__bigr_c, self.__bigr_c_w,

	def saveData(self, dirname):
		os.mkdir("./" + dirname)

		def format(a):
			return np.round(a[1], 5)

		self.__monogr[:, 1] = np.apply_along_axis(format, 1, self.__monogr)
		self.__monogr_w[:, 1] = np.apply_along_axis(format, 1, self.__monogr_w)
		self.__bigr_n[:, 1] = np.apply_along_axis(format, 1, self.__bigr_n)
		self.__bigr_n_w[:, 1] = np.apply_along_axis(format, 1, self.__bigr_n_w)
		self.__bigr_c[:, 1] = np.apply_along_axis(format, 1, self.__bigr_c)
		self.__bigr_c_w[:, 1] = np.apply_along_axis(format, 1, self.__bigr_c_w)

		pd.DataFrame(self.__monogr).to_csv("./" + dirname + "/self.__monogr.csv")
		pd.DataFrame(self.__monogr_w).to_csv("./" + dirname + "/self.__monogr_w.csv")
		pd.DataFrame(self.__bigr_n).to_csv("./" + dirname + "/self.__bigr_n.csv")
		pd.DataFrame(self.__bigr_n_w).to_csv("./" + dirname + "/self.__bigr_n_w.csv")
		pd.DataFrame(self.__bigr_c).to_csv("./" + dirname + "/self.__bigr_c.csv")
		pd.DataFrame(self.__bigr_c_w).to_csv("./" + dirname + "/self.__bigr_c_w.csv")


if __name__ == '__main__':
	start_time = time.time()
	lab1 = lab_1_Text_Container("./voina_i_mir.txt")
	lab1.selfSort()
	lab1.getEntropy()
	print("--- %s seconds ---" % (time.time() - start_time))
	lab1.saveData("voina_i_mir")
