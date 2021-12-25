import math
import random
import time


# p=9
# def toBinary(n):
#     r = []
#     while (n > 0):
#         r.append(n % 2)
#         n = n//2
#         return (r)

# def MillerRabin(n, s = 50):
#     for j in range(1, s + 1):
#             a = random.randint(1, n - 1)
#             b = toBinary(n - 1)
#             d = 1
#             for i in range(len(b) - 1, -1, -1):
#                 x = d
#                 d = (d * d) % n
#                 if d == 1 and x != 1 and x != n - 1:
#                 	return False
#                 else:
# 	                if b[i] == 1:
# 	                    d = (d * a) % n
# 	                    if d != 1:
# 	                    	return False
# 	                    return True
# 	                return True
# MillerRabin(p)
# print("All primes smaller than 100: ");
# for n in range(2,100):
#     if (MillerRabin(n, 9)):
#         print(n , end=" ");


k=50
def rozklad(p):
	s=0
	m=p-1
	while (m)%2==0:
		s+=1
		m=m//2
	d=int(m)
	return(d,s)
print(rozklad(13))

def bezout(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return (x, y, a)

def rabinchik(p,k):
	if (p <=1 or p==4):
		return False
	if (p<=3 or p==5 or p==7):
		return True
	if p%2 == 0 or p%3==0 or p%4==0 or p%5==0 or p%6 ==0 or p%7==0 or p%8==0 or p%9 == 0 or p%10==0:
		return False
	d,s=rozklad(p)
	for i in range(0,k):
		x=random.randint(2,p-1)
		c=pow(x,d,p)
		if c==1 or c==p-1:
			continue
		for r in range(0,s):
			c=pow(c,2,p)
			if c==1:
				return False
			elif c==p-1:
				break
			elif r==(s-1):
				return False
	return True

print(bezout(7,13))
print("All primes smaller than 100: ");
for n in range(2,100):
	if (rabinchik(n, 9)):
		print(n , end=" ");


def GenKeyPair():
	p=6
	q=6
	h=6
	y=6
	while p*q>=h*y:
		while rabinchik(p,k)==False:
			p = random.randrange(pow(2,256-1)+1, pow(2,256)-1)
		while rabinchik(q,k)==False:
			q = random.randrange(pow(2,256-1)+1, pow(2,256)-1)
		while rabinchik(h,k)==False:
			h = random.randrange(pow(2,256-1)+1, pow(2,256)-1)
		while rabinchik(y,k)==False:
			y = random.randrange(pow(2,256-1)+1, pow(2,256)-1)
	# print(p*q)
	# print(h*y)
	print("Ключ1=",p,"Ключ2=",q)
	print("Ключ1.2=",h,"Ключ2.2=",y)


p=67512136282248018078248869036918237922196268580297879484859703749803669070211
q=78676697896440637294008922382573488923755595169284286091196429573589060552927
p1=59765155917446913335915906580399204582284398205670562082569807697501514510011
q1=105681535007857362835701952203255787725518019392775001591498826275856866765727
def Evklid(a,b):
	if b==0:
		return a,1,0
	else:
		d, x, y = Evklid(b, a % b)
		return d, y, x - y * (a // b)
def Para(size,p,q):
	n=p*q
	o=(p-1)*(q-1)
	i = 1
	while i==1:
		e = random.randrange(2, o-1)
		if Evklid(e,o)[0]==1:
			i = 0
	d = int(Evklid(e,o)[1])%o
	secretniy = d
	publichnniy = [n,e]
	return secretniy,publichnniy
def Encrypt(t,e,n):
	c = pow(t,e,n)
	return c

def Decrypt(c,d,n):
	m=pow(c,d,n)
	return m

def Sign(m,d,n):
	s=pow(m,d,n)
	return s

def Verify(m,s,e,n):
	if m==pow(s,e,n):
		return True

def SendKey(k,e1,n1,d,n):
	k1=pow(k,e1,n1)
	s=pow(k,d,n)
	s1=pow(s,e1,n1)
	return k1,s1,s


def ReceiveKey(k1,s1,d1,n1,s,e,n):
	k=pow(k1,d1,n1)
	s=pow(s1,d1,n1)
	if k==pow(s,e,n):
		print("Soobshenie Verificirovano")
		return k,s
	else:
		print("Soobshenie ne Verificirovano")
		return False

secretniykluchOtpravitel, publichniykluchOtpravitel = Para(256, p, q)
secretniykluchPoluchatel, publichniykluchPoluchatel = Para(256, p1, q1)

print("\n","d =", secretniykluchOtpravitel,"\n","n =", publichniykluchOtpravitel[0],"\n","e =", publichniykluchOtpravitel[1],"\n","d1 =", secretniykluchPoluchatel,"\n", "n1 =", publichniykluchPoluchatel[0],"\n","e1 =", publichniykluchPoluchatel[1])
print("\n","d =", hex(secretniykluchOtpravitel),"\n","n =", hex(publichniykluchOtpravitel[0]),"\n","e =", hex(publichniykluchOtpravitel[1]),"\n","d1 =", hex(secretniykluchPoluchatel),"\n", "n1 =", hex(publichniykluchPoluchatel[0]),"\n","e1 =", hex(publichniykluchPoluchatel[1]))

k = random.randrange(1, publichniykluchOtpravitel[0]-1)
print("\nk =",k)
print("\nk =",hex(k))
m = random.randrange(1, publichniykluchOtpravitel[0]-1)
print("\nm =",m)
print("\nm =",hex(m))

cOtpravitel = Encrypt(m, publichniykluchOtpravitel[1], publichniykluchOtpravitel[0])
print("\ncOtpravitel=",cOtpravitel)
print("\ncOtpravitel=",hex(cOtpravitel))
print("\n m =",Decrypt(cOtpravitel, secretniykluchOtpravitel, publichniykluchOtpravitel[0]))
print("\n m =",hex(Decrypt(cOtpravitel, secretniykluchOtpravitel, publichniykluchOtpravitel[0])))


cPoluchatel = Encrypt(m, publichniykluchPoluchatel[1], publichniykluchPoluchatel[0])
print("\ncPoluchatel=",cPoluchatel)
print("\ncPoluchatel=",hex(cPoluchatel))
print("\n m =",Decrypt(cPoluchatel, secretniykluchPoluchatel, publichniykluchPoluchatel[0]))
print("\n m =",hex(Decrypt(cPoluchatel, secretniykluchPoluchatel, publichniykluchPoluchatel[0])))


podpisOtpravitel = Sign(m, secretniykluchOtpravitel, publichniykluchOtpravitel[0])
print("\npodpisOtpravitel =",podpisOtpravitel)
print("\npodpisOtpravitel =",hex(podpisOtpravitel))

if Verify(m,podpisOtpravitel, publichniykluchOtpravitel[1], publichniykluchOtpravitel[0]):
	print("verificirovano")

podpisPoluchatel = Sign(m, secretniykluchPoluchatel, publichniykluchPoluchatel[0])
print("\npodpisPoluchatel =",podpisPoluchatel)
print("\npodpisPoluchatel =",hex(podpisPoluchatel))

if Verify(m,podpisPoluchatel, publichniykluchPoluchatel[1], publichniykluchPoluchatel[0]):
	print("verificirovano")

k1, s1, s = SendKey(k, publichniykluchPoluchatel[1],  publichniykluchPoluchatel[0],secretniykluchOtpravitel, publichniykluchOtpravitel[0])
print("A otpravil kluch")
print("k1 = ",k1)
print("s1 = ",s1)
print("B poluchil kluch!")

ReceiveKey(k1,s1, secretniykluchPoluchatel, publichniykluchPoluchatel[0], s, publichniykluchOtpravitel[1], publichniykluchOtpravitel[0])



k1, s1, s = SendKey(k, int("10001", 16), int("9ED4FAC0862DB1ADA233E04FAB43694E784F255C01D8D94F8D8593AC952FCBDCF54EBF0694A87584608B2ABDF57E8B41D3B33BEE3CDC02AC9E8D3BA4DB37B7C7", 16),secretniykluchOtpravitel, publichniykluchOtpravitel[0])

print("k1 = ",hex(k1))
print("s1 = ",hex(s1))
print("s = ",hex(s))