from random import randint


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def miller_rabin(p):
    k = 50
    d = p - 1
    s = 0
    while d % 2 ==0:
        d//=2
        s+=1
    for _ in range(k):
        a = randint(2, p - 1)
        if gcd(a, p) > 1:
            return False
        x = pow(a, d, p)
        if x == 1 or x == p - 1:
            continue
        for _ in range(1, s):
            x = pow(x, 2, p)
            if x == 1:
                return False
            if x == p-1:
                break
        return False
    return True


def prime(length):
    n0 = 2**(length-1)
    n1 = 2**length - 1
    # print("prime from ", n0, " to ", n1)
    x = randint(n0, n1)
    if x % 2 == 0:
        x += 1
    while not miller_rabin(x):
        x += 2
    return x


def generator(len):
    p = prime(len)
    q = prime(len)
    e = pow(2, 16) + 1
    if p == q:
        q = prime(len)
    n = q * p
    fi_n = (p - 1) * (q - 1)
    while gcd(fi_n, e) != 1:
        e = randint(3, fi_n - 1)
    d = pow(e, -1, fi_n)
    open_key = e, n
    secret_key = d, n
    return open_key, secret_key


def encrypt(m, open_key):
    return pow(m, open_key[0], open_key[1])


def decrypt(c, secret_key):
    return pow(c, secret_key[0], secret_key[1])


def sign(m, secret_key):
    return encrypt(m, secret_key)


def verification(sign, msg, open_key):
    if msg == pow(sign, open_key[0], open_key[1]):
        return True
    else:
        return False


def send_key(k, A_sec, B_op):
    k1 = encrypt(k, B_op)
    s = sign(k, A_sec)
    print("Signature: ", s)
    S1 = encrypt(s, B_op)
    print("Encrypt Signature: ", S1)
    secret_msg = [k1, S1]
    return secret_msg


def receive_key(secret_msg, A_open_key, B_secret_key):
    k = decrypt(secret_msg[0], B_secret_key)
    S = decrypt(secret_msg[1], B_secret_key)
    return verification(S, k, A_open_key), k, S


def main():
    while True:
        A = generator(256)
        B = generator(256)
        if A[0][1] <= B[0][1]:
            break

    print("A")
    print("e", (A[0][0]))
    print("d", (A[1][0]))
    print("n", (A[0][1]))

    print("B")
    print("e", (B[0][0]))
    print("d", (B[1][0]))
    print("n", (B[0][1]))

    msg = prime(256)
    print("Open text: ", msg)
    send = send_key(msg,A[1],B[0])
    print("Encrypted msg: ", send[0])
    # print("Signature: ", send[1])
    receive = receive_key(send, A[0], B[1])
    print("Decrypted msg: ", receive[1])
    print("Decrypted sign: ", receive[2])
    print("Verification: ", receive[0])


def server_test():
    modulus = "D2358B0795616D393B67C1151715CC2C06F1FF53AEC760286AA1F49369139E67"
    exponent = "10001"
    open_text =[exponent, modulus]
    print("e - ", open_text[0])
    print("n - ", open_text[1])
    open_text[0] = int(open_text[0], 16)
    open_text[1] = int(open_text[1],16)
    msg = "abobus"
    print("Message ", msg)
    m = int(msg.encode().hex(),16)
    c = encrypt(m, open_text)
    print("Ciphertext", hex(c)[2:].upper())
    sign = "9F3F0F0315391B91E6A266AE6526126ABA590E8537F0571D06F83AF51E6A9FEF"
    sign = int(sign, 16)
    print("Sign - ", hex(sign)[2:].upper())
    print("Sign is", verification(sign, m, open_text))


main()
print("----------------------------------------------------------------------------------------------------------------"
      "------------------------------------------------------------")
print("----------------------------------------------------------------------------------------------------------------"
      "------------------------------------------------------------")
server_test()


