import numpy as np
import time
import matplotlib.pyplot as plt
import os
from Decryptor import lab_2_Decryptor as L2D
from Cryptor import lab_2_Cryptor as L2C

if __name__ == '__main__':
	start_time = time.time()
	cryptor = L2C("./voina_i_mir_small.txt")
	keys = "да нет киви жалко " \
		   "приветкиви " \
		   "приветжалко " \
		   "приветкивида " \
		   "приветжалкода " \
		   "приветжалконет " \
		   "приветкивижалко " \
		   "приветкивикивида " \
		   "приветкивикивинет " \
		   "приветкивижалконет " \
		   "приветжалкожалконет " \
		   "приветивижалкокивида"

	keys = keys.split(" ")

	for key in keys:
		text = cryptor.encrypt(key)
		with open(f"./examples/{key}.txt", 'wb') as outfile:
			outfile.write(cryptor.toStr(text).encode("utf-8"))
		print(cryptor.toStr(text)[:10])
