import random

def Euclid(a, b):
	print("GSD(", a, ",", b, ")")
	q = a // b

	r = a - (b * q)
	if (r != 0):
		b = Euclid(b, r)
		return b
	else:
		print("b:", b)
		return b

def Euclid_extra(a, b, q_vect):
	q = a // b
	q_vect.append(q)
	r = a - (b * q)
	if (r != 0):
		q_vect = Euclid_extra(b, r, q_vect)
		return q_vect
	else:
		print("b:", b)
		return q_vect

def Euclid_extra2(q_vect, u, v, count):
	u1 = []
	v1 = []
	for i in range(0, len(q_vect)):
		u1.append(u[count - 2] - q_vect[count - 2] * u[count - 1])
		v1.append(v[count - 2] - q_vect[count - 2] * v[count - 1])
		u.append(u1[len(u1)-1])
		v.append(v1[len(v1)-1])
		count = count+1
	print(u1)
	print(v1)
	return v1[len(v1)-2]

def prime_number(p):
	if(p%3==0):
		print("3|n")
		return False
	if(p%5==0):
		print("5|n")
		return False
	if(p%7==0):
		print("7|n")
		return False
	if(p%11==0):
		print("11|n")
		return False
	else:
		p0=p-1
		s=1
		s0=0
		d=0
		while(p0%2==0): #step 0
			p0 = p0//2
			s=s*2
			s0=s0+1
		d = (p-1)//s
		#d = int(d)
		print("d:", d, "2^s:", s, "s:", s0, "p-1:", p-1)
		counter = 0
		k=10
		while(counter<k):
			print("counter:", counter, "k:", k)
			x = random.randint(2, p-1) #step 1
			print("x:", x)
			if(Euclid(p, x)!=1):
				return False
			x_pow_d = pow(x, d, p)
			#print("x^d:", x_pow_d)
			print("x^d modp:", x_pow_d)
			if(x_pow_d==1): #step 2.1
				print("strong pseudo 1")
				counter = counter+1
			else:
				for i in range(0, s0): #step 2.2
					x_pow_d_2i = pow(x,d*pow(2,i),p)
					print("x^(d*2^i)modp:", x_pow_d_2i)
					if(x_pow_d_2i==p-1):
						print("strong pseudo 2")
						counter = counter+1
						break
					elif(x_pow_d_2i==1):
						print("not strong pseudo2")
						return False
					elif(i==s0-1):
						print("not strong pseudo1") #step 2.3
						return False
		return True

