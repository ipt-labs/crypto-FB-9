import math

alfavit = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ь','ы','э','ю','я']
ruspop = ['ст', 'но', 'то', 'на', 'ен']


file=open('10.txt', encoding='utf-8')
text=file.read()
RozshifrovaniyText=open("RozshifrovaniyText.txt","w+")

chistiy_text=text.lower()
for letter in chistiy_text:
	if letter not in alfavit:
		chistiy_text=chistiy_text.replace(letter,"")
def perevirututext(text):
    nepravilnibigrami = ["оь", "уь", "аь", "эь", "юь", "яь", "иь"]
    for bigram in nepravilnibigrami:
        if bigram in text:
            return False
    return True

def Evklid(a,b):
	if b==0:
		return a,1,0
	else:
		d, x, y = Evklid(b, a % b)
		return d, y, x - y * (a // b)

def ZnaytiKluchi(bigrams_open, bigrams_cipher):
	length = len(alfavit)*len(alfavit)
	vsikluchi = []
	y=0
	for i in range(5):
		for j in range(5):
			if i == j:
				pass
			else:
				for z in range(5):
					for x in range(5):
						if z == x:
							pass
						else:
							kluchi = []
							x1 = nomerbigrami(ruspop[i])
							x2 = nomerbigrami(ruspop[j])
							y1 = nomerbigrami(pop[z])
							y2 = nomerbigrami(pop[x])
							xriz = x1-x2
							yriz = y1-y2
							divider = Evklid(xriz, length)[0]
							if divider == 1:
								u = Evklid(xriz, length)[1]
								a = (u * yriz)%length
								b = (y1 - a*x1)%length
								kluchi.append([a,b])
							elif divider>1:
								if yriz % divider == 0:
									while y <(int(divider)):
										a1 = xriz / divider
										b1 = yriz / divider
										n1 = length / divider
										x = ((b1 * Evklid(a1, n1)[1]) % n1) + y * n1
										a = (x * yriz) % length
										b = (y1 - a * x1) % length
										kluchi.append([a, b])
										y+=1
								else:
									y+=1
									pass

							vsikluchi.append(kluchi)

	return vsikluchi

def nomerbigrami(bigram):
    length = len(alfavit)
    nomer = alfavit.index(bigram[0]) * length + alfavit.index(bigram[1])
    return nomer

def affine_decrypt(chistiy_text, a, b):
    roshifrovaniytext = ""
    lengthtext = len(chistiy_text)
    length = len(alfavit) * len(alfavit)
    for i in range(0, lengthtext, 2):
        pershabukva = chistiy_text[i]
        if i < lengthtext - 1:
            druhabukva = chistiy_text[i + 1]
            bigram = pershabukva + druhabukva
            counting = nomerbigrami(bigram)
            a_rev = Evklid(a, length)[1]
            x = ((counting - b) * a_rev) % length
            novadruhabukva = x % len(alfavit)
            novapershabukva = (x - novadruhabukva) / len(alfavit)
            roshifrovaniytext += alfavit[int(novapershabukva)] + alfavit[int(novadruhabukva)]
    return roshifrovaniytext

def chastotabigrambezprobkrok2():
	res = 0
	d = {}
	pop=[]
	ind =0 
	j=0
	while ind<31:
	 	while j<31:
	 		d[alfavit[ind]+alfavit[j]]=0
	 		j+=1
	 	ind+=1
	 	j=0
	bigram = ""
	i = 0
	count = 0
	length = len(chistiy_text)
	while i<length-1:
		bigram = (chistiy_text[i]+chistiy_text[i+1])
		d[bigram] += 1
		i+=2
	res = sum(d.values())
	for bigram in d:
		d[bigram] = float(d[bigram]/res)
	list_kluchi = list(d.keys())
	Sum = 0
	for bigram in d:
		if d[bigram]!=0:
			Sum += (d[bigram])*math.log2(d[bigram])
	for i in list_kluchi:
		if d[i]>0.013:
			pop.append(i)
			print(i,d[i])
	print(pop)
	print("H2Krok2 bez prob:%1f"%(-Sum/2))
	return pop
pop=chastotabigrambezprobkrok2()

def kinez():
	for kluchi in vsikluchi:
		for kluch in kluchi:
			Restext = affine_decrypt(chistiy_text, kluch[0], kluch[1])
			if perevirututext(Restext):
		        	RozshifrovaniyText.write(Restext+'\n'+'\n')
		        	print(kluch[0],kluch[1])

k=0
l=0
while k <5:
	while l <5:
		vsikluchi=ZnaytiKluchi((nomerbigrami(ruspop[k])),nomerbigrami(pop[l]))
		k+=1
		l+=1

kinez()




