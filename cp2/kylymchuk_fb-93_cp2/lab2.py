from collections  import Counter 
import math

with open("enctext.txt") as file:
    f=file.read()

with open("task3.txt") as file:
    t=file.read()

alph = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
keys=["ой", "как", "игра", "мешок", "автономный", "авиапосылка", "горообразный", "криптостойкий", "авиасоединение", "эллинистический", "дезодорированный","кратковременность", "легитимизированный", "сверхрациональность", "воздухоочистительный"]

def encoder(text, key):
    encrypt=[]
    for i in range(0, len(text)):
        encrypt.append(alph[((alph.index(text[i])+alph.index(key[i%len(key)]))%32)])
    return "".join(encrypt)

def index(text):
    ind=0
    for i in alph:
       ind+=Counter(text)[i]*(Counter(text)[i]-1)
    ind/=(len(text)*(len(text)-1))
    return ind

print("індекс для ВТ:", index(f))
for i in range (0, 15):
   print("для ключа длиной", len(keys[i]), ":", index(encoder(f, keys[i])))

def kroneker(text, r):
    d=0
    for i in range (0, len(text)-r):
        if text[i]==text[i+r]:
            d+=1
        i+=1
    return d

for i in range(5, 35):
    print(i, ":", kroneker(t, i))

def decoder(text, key):
    decrypt=[]
    for i in range(0, len(text)):
        decrypt.append(alph[((alph.index(text[i])-alph.index(key[i%len(key)]))%32)])
    return "".join(decrypt)

def findkey(text):
    r = 17
    key = []
    for i in range(r):
        symb = []
        for j in range(i, len(text), r):
            symb.append(text[j])
        k = (alph.index(Counter(symb).most_common(1)[0][0])-alph.index('о'))%32
        key.append(alph[k])
    return ''.join(i for i in key)

print(findkey(t))
key="венецианскийкупец"
print(decoder(f, key))