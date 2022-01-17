import random

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


def miller_rabin(n):
    for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
        if n % prime == 0:
            return False
    s = 0
    d = n - 1
    while d % 2 == 0:
        d = d // 2
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(4):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True

def generate_num():
    while True:
        n = random.randint(2**256,(2**256)*10)
        if miller_rabin(n) is not False:
            break
    return n

def generator():
    p=q = 1
    p1= q1 = 0
    while p * q > p1 * q1:
        p, q = generate_num(), generate_num()
        p1, q1 = generate_num(), generate_num()
    return p,q,p1,q1

def generate_keys(p,q):
    n=p*q
    e = 65537
    d=find_mod_inv(e, (p-1)*(q-1))
    return [e,n], [d,n]

def encrypt(M, open):
    C=pow(M, open[0], open[1])
    return C


def decryption(C, secret):
    M = pow(C, secret[0], secret[1])
    return M

def sign(M, secret, open):
    C=encrypt(M, [secret[0], secret[1]])
    return [encrypt(M, open), encrypt(C, open)  ]


def verify(Messege, open, secret1):
    M=decryption(Messege[0], secret1)
    return [M, M==encrypt(decryption(Messege[1], secret1),open)]


def sendkey(M, secret, open1):
    return sign(M, secret, open1)


def receivekey(signed, open, secret1):
    return verify(signed, open, secret1)



def task():
    p, q, p1, q1 = generator()
    print('Змінна p:' , p ,'\nЗмінна q:' ,q,'\nЗмінна p1:' ,p1,'\nЗмінна q1:' ,q1)
    open_key, secret_key=generate_keys(p,q)
    print("open",open_key,"\nsecret",secret_key)
    open_key1, secret_key1=generate_keys(p1,q1)
    M=random.randint(0,2**128)
    print("Our massage",M)
    C = sendkey(M, secret_key, open_key1)
    print("Cipher",C[0],"\nSign",C[1])
    received=receivekey(C, open_key, secret_key1)
    print("Massage is",received[1], "\nAnd its", received[0])


def test():
    test_key=["10001","813694966BAE83447E40BF3B6684C2B687BA142E624FE812A86A1FB2E9935A8B"]
    print("Open key",test_key)
    test_key[0],test_key[1]=int(test_key[0], 16),int(test_key[1], 16)
    M_test="ciphertext"
    print("Message '"+ M_test+"'")
    M_test = int(M_test.encode().hex(), 16)
    C_test=encrypt(M_test,test_key)
    print("Ciphertext",hex(C_test)[2:])
    sign="0EC7D6E4E6770E70A7D181F25A4A0FCF1FFB2C5223B957D0BD30264EF27C858D"
    sign=int(sign, 16)
    print("sign is", M_test==encrypt(sign, test_key))

#task()
test()
