import random
from array import *
def find_random_number(num1,num2):
    random_num = random.randint(num1, num2)
    return random_num

min = 57896044618658097711785492504343953926634992332820282019728792003956564819968 + 1   #2^255 + 1 
max = 115792089237316195423570985008687907853269984665640564039457584007913129639936 - 1  #2^256 - 1 
#print(a)
def check_simple(num):
    prime_number = [2, 3, 5, 7, 11, 13, 17]
    for prime in prime_number:
        if num % prime == 0:
            return 0
        else:
            return 1
#print(check_simple(341))
def s_d(number):
    s = 0
    number_1 = number-1
    d = number_1
    while (number_1)%2 == 0:
        s = s + 1
        number_1 = number_1 // 2

    for i  in range(s):
        d = d // 2
    return s,d
#print(s_d(341))   
def gcd(a,b):
    c = b
    t = 0
    while c != 0:
        t = c
        c = b % a
        b = a
        a = c
    return t

#print(gcd(34,341))
"""
mass = array('i', [])
def binary_form(binary):
    a = binary
    b = 0
    i = 0 
    while binary != 1:
        b = a % 2
        mass.insert(0, b)
        binary = a // 2
        a = binary
        i += 1
    mass.insert(0, 1)
    return mass
"""
def pow(x,d,mod):
    c = 1
    while (d != 0):
        if ((d % 2) == 1):
            c = (c * x) % mod
            d = d // 2
            x = (x * x) % mod
        else:
            d = d // 2
            x = (x * x) % mod
    return c
#print(pow(5,85,341))
def miller_rabin_test(p):
    pr = 0
    if check_simple(p) == 1:
        for k in range(100):
            x = random.randint(1, p)
            g = gcd(x,p)
            if g == 1:
                sd = s_d(p)
                s = sd[0]
                d = sd[1]
                if pow(x,d,p) == 1:
                    return 1
                else:
                    for i in range(1,s - 1):
                        hor = pow(x,d*(2 ** i),p)
                        if hor == p - 1:
                            return  1
                        else:
                            pr = 0
            else:
                pr = 0
    else:
        pr = 0
    return pr


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x) 
# x = mulinv(b) mod n, (x * b) % n == 1
def obrat(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

#print(miller_rabin_test(341))
def Key_Pair():
    n = 1
    while n > 0:
        p = find_random_number(min,max)
        if miller_rabin_test(p) == 1:
            break

    return p   
def Key():
    p = Key_Pair()
    q = Key_Pair()
    i = 1
    while i > 0:
        p1 = Key_Pair()
        q1 = Key_Pair()
        if p*q <= p1*q1:
            break
    return p,q,p1,q1 

def  GenerateKeyPair(p,q):
    n = p*q
    func = (p - 1)*(q - 1)
    i = 1
    while i > 0:
        e = random.randint(2, func - 1)
        if gcd(e,func) == 1:
            break
    d = obrat(e,func)
    return e,n,d

def Encrypt(A,text):
    e = A[0]
    n = A[1]
    M = pow(text,e,n)
    return M

def Decrypt(key_s,text):
    d = key_s[0]
    p = key_s[1]
    q = key_s[2]
    n = p*q
    M = pow(text,d,n)
    return M

def Sign(key_s,text):
    d = key_s[0]
    p = key_s[1]
    q = key_s[2]
    n = p*q
    S = pow(text,d,n)
    return S

def Verify(key_p,text,S):
    e = key_p[0]
    n = key_p[1]
    M = pow(S,e,n)
    if M == text:
        return 1
    else:
        return 0
def  SendKey(B,key_s,k):
    k1 = pow(k,B[0],B[1])
    n = key_s[1] * key_s[2]
    S = pow(k,key_s[0],n)
    S1 = pow(S,B[0],B[1])
    return k1,S1

def  ReceiveKey(A,key_s,sendkey):
    n = key_s[1] * key_s[2]
    k = pow(sendkey[0],key_s[0],n)
    S = pow(sendkey[1],key_s[0],n)
    Auth = pow(S,A[0],A[1])
    if Auth == k:
        return print("Аутентификация прошла успешно !!!")
    else:
        return print("!!! Не прошло аутентификацию !!!")

def create_signature(A,key_s_A,text):
    encrypt_text = Encrypt(A,text)
    sign_text = Sign(key_s_A,encrypt_text)
    return encrypt_text,sign_text

def check_signature(A,encrypt_text,sign_text,key_s_A):
    vr = Verify(A,encrypt_text,sign_text)
    if vr == 1:
        print("Текст прошел верификацию !")
    else:
        print("!!! Текст не прошел верификацию !!!")
    decrypt_text = Decrypt(key_s_A,encrypt_text)
    return decrypt_text
# Простые числа для создания ключей абонентов А и В
pq = Key()
p = pq[0]
q = pq[1]
p1 = pq[2]
q1 = pq[3]

print("Числа для создания ключей для абонента А: \n", "p =", p, "\n q =",q)
print("\nЧисла для создания ключей для абонента B: \n", "p1 =", p1, "\n q1 =",q1)

# Сохраняем открытые ключи (e,n) и секретный (b)
A = GenerateKeyPair(p,q)
print("\nОткрытые ключи абонента А: \n", "e =", A[0], "\n n =",A[1])
print("Секретный ключ абонента А: \n", "d =", A[2])

B = GenerateKeyPair(p1,q1)
print("\nОткрытые ключи абонента B: \n", "e =", B[0], "\n n =",B[1])
print("Секретный ключ абонента B: \n", "d =", B[2])

k = random.randint(1, A[1])
print("\nСекретное значение :\n k =",k)

text =  random.randint(0, A[1])
print("\nСообщение :\n ", text, "\n")

key_s_A = [A[2],p,q]
key_p_A = [A[0],A[1]]
key_s_B = [B[2],p1,q1]
send_key = SendKey(B,key_s_A,k)
ReceiveKey(A,key_s_B,send_key)
c_s = create_signature(A,key_s_A,text)
ch = check_signature(A,c_s[0],c_s[1],key_s_A)
print("\nЗашифрованное сообщение : \n", c_s[0])
print("\nДешифрованное сообщение : \n", ch)
"""
modulus = int("9E21D3EE327D4BED841861611393BDED",16)
exponent = int("10001",16)
print("Открытые ключи абонента c сайта: \n", "e =", exponent, "\n n =", modulus)
text = 49 
print("Сообщение в 16-ричной системе :\n",31)
A = [exponent,modulus]
encrypt_text = Encrypt(A,text)
print("Зашифрованное сообщение :\n", encrypt_text)
sign_text = int("5D0789F1303C49FCFF3227C28D985B8F",16)
print("Цифровая подпись :\n", sign_text)
vr = Verify(A,text,sign_text)
print("Верификация :\n", vr)
B = GenerateKeyPair(p1,q1)
key_s_B = [B[2],p1,q1]
k = random.randint(1, A[1])
send_key = SendKey(A,key_s_B,k)
print("moduls = ", B[1])
print("exponent = ", B[0])
print("\nSignature : ",send_key)
"""