def GenerateKeyPair():
	print("Function!!!")
	#n0=2
	#n1 = 100
	n0 = 10000000000000000000000000000000000000000000000000000000000000000000000000000000
	n1 = 100000000000000000000000000000000000000000000000000000000000000000000000000000000 
	prime_p=0
	while(prime_p==0):
		random_x = random.randint(n0, n1)
		print(random_x)
		if(random_x%2==0):
			print("even")
			m0=random_x+1
		else:
			print("odd")
			m0=random_x
		for i in range(0, ((n1-m0)//2)+1):
			print(m0+2*i)
			if(prime_number(m0+2*i)==True):
				prime_p=m0+2*i
				break
			else:
				prime_p=0
				print(m0+2*i,"is not prime!")

	print(prime_p, "is PRIME")
	prime_q=0
	while(prime_q==0):
		random_x = random.randint(n0, n1)
		print(random_x)
		if(random_x%2==0):
			print("even")
			m0=random_x+1
		else:
			print("odd")
			m0=random_x
		for i in range(0, ((n1-m0)//2)+1):
			print(m0+2*i)
			if(prime_number(m0+2*i)==True):
				prime_q=m0+2*i
				break
			else:
				prime_q=0
				print(m0+2*i,"is not prime!")

	print(prime_q, "is PRIME")
	return (prime_p, prime_q)

def gcd_euler(fi):
	check = 0
	while(check==0):
		e = random.randint(2, fi-1)
		print("e:",e)
		for i in range(e, fi-1):
				print(i)
				if(Euclid(fi, i)==1):
					e=i
					check=i
					break
				else:
					check=0
	
	return e

def inverted_element(e, fi):
	u = [1, 0]
	v = [0, 1]
	q_vector = []
	q_vector = Euclid_extra(fi, e, q_vector)
	#print(q_vector, q_vector[0], q_vector[1], q_vector[len(q_vector)-1])

	e_invert = Euclid_extra2(q_vector, u, v, 2)
	while(e_invert<0):
		e_invert = fi + e_invert
	return e_invert

def Encrypt(M, e, n):
	C = pow(M,e,n)
	print("C=",M,"^",e,"mod",n)
	return C

def Decrypt(C, d, n):
	M = pow(C,d,n)
	print("M=",C,"^",d,"mod",n)
	return M

def Sign(M, d, n):
	S = pow(M, d, n)
	print("S=",M,"^",d,"mod",n)
	return S

def Verify(S, e, n):
	M = pow(S, e, n)
	print("M=",S,"^",e,"mod",n)
	return M
		
p, q = GenerateKeyPair()
p1, q1 = GenerateKeyPair()
print("GenerateKeyPair #1:", p, "and", q)
print("GenerateKeyPair #2:", p1, "and", q1)
while(p==q):
	p, q = GenerateKeyPair()
while(p1==q1):
	p1, q1 = GenerateKeyPair()
n=p*q
n1=p1*q1
print("n #1:", n)
print("n #2:", n1)
while(n>n1):
	p, q = GenerateKeyPair()
	p1, q1 = GenerateKeyPair()
	while(p==q):
		p, q = GenerateKeyPair()
	while(p1==q1):
		p1, q1 = GenerateKeyPair()
	n=p*q
	n1=p1*q1
	print("GenerateKeyPair #1:", p, "and", q)
	print("GenerateKeyPair #2:", p1, "and", q1)
	print("n:", n)
	print("n1:", n1)

fi_n = (p-1)*(q-1)
fi_n1 = (p1-1)*(q1-1)
print("fi(n):", fi_n)
print("fi(n1):", fi_n1)

e = gcd_euler(fi_n)
e1 = gcd_euler(fi_n1)

print("final e:", e)
print("final e1:", e1)

d = inverted_element(e, fi_n)
d1 = inverted_element(e1, fi_n1)
print("final d:", d)
print("final d1:", d1)

M = int(input("Enter your message: "))
print(M)
C = Encrypt(M, e, n)
print("C=",C)
M1 = int(input("Enter your message: "))
print(M1)
C1 = Encrypt(M1, e1, n1)
print("C1=",C1)

M_decrypted = Decrypt(C, d, n)
print("M=",M_decrypted)
M1_decrypted = Decrypt(C1, d1, n1)
print("M1=",M1_decrypted)

S = Sign(M, d, n)
print("S=",S)
S1 = Sign(M1, d1, n1)
print("S1=",S1)

M_sign = Verify(S, e, n)
print("M=",M_sign)
M1_sign = Verify(S1, e1, n1)
print("M1=",M1_sign)

class Abonent:
	def __init__(self, e,n,d,e1,n1):
		self.e = e
		self.n = n
		self.d = d
		self.e1 = e1
		self.n1 = n1
	def SendKey(self):
		k = random.randint(1, n-1)
		S = pow(k,self.d,self.n)
		print("k:",k)
		k1 = pow(k, self.e1, self.n1)
		print("k1=",k,"^",self.e1,"mod",self.n1,"=",k1)
		print("S=",k,"^",self.d,"mod",self.n,"=",S)
		S1=pow(S,self.e1,self.n1)
		print("S1=",S,"^",self.e1,"mod",self.n1,"=",S1)
		return (k1,S1)
	def ReceiveKey(self,k1,S1):
		k = pow(k1, self.d,self.n)
		print("k=",k1,"^",self.d,"mod",self.n,"=",k)
		S = pow(S1,self.d,self.n)
		print("S=",S1,"^",self.d,"mod",self.n,"=",S)
		k_1 = pow(S,self.e1,self.n1)
		print("k(sign)=",S,"^",self.e1,"mod",self.n1,"=",k_1)
		return (k,S,k_1)

A = Abonent(e,n,d,e1,n1)
key_k1,key_S1 = A.SendKey()
print("A:")
print("k1:",key_k1)
print("S1:",key_S1)
B = Abonent(e1,n1,d1,e,n)
key_k,key_S,key_k_1 = B.ReceiveKey(key_k1,key_S1)
print("B:")
print("k:",key_k)
print("S:",key_S)
print("k_1:",key_k_1)

#SendKey()

#print(random.randint(10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000))
