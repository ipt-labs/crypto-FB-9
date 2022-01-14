import random


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


#пошук оберненого
def modinv(a, mod):
    nsd, x, y = egcd(a, mod)
    if nsd != 1:
        return False
    else:
        x = (x % mod + mod) % mod
        return x



def get_numbers():
    min = 2 ** 255
    max = 2 ** 256
    while True:
        p = random.randint(min, max)
        q = random.randint(min, max)
        if isPrime(p) and isPrime(q):
            if p != q:
                break
    return p, q



def isPrime(num):
    if num % 3 == 0: return False
    if num % 5 == 0: return False
    if num % 7 == 0: return False
    if num % 11 == 0: return False
    return miller_check(num)


def miller_check(num):
    s = 0
    d = num - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    x = random.randint(2, num-1) #part 1
    if egcd(x, num)[0] != 1:
        return False
    if pow(x, d, num) == 1 or pow(x, d, num) == num-1:  #part 2
        return True
    for r in range(1, s):#part 2.1 and 2.2
        xr = pow(x, d*pow(2, r), num)
        if xr == num-1:
            return True
        if xr == 1:
            return False
    return False


def get_keys(p, q):
    n = p*q
    fi = (p-1)*(q-1)
    while True:
        e=random.randint(2, fi - 1)
        if egcd(e, fi)[0] == 1:
            break
    d=modinv(e,fi)
    return [e, n], [d, n]


def encrypt(M, pubkey):
    return pow(M, pubkey[0], pubkey[1])


def decrypt(C, privkey):
    return pow(C, privkey[0], privkey[1])


def sign(M, privkey):
    return pow(M, privkey[0], privkey[1])


def verify(message, sign, pubkey):
    return pow(sign, pubkey[0], pubkey[1]) == message


class abonent:
    def __init__(self, pub, priv):
        self.public_key = pub     # [e,n]
        self.private_key = priv     # [d,n]
        self.e1 = 0
        self.n1 = 0


    def set_pubkey(self, pubkey):
        self.e1 = pubkey[0]
        self.n1 = pubkey[1]

    def get_pubkey(self):
        return self.public_key

    def send(self, k):
        print("send:")
        print("k",k)
        k1 = encrypt(k, [self.e1,self.n1])
        print("k1",k1)
        s = sign(k, self.private_key)
        print("s", s)
        s1 = encrypt(s, [self.e1,self.n1])
        print("s1",s1)
        return k1, s1

    def receive(self, k1, s1):
        print("receive:")
        k = decrypt(k1, self.private_key)
        print("k", k)
        s = decrypt(s1, self.private_key)
        print("s", s)
        if verify(k,s,[self.e1,self.n1]):
            print(f"Verified, message is {k}")
        else:
            print(f"msg not verified {k}")
        return k, s

def check_prog():
    while True:
        p, q = get_numbers()
        p1, q1 = get_numbers()
        if p * q <= p1*q1:
            break
    a, b = (get_keys(p, q))
    A = abonent(a, b)
    a, b = (get_keys(p1, q1))
    B = abonent(a, b)
    A.set_pubkey(B.get_pubkey())
    B.set_pubkey(A.get_pubkey())
    k1, s1 = A.send(66666666666666666)
    B.receive(k1, s1)
    k1, s1 = B.send(88005553535)
    A.receive(k1, s1)




def dec_to_hex(num):
    return hex(num)[2:].upper()


def hex_to_dec(hex):
    return int(hex, 16)


def str_to_hex(str):
    string = (str.encode('utf-8'))
    return string.hex().upper()

def decode(int):
    return bytearray.fromhex(hex(int)[2:]).decode()
# check_prog()


def check():
    n1=hex_to_dec("106C5B29B8D8711D751333D7D588F29126011E7DF8914DF6EAFD64753C768683B")
    e1=hex_to_dec("10001")



    Message= hex_to_dec(str_to_hex("hello"))
    e=7032796771994420273201031421598778194937435665956783394898325588193182082569303420109052208830728362171034954768134164982152415818948226074718380483394933
    d=3113873216419636765330105410314910061196466210414014305881276061383661066780362556289756755399489206387682645756908283315685082216957963298658485859442829
    n=7200093763697323968665349512793514389526113303959597030096397715601189648332790617622648761057634175623817320734144527591594825087364291875492838893269771

    encrypted=dec_to_hex(encrypt(Message,[e,n]))
    print("encrypted", encrypted)
    decrypted=decrypt(hex_to_dec(encrypted),[d,n])
    print("decrypted", decode(decrypted))

    s = "A440107EE7450AA139F2AA975906D4C1AAB4221E830100F4708664DBCD054E8D"
    print(s)
    signature = sign(hex_to_dec(s) , [e1, n1])
    mess=hex_to_dec(str_to_hex("verify"))
    print("signature:",decode(signature))

    mess="verificationcheck"
    print(mess)
    print("modulus",dec_to_hex(n))
    print("expon", dec_to_hex(e))
    signature=sign(hex_to_dec(str_to_hex(mess)),[d,n])
    print("signature",dec_to_hex(signature))



check()