import random
import math
#import colorama
'''import time
start_time = time.time()'''

def isPrime(p):
	if p == 1:
		return False

	if p == 2 or p == 3 or p == 5 or p == 7 or p == 11 or p == 13 or p == 17:
		return True

	elif p % 2 == 0 or p % 3 == 0 or p % 5 == 0 or p % 7 == 0 or p % 11 == 0 or p % 13 == 0 or p % 17 == 0:
		return False
	else:
		d = p - 1
		s = 0
		while d % 2 == 0:
			s += 1
			d //= 2
		#print("d =",d,"s =",s)
		x = random.randint(2,p-1)
		gcd = math.gcd(x,p)        ### step 1
		if gcd == 1:
			#try p -? strong pseudoprime (base x) 
			if Gorner(x,d,p) == 1 or Gorner(x,d,p) == -1:   ### step 2
				#print('p - strong ...')
				return True
			else:
				xr = Gorner(x,d,p)
				if xr - p == -1:		
					return True
				elif xr == 1:
					return False
				for r in range(1,s):
					xr = Gorner(xr,2,p)
					if xr - p == -1:		
						return True
					elif xr == 1:
						return False
				return False
		elif gcd > 1:
			return False
	#return True


def Miller_Rabin(p,k=100):
	for i in range(0,k):
		res = isPrime(p)
		if res == False:
			break
	return res


#generate prime number
def GenPrime(start=pow(10,127),finish=pow(10,128)):
	p = random.randrange(start,finish)
	#colorama.init()
	while Miller_Rabin(p) == False:
		#print(colorama.Fore.RED + "NOT APPROPRIATE: "+str(p))
		p = random.randrange(start,finish)
	#print(colorama.Style.RESET_ALL)
	return p  


#generate p, q, p1, q1
def GenPairs():
	p = GenPrime()
	q = GenPrime()
	p1 = GenPrime()
	q1 = GenPrime()
	while p*q > p1*q1:
		p = GenPrime()
		q = GenPrime()
	return p, q, p1, q1


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
			if gcd == 1:
				for i in range(len(Q)):
					p = Q[i] * P[-1] + P[-2]
					P.append(p)
				if p < 0:
					p = p + M
			else: 
				print("gcd(",A,",",M,"!= 1 ----> can't find inversed element.")
			return p


# generate PUBLIC and SECRET keys 
def RSA(p,q):
    n = p * q
    Euler = (p-1)*(q-1)
    #e = GenPrime(2,Euler)
    e = 65537
    if math.gcd(e,Euler) == 1:
        d = Inv_el_Euclid(e,Euler)
    public_key = (n, e)
    secret_key = (d, p, q)
    return public_key, secret_key


#Представление числа в двоичном виде
def toBin(num):
	b = "{0:b}".format(num)
	return b     #it's a string


def Gorner(x,e,n):
	e_str_bin = toBin(e)
	#e_str_bin = e_str_bin.replace("-","")
	e_str_bin_list = list(e_str_bin)
	binary_list = list(map(int,e_str_bin_list))
	y = 1
	for i in binary_list:
		y = pow(y,2,n) 
		y = (y * pow(x,i)) % n
		#print('i =',i,'y =',y)
	return y

#Представление текста в виде какого-то числа
def text_to_number(text_to_send):
	textbytes = text_to_send.encode('utf-8')
	number = int.from_bytes(textbytes, 'little')
	#print(number)
	return number

