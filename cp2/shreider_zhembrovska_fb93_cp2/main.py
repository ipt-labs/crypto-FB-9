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

def decryption(text,key):
    plaintext = []
    for i in range(len(text)):
        x = (alph.index(text[i]) - alph.index(key[i % len(key)])) % 32
        plaintext.append(alph[x])
    return ''.join(i for i in plaintext)

def coindex(text):
    nt = Counter(text)
    index = 0
    for i in nt:
        index += nt[i]*(nt[i]-1)
    index /= (len(text)*(len(text)-1))
    return index

def findkey(text,expv):
    r = keylen(text,expv)
    key = []
    for i in range(r):
        y = []
        for j in range(i, len(text), r):
            y.append(text[j])
        key.append(alph[ikey(y)])
    return ''.join(i for i in key)

def keylen(text, expv):
    rindex = []
    for r in range(2,33):
        index = 0
        for i in range(r):
            y = []
            for j in range(i, len(text), r):
                y.append(text[j])
            index += coindex(y)
        index /= r
        rindex.append(abs(index - expv))
    return rindex.index(min(rindex))+2

def exp(text):
    freq = Counter(text)
    expv = 0
    for i in freq:
        freq[i] /= len(text)
        expv += pow(freq[i],2)
    return expv

def ikey(text):
    freq_in_language = alph.index('о') # e - предпоследняя н,
    freq_in_ctext = alph.index(freqletter(text))
    key = (freq_in_ctext-freq_in_language)%32
    return key

def freqletter(text):
    freq = Counter(text)
    maxnum = max(Counter(text).values())
    for key, value in freq.items():
        if value == maxnum: return key


#for r in keys:
#    print("r:",r,''.join(i for i in encryption(r)))
#x = encryption(2)
#y = indexcoinc(x)
#for i in range(len(keys)):
#    print(coindex(encryption(plaintext,keys[i])))
key = 'возвращениеджинна'
print(decryption(ciphertext,findkey(ciphertext,exp(plaintext))))

