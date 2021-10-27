from collections import Counter

with open('text.txt', 'r', encoding = 'utf-8') as f:
    plaintext = f.read()

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
