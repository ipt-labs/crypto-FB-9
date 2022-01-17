import math
import re

file = open('D:\\Git\\1\\fb-labs-2021\\cp_1\\Roha_fb-92_cp1\\text.txt', encoding='utf-8')
alfavit = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ы','ь','э','ю','я']
alfavitzprob = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ы','ь','э','ю','я',' ']
rawtext = file.read()
rawtext = rawtext.lower()
text = re.sub("[”|„|&|$|“|>|+|/|<| |,|.|!|?|-|-|‒|—|;|:|–|-|»|«|-|*|1|2|3|4|5|6|7|8|9|0|#|…|(|)|-|'|№|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z]", " ", rawtext)
text = re.sub(r'\s+', ' ', text)
text = text.replace("ё", "е")
text = text.replace("ъ", "ь")
characters = len(text)
tekstbezprob = text.replace(" ", "")
lentekstbezprob = len(tekstbezprob)

def chastotabezprob():
	print('-----------------------------------------------------------------')
	i=0
	while i<31:
		print(alfavit[i],tekstbezprob.count(alfavit[i])/lentekstbezprob)
		i+=1
	print('-----------------------------------------------------------------')

def chastotazprob():
	i=0
	while i<31:
			print(alfavit[i],text.count(alfavit[i])/characters)
			i+=1
	print((text.count(" "))/characters)
	print('-----------------------------------------------------------------')

def chislobigramzprob():
	i=0
	j=0
	Sum=0
	while i<32:
		while j<32:
			chislo = text.count(alfavitzprob[i]+alfavitzprob[j])
			Sum+=chislo
			j+=1
			chislo=0
		j=0
		i+=1
	return Sum

def chislobigrambezprob():
	i=0
	j=0
	Sum=0
	while i<31:
		while j<31:
			chislo = tekstbezprob.count(alfavit[i]+alfavit[j])
			Sum+=chislo
			j+=1
			chislo=0
		j=0
		i+=1
	return Sum

chislobigrambezprob = chislobigrambezprob()
chislobigramzprob = chislobigramzprob()

def bigramibezprob():
	i=0
	j=0
	chislo = 0
	while i<31:
		while j<31:
			chislo = tekstbezprob.count(alfavit[i]+alfavit[j])
			#print(alfavit[i],alfavit[j],round((chislo/chislobigrambezprob), 7))
			j+=1
			chislo=0
		j=0
		i+=1

def bigramizprob():	

	i=0
	j=0
	chislo = 0
	while i<32:
		while j<32:
			chislo = text.count(alfavitzprob[i]+alfavitzprob[j])
			#print(alfavitzprob[i],alfavitzprob[j],round((chislo/chislobigramzprob), 7))
			j+=1
			chislo=0
		j=0
		i+=1

	


def H1zprob():
	Sum = 0
	i = 0
	while i<31:
		P = text.count(alfavit[i])/characters
		Sum += P * math.log2(P)
		i += 1
	P = text.count(" ")/characters
	Sum += P * math.log2(P)
	print("H1 z prob:%1f"%(-Sum))


def H1bezprob():
	Sum = 0
	i = 0
	while i<31:
		P = tekstbezprob.count(alfavit[i])/lentekstbezprob
		Sum += P * math.log2(P)
		i += 1
	print("H1 bez prob:%1f"%(-Sum))

def H2zprob():
	Sum = 0
	i=0
	j=0
	P = 0
	chislo = 0
	while i<32:
		while j<32:
			chislo = text.count(alfavitzprob[i]+alfavitzprob[j])
			P = chislo/chislobigramzprob
			if P!=0:
				Sum += P * math.log2(P)
			j+=1
			chislo=0

		j=0
		i+=1
	print("H2 z prob:%1f"%(-Sum/2))

def H2bezprob():
	Sum = 0
	i=0
	j=0
	P = 0
	chislo = 0
	while i<31:
		while j<31:
			chislo = tekstbezprob.count(alfavit[i]+alfavit[j])
			P = chislo/chislobigrambezprob
			if P!=0:
				Sum += P * math.log2(P)
			j+=1
			chislo=0

		j=0
		i+=1
	print("H2 bez prob:%1f"%(-Sum/2))

def chastotabigramzprobkrok2():
	res = 0
	d = {}
	ind =0 
	j=0
	while ind<32:
	 	while j<32:
	 		d[alfavitzprob[ind]+alfavitzprob[j]]=0
	 		j+=1
	 	ind+=1
	 	j=0
	bigram = ""
	i = 0
	count = 0
	length = len(text)
	while i<length:
		if text[i]==" " or text[i+1]==" ":
			i+=2
		else:
			bigram = (text[i]+text[i+1])
			d[bigram] += 1
			i+=2
	res = sum(d.values())
	for bigram in d:
		d[bigram] = float(d[bigram]/res)
	list_keys = list(d.keys())
	list_keys.sort()
	#for i in list_keys:
		#print(i)
	#for i in list_keys:
		#print(d[i])
	#print('---------------------')
	Sum = 0
	for bigram in d:
		if d[bigram]!=0:
			Sum += (d[bigram])*math.log2(d[bigram])
	print("H2Krok2 z prob:%1f"%(-Sum/2))

def chastotabigrambezprobkrok2():
	res = 0
	d = {}
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
	length = len(tekstbezprob)
	while i<length-1:
		bigram = (tekstbezprob[i]+tekstbezprob[i+1])
		d[bigram] += 1
		i+=2
	res = sum(d.values())
	for bigram in d:
		d[bigram] = float(d[bigram]/res)
	list_keys = list(d.keys())
	list_keys.sort()
	#for i in list_keys:
		#print(i)
	#for i in list_keys:
		#print(d[i])

	Sum = 0
	for bigram in d:
		if d[bigram]!=0:
			Sum += (d[bigram])*math.log2(d[bigram])
	print("H2Krok2 bez prob:%1f"%(-Sum/2))

chastotabezprob()
chastotazprob()
H1zprob()
H1bezprob()
H2zprob()
H2bezprob()
chastotabigrambezprobkrok2()
chastotabigramzprobkrok2()
bigramizprob()
bigramibezprob()