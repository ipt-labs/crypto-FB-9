import re
from collections  import Counter
import random

alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
alph1 = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
with open('text.txt','r',encoding='utf-8') as f:
	txt = f.read()
txt = re.sub("[^А-Яа-я]", "", txt)
txt = txt.replace('\n', '')
txt = txt.lower()
print(txt,'\n')

with open('shifrtxt.txt','r', encoding= 'utf-8') as f:
	shifrtxt = f.read()

shifrtxt = re.sub("[^А-Яа-я]", "", shifrtxt)
shifrtxt = shifrtxt.replace('\n', '')

with open('shifrtxt.txt','w',encoding ='utf-8') as f:
	f.write(shifrtxt)
	print(shifrtxt)

def Keys1():
	keys=[]
	for i in range(2,6):
		str = ''.join(random.choice(alph) for m in range(i))
		keys.append(str)
	print('\n',keys)
	return keys

def Keys2():
	keys=[]
	for i in range(10,21):
		str = ''.join(random.choice(alph) for m in range(i))
		keys.append(str)
	print('\n',keys)
	return keys

Keys2to5 = Keys1()
Keys10to20 = Keys2()
Keys = Keys2to5+Keys10to20
print('\n',Keys,'\n',len(Keys))

#task 1
def encrypt(txt,key):
	encrTxt = []
	for i in range(len(txt)):
		encrTxt.append(alph[(alph.index(txt[i]) + alph.index(key[i % len(key)]))% len(alph)])
	EncryptedText = ''.join(encrTxt[i] for i in range(len(encrTxt)))
	print('\n'," key - ",key,'\n')
	print(EncryptedText)
	with open("EncryptText.txt",'w',encoding = "utf-8") as encryptfile:
		encryptfile.write(EncryptedText)
	return EncryptedText

#encrypt(txt,Keys[4])
#task 2
def indexFormula(txt):
	index = 0
	lettersCounts = Counter(txt)
	for i in lettersCounts:
		index +=lettersCounts[i]*(lettersCounts[i] - 1)
	index /= (len(txt))*(len(txt)-1)

	return index



def indexCalc():
	index = {}
	for i in range(len(Keys)):
		encrTxt = encrypt(txt,Keys[i])
		index[len(Keys[i])] = indexFormula(encrTxt)
	print('\n',index)
	return index
indexCalc()

def Blocks(txt,l):
	blocks = []
	for i in range(l):
		blocks.append(txt[i::l])

	return blocks

def KeySearch():
	dic = {}
	for i in range(1, 31):
		block = Blocks(shifrtxt, i)
		ind = 0
		for b in block:
			ind += indexFormula(b)
		ind /= i
		dic[i] = ind
	print('\n',dic)
	#print('\n','symbols -',max(dic),max(dic.values()))
	return dic
KeySearch()

def OurKey(len_key):
    block = Blocks(shifrtxt, len_key)
    let = "аео"
    for l in let:
        ourkey =""
        for b in block:
            blocksCalc = Counter(b[i] for i in range(len(b)))
            maxCalc = max(blocksCalc, key=blocksCalc.get)
            ourkey+=alph1[(alph1.index(maxCalc)-alph1.index(l))%len(alph1)]
        print(ourkey)

OurKey(max(KeySearch(), key=KeySearch().get))


def decrypt(key,shifrtxt):
    decrTxt = []
    for i in range(len(shifrtxt)):
        decrTxt.append( alph1[(alph1.index(shifrtxt[i]) - alph1.index(key[i % len(key)]) % len(alph1))])
    text = ''.join(decrTxt[i] for i in range(len(decrTxt)))

    return text

ourkey = 'крадущийсявтени'
ourText = decrypt(ourkey, shifrtxt)
file= open('ourtext.txt', 'w', encoding='utf-8')
file.write(ourText)
#indexTask1 = indexFormula(txt)