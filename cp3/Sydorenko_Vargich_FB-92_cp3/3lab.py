# Алгоритм Евкліда
def Euclid_gcd(a,m):
	Q = []
	P = [0,1]
	M = m
	A = a
	if m > a:
		if m % a == 0:
			gcd = a	
		else:
			q = m // a 
			Q.append(-q)
			r = m % a 
			while r != 0:
				m = a
				a = r
				r = m % a 
				if r == 0:
					gcd = a
					break
				q = m // a 
				Q.append(-q)
	return gcd


# Обернений елемент
def Inv_el_Euclid(a,m):
	Q = []
	P = [0,1]
	M = m
	A = a
	if m > a:
		if m % a == 0:
			gcd = a
		else:
			#i = 0
			q = m // a 
			Q.append(-q)
			r = m % a 
			while r != 0:
				m = a
				a = r
				#i += 1
				r = m % a 
				if r == 0:
					gcd = a
					break
				q = m // a 
				Q.append(-q)
			if gcd == 1:
				for i in range(len(Q)):
					p = Q[i] * P[-1] + P[-2]
					P.append(p)
			else: 
				print("gcd(",A,",",M,"!= 1 ----> can't find inversed element.")
			return p


# Лінійне порівняння
def linear(a,b,m):
	a = a % m
	b = b % m
	d = Euclid_gcd(a,m)
	if d == 1:
		#1 rozvyazok
		inv_a = Inv_el_Euclid(a,m)
		x = (inv_a * b) % m
	elif d > 1 and b % d != 0:
		# bez rozvyazkiv
		x = 0 
	elif d > 1 and b % d == 0:
		# d rozvyazkiv
		a = a // d
		b = b // d
		m = m // d
		inv_a = Inv_el_Euclid(a,m)
		x0 = (inv_a * b) % m
		i = 0
		x = []
		while i < d:
			x.append(x0 + m*i)
			i += 1
	else:
		x = -1
	return x


# 5 найчастіших біграм
def freq_bigrams(file):	
	with open(file, "r", encoding="utf-8") as reader:
	    lis = reader.read()
	    global l
	    l = lis.replace(" ","").replace("\n","")
	    global length
	    length = len(l)

	top5_bigrams = []
	bigram_freq = {}
	all_bigrams = 0
	res = {}
	for i in range(length-1):
	    bigram = (l[i], l[i+1])
	    if bigram not in bigram_freq:
	        bigram_freq[bigram] = 0
	    bigram_freq[bigram] += 1
	    all_bigrams += 1    
	for key in bigram_freq:
	    res[key] = bigram_freq[key]/all_bigrams
	list_res = list(res.items())
	list_res.sort(key=lambda i: i[1], reverse=True)
	B = 1
	for i in list_res:
		if B > 5:
			break
		top5_bigrams.append(i[0])
		B += 1       
	return top5_bigrams

#формування словника із 5 найчастіших біграм шифротексту та їх Yi (y1*m+y2) 
def dict_top5_bigram_and_Y(T5):
	for i in T5:
		Yi = char_to_number(i[0]) * 31 + char_to_number(i[1])
		Y_dict[i] = Yi	
	return Y_dict


#на вход - буква, на выход - ее число (из словаря alphabet)       
def char_to_number(letter):
    number = alphabet[letter]
    return number

#на вход - число, на выход - буква (из словаря alphabet)
def get_letter(num):
    for k, v in alphabet.items():
        if v == num:
            return k

# функція для створення вищезазначеного словника
def create_Y_dict(f):
	return dict_top5_bigram_and_Y(freq_bigrams(f))

#list --> string
def listToString(s): 
    str1 = "" 

    for ele in s: 
        str1 += ele  
    
    return str1 


#частота определенной буквы текста
def char_freq(char,decrypted_str):
	z = 0
	len_d = len(decrypted_str)
	for i in range(len_d):
		ch = decrypted_str[i]
		if ch == char:
			z += 1
	return z/len_d


# Функція, що знаходить а та b (пункт 3 у методичці)
def xy1_xy2():
	for y1 in Y_list:
		for x1 in X_list:
			xy1 = (y1,x1)
			for y2 in Y_list:
				if y1 == y2:
					continue
				for x2 in X_list:
					if x1 == x2:
						continue
					xy2 = (y2,x2)
					mm = 961
					b = (y1-y2)%mm
					a = (x1-x2)%mm
					# xa == a in metodichka
					xa = linear(a,b,mm)
					if isinstance(xa,list):
						for i in xa:
							ya = (y1 - i * x1) % mm
							print('a =',i," ", 'b =',ya)
					elif isinstance(xa,int):
						if xa == 0 or xa == -1:
							continue
						elif Euclid_gcd(xa,mm) != 1:
							continue
						else:
							#ya == b in metodichka
							ya = (y1 - xa * x1) % mm
							decrypted_list = []
							for i in range(length-1):
								if i % 2 == 0:
									bigram = (l[i], l[i+1])
									Y = char_to_number(bigram[0]) * 31 + char_to_number(bigram[1])
									# K == Yi - b in metodichka
									K = Y - ya
									X = (Inv_el_Euclid(xa,mm)*K) % mm
									ans_x1 = X // 31
									ans_x2 = X - 31 * ans_x1
									first_in_X_bigram = get_letter(ans_x1)
									second_in_X_bigram = get_letter(ans_x2)
									decrypted_list.append(first_in_X_bigram)
									decrypted_list.append(second_in_X_bigram)
							decrypted_str = listToString(decrypted_list)
							if char_freq('о',decrypted_str) < 0.104: 
								continue
							else:	
								print('\t' + '-' * 23 + '\n' +'\t|' + ' Key: a = '+str(xa) + ' b = ' + str(ya),'|\n' + '\t' + '-' * 23, '\n' * 2, decrypted_str,'\n')
								'''with open('decrypted.txt', 'w') as filee:
									filee.write('Key: a = ' + str(xa) + 'b = ' + str(ya) + "\n" + decrypted_str + '\n')'''
								exit()



alphabet = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9, 'к': 10, 'л': 11,

        'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 

        'ч': 23, 'ш': 24, 'щ': 25, 'ы': 26, 'ь': 27, 'э': 28, 'ю': 29, 'я': 30}


X_dict = {('с', 'т'): 545, ('н', 'о'): 417, ('т', 'о'): 572, ('н', 'а'): 403, ('е', 'н'): 168}
Y_dict = {}
X_list = [i for i in X_dict.values()]
Y_list = [create_Y_dict('09.txt')[i] for i in create_Y_dict('09.txt')]
l = 0


create_Y_dict('09.txt')
xy1_xy2()

