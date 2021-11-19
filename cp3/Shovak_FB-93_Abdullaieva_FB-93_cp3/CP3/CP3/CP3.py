import math
import re
import codecs
import random
import numpy as np


file=codecs.open("1.txt","r","utf_8_sig")
text=file.read()
text1=re.sub(r"[^а-я+ё]+", " ", text.lower()).replace("ё","е").replace(" ", "")

FILE = codecs.open("1_es.txt", "r","utf_8_sig")
TEXT = FILE.read()
TEXT1 = re.sub(r"[^а-я+ё]+", " ", TEXT.lower()).replace("ё","е").replace(" ", "")
alphabet = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ь','ы','э','ю','я']

#Most common bigrams
#bigram1 = [['с','т'], ['н','о'], ['т', 'о'], ['н','а'], ['е','н']] # вихідный текст
#bigram2 = [['р','н'], ['ы','ч'], ['н','к'], ['ц','з'], ['и','а']] # вхідний текст
bigram1 = [['с','т'], ['е','н']]
bigram2 = [['р','н'], ['н','к']]

#Euqlid algorythm
def euclid_ext(a, n):
    if n == 0:
        return a, 1, 0
    else:
        d, x, y = euclid_ext(n, a % n)
        return d, y, x - y * (a // n)

def reverse(a, n):
    gcd, x, y = euclid_ext(a, n)
    if gcd == 1:
        return (x % n + n) % n
    else:
        return -1

def euclid(a, y, n):
    gcd, y1, x1 = euclid_ext(a, n)
    if gcd == 1:         # знаходимо обернений
        x = reverse(a,n)
        return x
    elif y % gcd != 0: # немає розв`язкі
        return False
    else:
        euclid(a/gcd, y/gcd, n/gcd)

#Find the number of most common bigrams
def max_bigram(text):
    mass = []
    mass1 = []
    line = [text[k:k + 2] for k in range(0, len(text), 2)]
    new_line = set(line)
    for i in new_line:
        number = line.count(i)
        mass.append([i,number])
    sorted_bigrams = sorted(mass, key=lambda x: x[1])
    for i in range(5):
        mass1.append(sorted_bigrams[-(i+1)])
        mass.clear()
    for i in range(len(mass1)):
        mass.append(mass1[i][0])
    return (mass)

def index(i):
    X1 = alphabet.index(bigram1[i][0]) * 31 + alphabet.index(bigram1[i][1])
    Y1 = alphabet.index(bigram2[i][0]) * 31 + alphabet.index(bigram2[i][1])
    X2 = alphabet.index(bigram1[i + 1][0]) * 31 + alphabet.index(bigram1[i + 1][1])
    Y2 = alphabet.index(bigram2[i + 1][0]) * 31 + alphabet.index(bigram2[i + 1][1])
    return X1, Y1, X2, Y2

def find_key():
    mass = []
    for i in range(len(bigram2)-1):
        X1, Y1, X2, Y2 = index(i)
        a = (euclid(X1-X2, Y1-Y2, 31 ** 2)*(Y1-Y2)) % (31 ** 2)
        b = (Y1 - a * X1) % (31 ** 2)
        mass.append([a,b])
    return (mass)

def decrypt(text):
    arr = []
    arr1 = []
    mass = find_key()
    line = [text[k:k + 2] for k in range(0, len(text), 2)]
    for i in range(len(line)):
        A = mass[0][0]
        B = mass[0][1]
        Y = alphabet.index(line[i][0])*31 + alphabet.index(line[i][1])
        X = (reverse(A,31**2) *(Y - B))% 31**2
        arr.append(X)
    for i in range(len(arr)):
        letter = alphabet[arr[i] // 31] + alphabet[arr[i] % 31]
        arr1.append(letter)
    return(''.join(arr1))

print(decrypt(TEXT1))
