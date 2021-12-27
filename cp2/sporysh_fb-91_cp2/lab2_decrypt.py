import numpy as np
import time
import matplotlib.pyplot as plt
import os
from Decryptor import lab_2_Decryptor as L2D


def visualise_blocks(x, y, mean):
	mask1 = y < mean
	mask2 = y >= mean
	X = np.asarray((x, y), dtype=object).T
	X = X[np.argsort(X[:, 0])]
	x = X[:, 0]
	y = X[:, 1]
	print()
	for t in x:
		print(t, end=" ")
	print()
	for t in y:
		print(round(t,4), end=" ")
	plt.title('Індекси відповідності')
	plt.bar(x[mask1], y[mask1], color='red')
	plt.bar(x[mask2], y[mask2], color='green')
	plt.show()


if __name__ == '__main__':
	start_time = time.time()
	lab2 = L2D("./voina_i_mir_small.txt")
	test_values = [lab2.getTextIndex()[0, 1]]
	samples = os.listdir("./examples")
	x_samples = [-1]

	for filename in samples:
		x_samples.append(len(filename.split(".")[0]))
		lab2 = L2D("./examples/" + filename)
		test_values.append(lab2.getTextIndex()[0, 1])
	visualise_blocks(np.array(x_samples), np.array(test_values), np.array(test_values).mean())
	lab2 = L2D("./10.txt")
	mean_values = []
	for x in range(2, 31):
		mean_values.append(lab2.getIndexes(x)[:, 1].mean())

	mean = np.array(mean_values).mean()
	y = np.array(mean_values)
	x = np.arange(2, 31, 1)
	visualise_blocks(x, y, mean)

	lab2.getResult()

	# print(lab2.getTextIndex())
	print("DONE --- %s seconds ---" % (time.time() - start_time))
