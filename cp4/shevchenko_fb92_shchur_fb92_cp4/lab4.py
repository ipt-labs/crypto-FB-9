import random
from random import randrange


def GetGcd(num, mod):
    if num == 0:
        return (mod, 0, 1)
    else:
        g, u, v = GetGcd(mod % num, num)
        return (g, v - (mod // num) * u, u)


def GetReverse(num, mod):
    g, u, _ = GetGcd(num, mod)
    if g == 1:
        return (u % mod + mod) % mod
    else:
        return -1


def Gorner(num, pow, mod):
    bits = format(pow, 'b')
    y = 1
    for bit in bits:
        y = (y * y) % mod
        if bit == '1':
            y = (y * num) % mod
    return y


def Test(number):
    if number % 2 == 0 or number % 3 == 0 or number % 5 == 0 or number % 7 == 0:
        return False
    for k in range(50):
        d = number - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        x = randrange(2, number - 1)
        gcd = GetGcd(x, number)[0]
        if gcd > 1:
            return False
        y = Gorner(x, d, number)
        if y == 1 or y == number - 1:
            return True
        while s > 1:
            y = Gorner(y, y, number)
            if y == 1:
                return False
            if y == -1:
                return True
            s -= 1
        return False


def GenerateRandomPrime(N = 256):
    iter = 0
    while (True):
        iter = iter + 1
        bin_str = "1"
        for i in range(N - 1):
            bit = random.randint(0, 1)
            bin_str = bin_str + str(bit)
        num = int(bin_str, 2)
        if Test(num) == True:
            return num


def GenerateRandomPairs():
    while (True):
        numbers = []
        for i in range(4):
            numbers.append(GenerateRandomPrime())
        if (numbers[0] * numbers[1] >= numbers[2] * numbers[3]):
            return numbers


def GenerateKeyPair(p, q):
    n = p * q
    f = (p - 1) * (q - 1)
    while (1):
        e = randrange(2, f)
        if (GetGcd(e, f)[0] == 1):
            break
    d = GetReverse(e, f)
    return [e, n], [d, p, q]


def Encrypt(public_key, msg):
    if msg >= 0 and msg <= public_key[1] - 1:
        return Gorner(msg, public_key[0], public_key[1])
    else:
        print('Plain message should be smaller than n-1, but bigger than 0 (0 <= M <= n-1)')
        exit(1)


def Decrypt(private_key, msg):
    return Gorner(msg, private_key[0], private_key[1] * private_key[2])


def Sign(private_key, msg):
    return Gorner(msg, private_key[0], private_key[1] * private_key[2])


def Verify(public_key, msg, signature):
    return Gorner(signature, public_key[0], public_key[1]) == msg


def Send(private_key_sender, public_key_receiver, msg):
    encrypted_msg = Encrypt(public_key_receiver, msg)
    print('\nEncrypted message:', encrypted_msg)

    signature = Sign(private_key_sender, encrypted_msg)
    print('\nSignature for encrypted message:', signature)

    return [encrypted_msg, signature]


def Receive(private_key_receiver, public_key_sender, encrypted_msg, signature):
    if Verify(public_key_sender, encrypted_msg, signature) == True:
        print('\nVerified message!')
    else:
        print('\nNot verified message!')
        exit(2)

    decrypted_msg = Decrypt(private_key_receiver, encrypted_msg)
    print('\nDecrypted message:', decrypted_msg)

    return decrypted_msg


def Main():
    p, q, p1, q1 = GenerateRandomPairs()

    print("p = ", p)
    print("q = ", q)
    print("p1 = ", p1)
    print("q1 = ", q1, '\n')

    A_public, A_private = GenerateKeyPair(p, q)
    B_public, B_private = GenerateKeyPair(p1, q1)

    print('A public key:')
    print('e =', A_public[0])
    print('n =', A_public[1])
    print('A private key:')
    print('d =', A_private[0])
    print('p =', A_private[1])
    print('q =', A_private[2])

    print('\nB public key:')
    print('e1 =', B_public[0])
    print('n1 =', B_public[1])
    print('B private key:')
    print('d1 =', B_private[0])
    print('p1 =', B_private[1])
    print('q1 =', B_private[2])

    msg = GenerateRandomPrime(443)
    print('\nPlain message:', msg)

    sent_msg = Send(A_private, B_public, msg)

    received_msg = Receive(B_private, A_public, sent_msg[0], sent_msg[1])


Main()
