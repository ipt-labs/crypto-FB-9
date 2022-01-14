import random

def gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcd(b, a % b)
        return d, y, x - y * (a // b)

def reverse(a, mod):
    return gcd(a, mod)[1] % mod

def MRabintest(n, k):
    n = int(n)
    if n != int(n):
        return False
    check = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for i in check:
        if n % i == 0:
            return False
        s = 0
        d = n-1
        while d % 2 == 0:
            d = int(d//2)
            s += 1
        for i in range(0, k):
            a = random.randint(2, n-1)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for r in range(0, s-1):
                x = pow(x, 2, n)
                if x == 1:
                    return True
                if x == n-1:
                    break
            else:
                return False
        return True
    else:
        return False

print('RabinTEST 6:', MRabintest(6, 4))
print('RabinTEST 10:', MRabintest(10, 4))
print('RabinTEST 13:', MRabintest(13, 4))
print('RabinTEST 19:', MRabintest(19, 4))

def search_prime():
    n = random.getrandbits(256)
    while MRabintest(n, 4) == False:
        print(n)
        print(MRabintest(n, 4))
        n = random.getrandbits(256)
    return n

p = search_prime()
q = search_prime()
p1 = search_prime()
q1 = search_prime()
while p*q > p1 * q1:
    p = search_prime()
    q = search_prime()
    p1 = search_prime()
    q1 = search_prime()

print('p:', p, '\nq:', q, '\np1:', p1, '\nq1:', q1)
print('check p*q < p1*q1:', p*q < p1*q1)
print('length in bits:', 'p:', p.bit_length(), 'q:', q.bit_length(), 'p1:', p1.bit_length(), 'q1:', q1.bit_length())
print('p*q bit length:', p.bit_length()+q.bit_length())

def GenerateKeyPair(p, q):
    n = p * q
    phi = (p-1)*(q-1)
    e = random.randint(2, phi-1)
    while gcd(e, phi)[0] != 1:
         e = random.randint(2, phi-1)
    d = reverse(e, phi)
    return n, e, d, phi

n, e, d, phi = GenerateKeyPair(p, q)
n1, e1, d1, phi1_n = GenerateKeyPair(p1, q1)
while n > n1:
    n, e, d, phi_n = GenerateKeyPair(p, q)
    n1, e1, d1, phi1_n = GenerateKeyPair(p1, q1)

def Encrypt(n, e, M):
    C = pow(M, e, n)
    return C

def Decrypt(C, d, n):
    M = pow(C, d, n)
    return M

def Sign(M, d, n):
    S = pow(M, d, n)
    return S

def Verify(M, S, e, n):
    return M == pow(S, e, n)

M = random.getrandbits(100)
print('\n''M:', M)

C = Encrypt(n, e, M)
print('C:', C)

M_d = Decrypt(C, d, n)
print('M_d:', M_d)

print('check M == M_d:', M == M_d)

def SendKey(k, e1, n1, d, n):
    k1 = pow(k, e1, n1)
    S = pow(k, d, n)
    S1 = pow(S, e1, n1)
    return k1, S1, S

def ReceiveKey(k1, S1, d1, n1):
    k = pow(k1, d1, n1)
    S = pow(S1, d1, n1)
    return k, S

print('\n'"A public: ", '\ne:', e, '\nn:', n, '\nd:', d, '\n\nB public:', '\ne1:', e1, '\nn1:', n1, '\nd1:', d1)

print('\ncheck n1 > n:', n1 > n)

k = random.randint(0, n)
print('k: ', k)

k1, S1, S = SendKey(k, e1, n1, d, n)
print('k1: ', k1, "\nS1: ", S1, "\nS: ", S)

k_r, S_r = ReceiveKey(k1, S1, d1, n1)
print('k_r: ', k_r, '\nS_r: ', S_r)

print('Verify:', Verify(k_r, S_r, e, n))


#code for testing the site
#m = 'i hate this site'
#m = int(m.encode().hex(), 16)
#n = '82321E2ADD8A79C826C101220A6B8CC92549A3D70E6EB5078E486AD5EC61F37B'
#e = '10001'
#e = int(e, 16)
#print(m)
#n = int(n, 16)
#
#c = Encrypt(n, e, m)
#print(c)
#c = hex(c)[2:]
#print(c)
