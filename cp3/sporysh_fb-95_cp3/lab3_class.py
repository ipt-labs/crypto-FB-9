import numpy as np
from itertools import product
import time
from Text_Container import Text_Container as TK


def Sort(arr):
    return arr[arr[:, 1].argsort()[::-1]]


def gcd(x, y):
    return x if y == 0 else gcd(y, x % y)


def EGCD(a, b):
    if a == 0:
        return b, 0, 1
    Gcd, x1, y1 = EGCD(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return Gcd, x, y


def rev(x, m):
    Gcd, a, b = EGCD(x, m)
    if Gcd == 1:
        return (a % m + m) % m


def Lin(a, b, m):
    Gcd = gcd(a, m)
    if Gcd == 1:
        return [rev(a, m) * b % m]
    if Gcd > 1 and (b // Gcd == 0):
        a1 = a / Gcd
        b1 = b / Gcd
        m1 = m / Gcd
        first = rev(a1, m1) * b1 % m1
        return [first + m1 * i for i in range(Gcd)]


def createNgram(array):
    ngrames, counts = np.unique(array, return_counts=True)
    counts2 = np.array([item / np.sum(counts) for item in counts])
    return np.asarray((ngrames, counts2), dtype=object).T


class lab_3_class(TK):

    def __init__(self, filename):
        """
		:param filename: path to the file ot read
		"""
        super().__init__(filename)
        self.__common_mono = np.array(['о', 'е', 'а', 'и', 'н', 'т'])
        self.__common_bigr = np.array(["ст", "но", "то", "на", "ен"])
        self.__encoded = None
        self.__encrypted = None

        # Monograms
        self.__monogr      = np.array([self.getText()[i:i + 1] for i in range(0, len(self.getText()), 1)])
        self.__monogr_freq = createNgram(self.__monogr)
        self.__bigr        = np.array([self.getText()[i:i + 2] for i in range(0, len(self.getText()), 2)])
        self.__bigr_freq   = createNgram(self.__bigr)

    def getCommon(self):
        return self.__common_mono, self.__common_bigr

    def selfSort(self):
        self.__monogr_freq = Sort(self.__monogr_freq)
        self.__bigr_freq   = Sort(self.__bigr_freq)

    def getNgrams(self):
        return self.__monogr, self.__bigr

    def getNgramsFreq(self):
        return self.__monogr_freq, self.__bigr_freq

    def encode_one(self, bigr):
        bigr = self.forwardTrans(bigr)
        return bigr[0] * self.get_A_len() + bigr[1]

    def decode_one(self, number):
        for a in range(self.get_A_len()):
            for b in range(self.get_A_len()):
                reversed_a = rev(a, self.get_A_len())
                if reversed_a is None:
                    break
                else:
                    if self.get_A_len() == (reversed_a * (number - b) % (self.get_A_len() ** 2)):
                        return self.backwardTrans(a, single=True) + self.backwardTrans(b, single=True)
                    if 0 == (reversed_a * (number - b) % (self.get_A_len() ** 2)):
                        return self.backwardTrans(0, single=True) + self.backwardTrans(b, single=True)

    @staticmethod
    def encrypt_one(bigr, key, m):
        return (key[0] * bigr + key[1]) % (m ** 2)

    @staticmethod
    def decrypt_one(bigr, key, m):
        a = key[0]
        reversed_a = rev(a, m ** 2)
        if reversed_a is None:
            return
        b = key[1]
        return reversed_a * (bigr - b) % (m ** 2)

    def encode(self, bigr, copy=False):
        if copy:
            arr = np.copy(bigr)
        else:
            arr = bigr
        arr = np.array([self.encode_one(x) for x in arr])
        return arr

    def decode(self, bigr, copy=False):
        if copy:
            arr = np.copy(bigr)
        else:
            arr = bigr
        arr = np.array([self.decode_one(x) for x in arr if x is not None])
        return arr

    def encrypt(self, bigr, key, copy=False):
        if copy:
            arr = np.copy(bigr)
        else:
            arr = bigr
        arr = np.array([self.encrypt_one(x, key, self.get_A_len()) for x in arr])
        return arr

    def decrypt(self, bigr, key, copy=False):
        if copy:
            arr = np.copy(bigr)
        else:
            arr = bigr
        arr = np.array([self.decrypt_one(x, key, self.get_A_len()) for x in arr])
        return arr

    def findText(self):
        mono, bigr = self.getCommon()
        self.selfSort()
        enc_mono_freq, enc_bigr_freq = self.getNgramsFreq()
        keys = []
        for x in (product(range(5), repeat=4)):
            X1 = self.encode_one(bigr[x[0]])
            X2 = self.encode_one(bigr[x[1]])
            Y1 = self.encode_one(enc_bigr_freq[:, 0][x[2]])
            Y2 = self.encode_one(enc_bigr_freq[:, 0][x[3]])
            VTD = (X1 - X2) % (self.get_A_len() ** 2)
            STD = (Y1 - Y2) % (self.get_A_len() ** 2)
            if VTD == 0 or STD == 0:
                continue
            results = Lin(VTD, STD, self.get_A_len()**2)
            if results is not None:
                for a in results:

                    b = (Y1 - a * X1)
                    while b < 0:
                        b += (self.get_A_len() ** 2)
                    b = b % (self.get_A_len() ** 2)
                    key = [int(a), b]
                    if key not in keys:
                        keys.append(key)
        with open(f"./my_keys.txt", 'w', encoding='utf-8') as outfile:
            text = ''
            for item in keys:
                text += f"A::{item[0]} B::{item[1]}\n\r"
            outfile.write(text)
        print(f"\n{len(keys)} keys in total\napproximate execution time is:\n--- {len(keys) * 7} seconds ---")
        enc_mono, enc_bigr = self.getNgrams()
        for i, key in enumerate(keys):
            print(f"Key::{i}\t{key}")
            start_time = time.time()
            temp_text = np.array(self.decrypt(self.encode(enc_bigr), key, copy=True))
            temp_text = self.decode(temp_text)
            temp_text_str = ''.join(temp_text)
            test_monogr = np.array([temp_text_str[i:i + 1] for i in range(0, len(temp_text_str), 1)])
            test_monogr_freq = Sort(createNgram(test_monogr))
            test_bigr_freq   = Sort(createNgram(temp_text))
            most_common_test_mono = test_monogr_freq[:, 0][:6]
            most_common_test_bigr = test_bigr_freq[:, 0][:5]

            if len(set(most_common_test_mono) & set(mono)) >= 5 and len(set(most_common_test_bigr) & set(bigr)) >= 1:
                print(most_common_test_mono)
                print(mono)
                print(most_common_test_bigr)
                print(bigr)
                print(temp_text_str[:30])
                with open(f"./samples/{temp_text_str[:10]}_{key[0]}_{key[1]}.txt", 'w', encoding='utf-8') as outfile:
                    outfile.write(temp_text_str)

            print("--- %s seconds ---\n" % (time.time() - start_time))