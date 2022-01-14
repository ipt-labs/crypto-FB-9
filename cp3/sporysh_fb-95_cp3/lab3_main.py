import numpy as np
from lab3_class import *

if __name__ == "__main__":
	start_time = time.time()
	L3 = lab_3_class("./10.txt")
	L3.selfSort()

	### Перші 5 мого та біграми
	ngrams = L3.getNgrams()
	freqs = L3.getNgramsFreq()
	print("Перші 5 монограми та біграми")
	print(" монограми")
	for item in freqs[0][:5]:
		print(f" {item}")
	print()
	print(" біграми")
	for item in freqs[1][:5]:
		print(f" {item}")

	L3.findText()
	print("Program has ended\n--- %s seconds ---\n" % (time.time() - start_time))
