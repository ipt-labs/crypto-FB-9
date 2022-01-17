from sympy import mod_inverse
import random
a = pow(2,256)

def Prime(n, k=4):
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
        p = Prime(n)
        if p is not False:break
    return p

def generate_pq():
    p, q = generate_key(a), generate_key(a)
    p1, q1 = generate_key(a), generate_key(a)
    while p * q > p1 * q1:
        p, q = generate_key(a), generate_key(a)
        p1, q1 = generate_key(a), generate_key(a)
    return p, q, p1, q1

def generete_key_pair(p,q):
    e = (2**16)+1
    n=p*q
    fi=(p-1)*(q-1)
    d=mod_inverse(e,fi)
    return [e,n], [d,p,q]

encrypt = lambda M, en: pow(M, en[0], en[1])

decrypt = lambda C, dpq: pow(C, dpq[0], dpq[1]*dpq[2])

def sign(M, secret, open1):
    C=encrypt(M, [secret[0], secret[1]*secret[2]])
    C1=encrypt(M, open1)
    S1=encrypt(C, open1)
    return [C1, S1]


def verify(Messege, open, secret1):
    M=decrypt(Messege[0], secret1)
    C=decrypt(Messege[1], secret1)
    k=encrypt(C,open)
    return [M, M==k]

sendkey = lambda M, secret, open1: sign(M, secret, open1)

receivekey = lambda signed, open, secret1: verify(signed, open, secret1)

def main():
    p, q, p1, q1 = generate_pq()
    print("P * Q", p * q, "\nP1 * Q1", p1 * q1)
    open, secret = generete_key_pair(p, q)
    open1, secret1 = generete_key_pair(p1, q1)
    M = random.randint(0, 2 ** 256)
    print('Ваше сообщение:', M)
    C = sendkey(M, secret, open1)
    print("C1:", C[0])
    print("S1:", C[1])
    P = receivekey(C, open, secret1)
    print("Получено:", P[0])
    print("Подтвержденно? -", P[1])
    open_test=["10001","85918D25C824C820D8A82F4256BCD88170971F9D2108D1B1280BA40F4094AF5D"]
    print("Open key",open_test)
    open_test[0],open_test[1]=int(open_test[0], 16),int(open_test[1], 16)
    M_test="hochueshku"
    print("Message '"+ M_test+"'")
    M_test = int(M_test.encode().hex(), 16)
    C_test=encrypt(M_test,open_test)
    print("Ciphertext",hex(C_test)[2:])
    sign="36337E1F0B1CEBDC4BCE8A39073AF2A3252236BC211594C32755861FAE1BF539"
    sign=int(sign, 16)
    print("sign is", M_test==encrypt(sign, open_test))
if __name__ == "__main__":
    main()