import random
from math import gcd

min = pow(2, 255) + 1
max = pow(2, 256) - 1
def toInt(txt):
    return int(txt.encode('utf-8').hex(), 16)

def toText(txt):
    return bytes.fromhex(hex(txt)[2:]).decode('ASCII')

def MillerRabin(n, k=100):
    primes = [2, 3, 5, 7, 11]
    r = 0
    s = n - 1
    if n == 2:
        return True

    if 0 in list(map(lambda x: n % x, primes)):
        return False

    while s % 2 == 0:
        r += 1
        s //= 2

    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:

            return False
    return True

def rand():
    p = random.randrange(min, max)
    while not MillerRabin(p):
        p = random.randrange(min, max)
    return p

def RSA(p, q):
    n = p * q
    e = random.randrange(2, (p - 1) * (q - 1))
    while gcd(e, (p - 1) * (q - 1)) != 1:
        e = random.randrange(2, (p - 1) * (q - 1))
    d = pow(e, -1, (p - 1) * (q - 1))
    prKey = (d, p, q)
    opKey = (n, e)
    return prKey, opKey

def Encrypt(message, n, e):
    p = pow(message, e, n)
    return p

def Decrypt(encrMsg, d, p, q):
    p = pow(encrMsg, d, p * q)
    return p

def Signature(message, d, p, q):
    p = pow(message, d, p * q)
    return p

def SignVer(message, sign, opKey):
    n, e = opKey
    if pow(sign, e, n) != message:
        return False
    else:
        return True


def Send(message, opKey, prKey):
    n, e = opKey
    d, p, q = prKey
    encrMessage = Encrypt(message, n, e)
    sign = Signature(message, d, p, q)
    return encrMessage, sign


def recieveMessage(encrMsg, sign, opKey, prKey):
    n, e = opKey
    d, p, q = prKey
    sms = Decrypt(encrMsg, d, p, q)
    if SignVer(sms, sign, opKey):
        return sms
    else:
        return 1


text = "130"
print('Message: ', text)
message = toInt(text)
p = rand()
q = rand()
p1 = rand()
q1 = rand()
while p * q > p1 * q1:
    p = rand()
    q = rand()
rsaOne, rsaTwo = RSA(p, q), RSA(p1, q1)
encryptSms, sign = Send(message, rsaTwo[1], rsaOne[0])
print('encryptMessage: ',encryptSms, '\nsignature: ',sign, '\nsended...\n')
message = recieveMessage(encryptSms, sign, rsaOne[1], rsaTwo[0])
print(message)
txt = toText(message)
print('We get: ',txt)

def intHex(num):
    return hex(num)[2:].upper()
def hexInt(hexxx):
    return int(hexxx, 16)


def check():
    print("\nCheck function\n")
    text = 130
    modulus = '369B87290493AC8520954BAF362A50B85'
    exponent = '10001'
    n = int("369B87290493AC8520954BAF362A50B85", 16)
    e = int("10001", 16)
    pair = [n, e]
    enc = Encrypt(text, n, e)
    sign = int("028D891DAC58AC06D4322D7FD6330AFDEF", 16)
    vert = SignVer(text, sign, pair)
    print('Message: ', text)
    print('mod = ', n)
    print('exp = ', e)
    print('Encrypted: ', enc)
    print('Signature: ', sign)
    print('SignVer: ', vert)


check()