#"Возврат" числа в текст
def number_to_text(number):
	recoveredbytes = number.to_bytes((number.bit_length() + 7) // 8, 'little')
	recoveredstring = recoveredbytes.decode('utf-8')
	#print(recoveredstring)
	return recoveredstring


def Gen_M(plaintext):
	M = text_to_number(plaintext)
	print("A side: Plaintext converted to number (М):",M)
	return M


def Encryption(M, PubKey):
	e = PubKey[1]
	n = PubKey[0]
	C = Gorner(M,e,n)
	#print(C)
	return C    #number


def Decryption(C, SecKey):
	n = SecKey[1]*SecKey[2]
	d = SecKey[0]
	M = Gorner(C,d,n)
	print("B side: M gained by an addressee:",M)
	plaintext = number_to_text(M)
	return plaintext    #information which originally has been passed on


#Створення цифрового підпису
def Sign(M,SecKey):
	d = SecKey[0]
	n = SecKey[1]*SecKey[2]
	#S = M^d mod n
	S = Gorner(M,d,n)
	return M, S


#Перевірка цифрового підпису
def Verify(MS_tuple,PubKey):
	M_check = Gorner(MS_tuple[1],PubKey[1],PubKey[0])
	if MS_tuple[0] == M_check:
		return M
	return False


def SendKey(k,PubKey1,PubKey,SecKey):
	#(k1,S1)
	n = PubKey[0]
	d = SecKey[0]
	S = Gorner(k,d,n)
	e1 = PubKey1[1]
	n1 = PubKey1[0]
	k1 = Gorner(k,e1,n1)
	S1 = Gorner(S,e1,n1)
	return k1, S1


def ReceiveKey(tuple_of_k1_S1,PubKey1,PubKey,SecKey1):
	d1 = SecKey1[0]
	n1 = PubKey1[0]
	k1 = tuple_of_k1_S1[0]
	S1 = tuple_of_k1_S1[1]
	k = Gorner(k1,d1,n1)
	S = Gorner(S1,d1,n1)
	e = PubKey[1]
	n = PubKey[0]
	k_authentification = Gorner(S,e,n)
	if k == k_authentification:
		return k


def A_data():
	n = public_key[0]
	e = public_key[1]
	d = secret_key[0]
	p = secret_key[1]
	q = secret_key[2]	
	print('Сторона А:\nn =',n,'\ne =',e,'\nd =',d,'\np =',p,'\nq =',q,'\n')	


def B_data():
	n = public_key1[0]
	e = public_key1[1]
	d = secret_key1[0]
	p = secret_key1[1]
	q = secret_key1[2]	
	print('Сторона B:\nn =',n,'\ne =',e,'\nd =',d,'\np =',p,'\nq =',q,'\n')

alphabet = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9, 'к': 10, 'л': 11,

        'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 

        'ч': 23, 'ш': 24, 'щ': 25, 'ы': 26, 'ь': 27, 'э': 28, 'ю': 29, 'я': 30}


p, q, p1, q1 = GenPairs()
public_key, secret_key = RSA(p,q)
public_key1, secret_key1 = RSA(p1,q1)
A_data()
B_data()

#Шифрування
print('Шифрування:')
PlainText = 'Наутилус Помпилиус'
PlainText = PlainText.replace(" ","").replace("\n","").replace("-","").lower()
print('A side: Original text of a sender (text to send):', PlainText)
M = Gen_M(PlainText)
encrypted_message = Encryption(M, public_key)
print('A side: Encrypted message (С):', encrypted_message,'\n==========\n')

#Розшифрування
print('Розшифрування:')
decrypted_message = Decryption(encrypted_message, secret_key)
print('B side: Decrypted message (Obtained text from a sender):', decrypted_message)
print('\n'*3)

#Підписання відкритого повідомлення
MS_signature = Sign(M, secret_key)
print('Пiдписання вiдкритого повiдомлення:\nM = ',MS_signature[0],'\nS =', MS_signature[1])

#Перевірка підпису
checked_M = Verify(MS_signature, public_key)
print('\n\nПеревiрка пiдпису:\nM =', checked_M)

#Надсилання ключа
K = 7146570146780147086
k1_S1_tuple = SendKey(K,public_key1,public_key,secret_key)
print('\n\nКлюч надiслано\nk =',K)

#Перевірка відправника
print('\nПеревiрка вiдправника:\nk =',ReceiveKey(k1_S1_tuple,public_key1,public_key,secret_key1),'\n\n')

#print("--- %s seconds ---" % (time.time() - start_time))