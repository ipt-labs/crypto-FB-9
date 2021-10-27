import math
from collections import Counter

with open('plaintext.txt', 'r', encoding = 'utf-8') as f:
    plaintext = f.read()

with open('ciphertext.txt', 'r', encoding = 'utf-8') as f:
    ciphertext = f.read()

alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
keys = ['ай','кот','мать','жесть','разложение','превращение','трагикомедия','недоразумение','нравственность',
        'амариллисцветок','мягенькаяподушка','пельменискетчупом','неспатьаделатьлабу','киберполицияукраины','женоненавистничесвто']

def encryption(text,key):
    ciphertext = []
    for i in range(len(text)):
        y = (alph.index(text[i])+alph.index(key[i%len(key)]))%32
        ciphertext.append(alph[y])
    return ''.join(i for i in ciphertext)

def coindex(text):
    nt = Counter(text)
    index = 0
    for i in nt:
        index += nt[i]*(nt[i]-1)
    index /= (len(text)*(len(text)-1))
    return index

def findkeylen(text):
    rindex = []
    for r in range(2,31):
        index = 0
        for i in range(r):
            y = []
            for j in range(i, len(text), r):
                y.append(text[j])
            index += coindex(y)
        rindex.append(abs(index - 0.553))
    return rindex.index(min(rindex)) + 2


