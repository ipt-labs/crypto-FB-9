from io import open, open_code
from collections import Counter

f = open('text.txt', 'r', encoding='utf-8')
text = f.read()
f.close()
text = text.lower()
text = ' '.join(text.split())

alphabet = 'абвгдежзийклмнопрстуфхцчщъыьэюя'

preptext = ''

for i in text:
    if i in alphabet:
        preptext = preptext + i

f = open('preptext.txt', 'w', encoding='utf-8')
f.write(preptext)
f.close()

r = ['ка', 'при', 'зова', 'попул', 'евнаселенияаз']

def encrypt(text, key):
    etext = ''
    for i in range(len(text)):
        x = alphabet.find(text[i])
        k = alphabet.find(key[i % len(key)])
        etext = etext + alphabet[(x+k) % len(alphabet)]
    return etext


for i in range(len(r)):
    f = open(str(i) + '.txt', 'w', encoding='utf-8')
    f.write(encrypt(preptext, r[i]))
    f.close()

f = open('opentxt.txt', 'r', encoding='utf-8')
opentext = f.read()
f.close()

def compindex(text):
    count_dict = Counter(text)
    x = 0
    for i in count_dict:
        x += count_dict[i]*(count_dict[i]-1)
    x /= len(text)/(len(text)-1)
    return x

f = open('compindex.txt', 'a', encoding='utf-8')
f.write('i = ' + str(compindex(opentext)) + '\n')
f.close()

for i in range(5):
    f = open(str(i)+'.txt', 'r', encoding='utf-8')
    text = f.read()
    f.close()
    f = open('compindex.txt', 'a', encoding='utf-8')
    f.write('i = ' + str(compindex(text)) + '\n')
    f.close()

def theoretical_compindex(text):
    count_dict = Counter(text)
    thecoind = 0
    for i in count_dict:
        count_dict[i] /= len(text)
        thecoind += count_dict[i]**2
    return thecoind

