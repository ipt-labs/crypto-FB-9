import random
import math
a = pow(2,256)

def miller_rabin(n, k=4):
    if n < 3: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            if n == p: return n
            else: return False
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for i in range(k):
        x = pow(random.randint(2, n - 1), d, n)
        if x == 1 or x == n - 1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1:return False
            if x == n - 1: break
        else: return False
    return n

def generate_key(a):
    while True:
        n = random.randint(a,a*2)
        p = miller_rabin(n)
        if p is not False:break
    return p


def generate_pq():
    p, q = generate_key(a), generate_key(a)
    p1, q1 = generate_key(a), generate_key(a)
    while p * q > p1 * q1:
        p, q = generate_key(a), generate_key(a)
        p1, q1 = generate_key(a), generate_key(a)
    return p, q, p1, q1


def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = gcd(b % a, a)
        return g, y - (b // a) * x, x


def find_mod_inv(b, n):
    g, x, y = gcd(b, n)
    if g == 1:
        return x % n

def generete_key_pair(p,q):
    e = pow(2,16)+1
    n=p*q
    fi=(p-1)*(q-1)
    d=find_mod_inv(e,fi)
    return [e,n], [d,p,q]

def encrypt(M, en):
    return pow(M, en[0], en[1])


def decryption(C, dpq):
    return pow(C, dpq[0], dpq[1]*dpq[2])


def sign(M, secret, open1):
    C=encrypt(M, [secret[0], secret[1]*secret[2]])  #S=k**d mod(n)
    C1=encrypt(M, open1)        #k1=k**e1 mod(n1)
    S1=encrypt(C, open1)        #S1=S**e1 mod(n1)
    return [C1, S1]


def verify(Messege, open, secret1):
    M=decryption(Messege[0], secret1)
    C=decryption(Messege[1], secret1)
    k=encrypt(C,open)
    return [M, M==k]


def sendkey(M, secret, open1):
    signed = sign(M, secret, open1)
    print('Massage sended', signed)
    return signed


def receivekey(signed, open, secret1):
    verifyed=verify(signed, open, secret1)
    print('Massage received', verifyed)
    return verifyed


p, q, p1, q1 = generate_pq()
print("p*q", p*q, "\np1*q1",p1*q1)
open, secret = generete_key_pair(p, q)
open1, secret1 = generete_key_pair(p1, q1)
M=random.randint(0,2**256)
print('m=',M)
C=sendkey(M, secret, open1)
receivekey(C, open, secret1)

#Server tests

# open_test=["10001","9D5E56535B05820AD9D17C1AD1CBEEAEFEE2AD5A757C6B155DCE6C4B5EB7524B"]
# print("Open key",open_test)
# open_test[0],open_test[1]=int(open_test[0], 16),int(open_test[1], 16)
# M_test="text to penis"
# print("Message '"+ M_test+"'")
# M_test = int(M_test.encode().hex(), 16)
# C_test=encrypt(M_test,open_test)
# print("Ciphertext",hex(C_test)[2:])
# sign="77B3F041D5663A222A723D3BE708E7CA64C99CF3AFAAA0161727C4F5FED536DD"
# sign=int(sign, 16)
# print("sign is", M_test==encrypt(sign, open_test))
