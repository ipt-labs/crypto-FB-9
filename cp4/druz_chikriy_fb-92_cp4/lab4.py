from random import randrange
import random

def gcd(a, b, u0=1, v0=0, u1=0, v1=1):
    result = []
    r1 = 0
    r2 = 0
    if a >= b:
        r1 = a
        r2 = b
    else:
        r1 = b
        r2 = a
    if r2 == 0:
        return [0, 0, 0]
    r3 = int(r1 % r2)
    q = int(r1 / r2)
    u3 = u0 - q * u1
    v3 = v0 - q * v1
    if r3 == 0:
        return (r2, u1, v1)
    result = gcd(r2, r3, u0=u1, v0=v1, u1=u3, v1=v3)
    if a > b:
        return result
    else:
        return (result[0], result[2], result[1])


def pow_mod(number, power, mod):
    bitArray = "{0:b}".format(power)
    y = 1
    i = 0
    while i < len(bitArray):
        y = (y ** 2) % mod
        if bitArray[i] == "1":
            y *= number
            y %= mod
        i += 1
    return y


def millerRabbinTest(testedNumber):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for prime in primes:
        if testedNumber % prime == 0:
            return False

    k = 0
    while k < 100:
        d = testedNumber - 1
        s = 0

        while d % 2==0:
            d //= 2
            s += 1

        x = randrange(2, testedNumber - 1)

        if gcd(x, testedNumber)[0] > 1:
            return False

        xPowD = pow_mod(x, d, testedNumber)
        if xPowD == 1:
            return True
        elif xPowD == testedNumber - 1:
            return True

        xPow2 = xPowD

        r = 1
        while r < s:
            xPow2 = pow_mod(xPow2, xPow2, testedNumber)
            if xPow2 == 1:
                return False
            if xPow2 == -1:
                return True
            r += 1
        k += 1
    return False


def genPrime():
    min = 57896044618658097711785492504343953926634992332820282019728792003956564819968  # min 256 bit number
    max = 115792089237316195423570985008687907853269984665640564039457584007913129639935  # max 256 bit number

    prime = randrange(min, max)

    while not millerRabbinTest(prime):
        prime = randrange(min, max)

    return prime


def genQuartet():
    p = genPrime()
    q = genPrime()
    q1 = genPrime()
    p1 = genPrime()

    if (p * q) <= (p1 * q1):
        return [p, q, q1, p1]
    else:
        return genQuartet()


def genPair(p, q):
    n = p * q
    fi = (p - 1) * (q - 1)
    while "Beskonechnost":
        e = randrange(2, fi)
        if gcd(e, fi)[0] == 1:
            break
    d = gcd(e, fi)[1]
    if d < 0:
        d += fi
    return [[e, n], [d, p, q]]


def encrypt(pub_key, message):
    e = pub_key[0]
    n = pub_key[1]

    if message < 0:
        print("message under zero error")
        return -1
    elif message >= n:
        print("too many info, hard to remember")
        return -1

    return pow_mod(message, e, n)


def decrypt(secret_key, message):
    d = secret_key[0]
    p = secret_key[1]
    q = secret_key[2]

    return pow_mod(message, d, p * q)


def sign(secret_key, message):
    d = secret_key[0]
    p = secret_key[1]
    q = secret_key[2]

    return pow_mod(message, d, p * q)


def verify(pub_key, message, sign):
    e = pub_key[0]
    n = pub_key[1]

    if pow_mod(sign, e, n) == message:
        return True

    return False


##
# PRK - private key
# PK - public key
##


def send(sendersPRK, receiversPK, message):
    encrypted = encrypt(receiversPK, message)
    signature = sign(sendersPRK, encrypted)
    print("\nEncrypted:", encrypted, "\nSigned:", signature)

    return [encrypted, signature]


def receive(receiverPRK, sendersPK, encrypted, signature):
    print("Checking...")
    if verify(sendersPK, encrypted, signature):
        print("Look`s like original")
    else:
        print("Message is made in prc")  # Made in PRC == Made in china == fake
        # exit()

    decrypted = decrypt(receiverPRK, encrypted)
    print("Got message:", decrypted)

    return decrypted


def sendKey(sendersPRK, receiversPK, k):
    e1 = receiversPK[0]
    n1 = receiversPK[1]
    d = sendersPRK[0]
    p = sendersPRK[1]
    q = sendersPRK[2]
    k1 = pow_mod(k, e1, n1)
    S = pow_mod(k, d, p*q)
    S1 = pow_mod(S, e1, n1)
    return [k1, S1]


def receiveKey(receiverPRK, sendersPK, key):
    e = sendersPK[0]
    n = sendersPK[1]
    d1 = receiverPRK[0]
    p1 = receiverPRK[1]
    q1 = receiverPRK[2]
    k1 = key[0]
    S1 = key[1]
    k = pow_mod(k1, d1, p1*q1)
    S = pow_mod(S1, d1, p1*q1)
    if pow_mod(S,e,n) == k:
        print("Authentification success")
    else:
        print("Authentification fail")
        exit()


# quarted = genQuartet()
# FirstDudeKeys = genPair(quarted[0], quarted[1])
# SecondDudeKeys = genPair(quarted[3], quarted[2])
# print("Data:\n" + "Sender Public Key: e =",FirstDudeKeys[0][0],"n =", FirstDudeKeys[0][1], "\nSender Secret Key: d =", FirstDudeKeys[1][0], "p =",FirstDudeKeys[1][1],"q =",FirstDudeKeys[1][2])
# print("Data:\n" + "Receiver Public Key: e =",SecondDudeKeys[0][0],"n =", SecondDudeKeys[0][1], "\nReceiver Secret Key: d =", SecondDudeKeys[1][0], "p =",SecondDudeKeys[1][1],"q =",SecondDudeKeys[1][2])
# message = randrange(0, FirstDudeKeys[0][1])
# print("Generated message:",message)
# print("Authentification...")
# k = randrange(1, FirstDudeKeys[0][1]) 
# print("Authentification key", k)
# sendedkey = sendKey(FirstDudeKeys[1], SecondDudeKeys[0], k)
# receiveKey(SecondDudeKeys[1], FirstDudeKeys[0], sendedkey)
# sended = send(FirstDudeKeys[1], SecondDudeKeys[0], message)
# received = receive(SecondDudeKeys[1], FirstDudeKeys[0], sended[0], sended[1])
n = int("D35913665679F190F20040892336193A61BD6767FE1E97085EAB0DB2A52517C7",16)
e = int("10001",16)
print("Public keys: n=", n, "e =", e)
message = 53
print("Message in hex:", hex(message)[2:])
encrypted = encrypt((e, n), message)
# signature = sign()
print("Encrypted message:", hex(encrypted)[2:])
print("Signature:", int("22BB6DD8F9E6C8EEEB73B19388F8B51811815109B12A2F86A042E6722938D33B", 16))
print("Verifycation:", verify((e, n), message, int("22BB6DD8F9E6C8EEEB73B19388F8B51811815109B12A2F86A042E6722938D33B", 16)))
