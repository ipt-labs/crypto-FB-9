import math, random

def num_gen(lim, lim1):
    return random.randint(lim,lim1)

def egcd(a,b):#рекурсивная евклида
    if a == 0:
        return (b, 0, 1)
    else:
        g, y ,x = egcd(b%a, a)
        return (g, x - (b//a)*y, y)

def miller_rabin_test(n):
    k = 100
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d = d // 2
    for i in range(k):
        x = num_gen(2, n - 1)
        if math.gcd(x, n) > 1:
            return False
        x = pow(x, d, n)
        if x == 1 or x == (n - 1):
            continue
        else:
            p_prime = False
            for m in range(1, s):
                x_r = x * pow(x, 2 ** m, n)
                if x_r == n - 1:
                    p_prime = True
                elif x_r == 1:
                    return False
            if not p_prime:
                return False
    return True


def inverse(a, b):
    g, x, y = egcd(a, b)#расширенный алгоритм евклида
    if g == 1:
        return x % b
    else:
        return False

def prime_gen(bit):
    min = 1 << bit
    max = (1 << bit + 1) - 1
    getnum = num_gen(min, max)
    while True:
        if getnum % 2 == 0: # isn`t prime
            getnum += 1
        elif miller_rabin_test(getnum):
            break
        else:
            getnum +=1
    return getnum

def key_generator(bit):
    e = 0
    p = prime_gen(bit)
    q = prime_gen(bit)
    print('The p is ')
    print(p)
    print('The q is ')
    print(q)
    while p == q:
        q = prime_gen(bit)
    n = p*q
    euler_n = (p-1)*(q-1)
    while math.gcd(e, euler_n) != 1:
        e = num_gen(2, euler_n - 1)
    d = inverse(e,euler_n)
    if d < 0:
        d = d + euler_n #mod
    open_key = [e,n]
    secret_key = [d,n]
    return [open_key, secret_key]


def enc(msg, open_key):
    return pow(msg,open_key[0], open_key[1]) #msg^emod(n)


def dec(enc_msg, secret_key):
    return pow(enc_msg, secret_key[0], secret_key[1]) #enc_msg^dmod(n)


def sign(msg, secret_key):
    signature = enc(msg, secret_key)
    return signature


def verification(sign, msg, open_key):
    if msg == pow(sign, open_key[0], open_key[1]):
        return True
    else:
        return False


def send(k, A_secret_key, B_open_key):
    k1 = enc(k,B_open_key)
    S = sign(k,A_secret_key)
    print ('Signature is: ', S)
    S1 = enc(S,B_open_key)
    secret_msg = [k1,S1]
    return secret_msg



def receive(secret_msg, A_open_key, B_secret_key):
    k = dec(secret_msg[0], B_secret_key)
    S = dec(secret_msg[1], B_secret_key)
    print('Starting to receive a key')
    print('The key is: ', k)
    print('Signature is: ', S)
    return verification(S,k,A_open_key)

print('Generating key pair for Alice:')
A = key_generator(256)
print('Public exponent (e) is %s' % hex(A[0][0]))
print('Private key (d) is %s:' % hex(A[1][0]))
print('Modulus is (n) is %s' % hex(A[0][1]))
print('Generating key pair for Bob:')
B = key_generator(257)
print('Public exponent (e) is %s' % hex(B[0][0]))
print('Private key (d) is %s:' % hex(B[1][0]))
print('Modulus is (n) is %s' % hex(B[0][1]))
l = num_gen(1,100000)
print('Secret message is now ', l)
enc_l = enc(l, A[0])
print('Encrypted message L is: ', enc_l)
dec_l = dec(enc_l, A[1])
print('Decrypted back message is ', dec_l )
print('Lets see how Send and Receive works: ')
k = 130
print('Shared key is: ', k)
msg = send(k, A[1], B[0])
print('Encrypted signature: ', msg[1])
print('Encrypted message: ', msg[0])
if receive(msg,A[0],B[1]):
    print('The key was successfully received')
else:
    print('Something went wrong')





