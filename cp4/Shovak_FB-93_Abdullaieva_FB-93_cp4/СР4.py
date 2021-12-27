from random import randrange
from math import gcd

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def print_():
    print(
        '+------------------------------------------------------------------------------------------------------------------------------------------------------------------+')


def euclid_ext(a, n):
    if n == 0:
        return a, 1, 0
    else:
        gcd1, x, y = euclid_ext(n, a % n)
        return gcd1, y, x - y * (a // n)


def miller_rabin(num):
    if num % 2 == 0 or num % 3 == 0 or num % 5 == 0 or num % 7 == 0:
        return False
    d = num - 1
    s = 0
    while d % 2 == 0:
        d = d // 2
        s += 1
    x = randrange(2, num)
    if gcd(x, num) > 1:
        return False
    x = pow(x, d, num)
    if x == 1 or x == num-1:
        return True
    for r in range(1, s-1):
        x = pow(x, 2, num)
        if x == num-1:
            return True
        if x == 1:
            return False
    return False


def gen_number(bit):
    num = (randrange(1 << bit - 1, 1 << bit) << 1) + 1
    if miller_rabin(num):
        return num
    else:
        num = gen_number(bit)
        return num


def gen_pairs():
    p, q, p1, q1 = gen_number(256), gen_number(256), gen_number(256), gen_number(256)
    while p*q > p1*q1:
        p, q, p1, q1 = gen_number(256), gen_number(256), gen_number(256), gen_number(256)
    return p, q, p1, q1


def GenerateKeyPairs(p, q):
    n = p * q
    fi = (p - 1) * (q - 1)
    e = randrange(2, fi)
    while gcd(e, fi) != 1:
        e = randrange(2, fi)
    gcd1, x, y = euclid_ext(e, fi)
    d = (x % n + n) % n
    return [n, e], [d, p, q]


def Encrypt(m, e, n):
    return pow(m, e, n)


def Decrypt(c, d, n):
    return pow(c, d, n)


def Sign(m, d, n):
    return pow(m, d, n)


def Verify(s, m, e, n):
    return pow(s, e, n) == m


def SendKey(k, e1, d, n1, n):
    print(f'{k = }')
    k1 = Encrypt(k, e1, n1)
    S = Sign(k, d, n)
    print(f'{S = }')
    S1 = Encrypt(S, e1, n1)
    print(f'{k1 = }\n{S1 = }')
    print_()
    return k1, S1


def ReceiveKey(k1, S1, e, d1, n1, n):
    k = Decrypt(k1, d1, n1)
    S = Decrypt(S1, d1, n1)
    print(f'{k = }\n{S = }')
    if Verify(S, k, e, n):
        print('message =', k)
        print('True')
    else:
        print('False')


def int_message():
    m = input('Enter your message: ')
    msg = (m.encode('utf-8'))
    msg = int(msg.hex().upper(), 16)
    return msg


def Abonent(p, q, p1, q1):
    print_()
    # A
    public_key, secret_key = GenerateKeyPairs(p, q)
    print(f'Subscriber A:\nn = {public_key[0]}\ne = {public_key[1]}\nd = {secret_key[0]}')
    # B
    public_key1, secret_key1 = GenerateKeyPairs(p1, q1)
    print(f'Subscriber B:\nn = {public_key1[0]}\ne = {public_key1[1]}\nd = {secret_key1[0]}')
    print_()

    message = 1234567890
    k1, S1 = SendKey(message, public_key1[1], secret_key[0], public_key1[0], public_key[0])
    ReceiveKey(k1, S1, public_key[1], secret_key1[0], public_key1[0], public_key[0])
    print_()
    # A
    message = int_message()
    print(f'Message in int view: {message}')
    mass_m = Encrypt(message, public_key[1], public_key[0])
    mass_d = Decrypt(mass_m, secret_key[0], public_key[0])
    msg = bytearray.fromhex(hex(mass_d)[2:]).decode()
    mass_s = Sign(message, secret_key[0], public_key[0])
    mass_v = Verify(mass_s, message, public_key[1], public_key[0])
    print('\nDecrypted message: ', mass_m, '\nEncrypted message: ', msg, '\nSignature: ', mass_s, '\nVerify: ', mass_v)
    print_()

    # B
    message = int_message()
    print(f'Message in int view: {message}')
    mass_m = Encrypt(message, public_key1[1], public_key1[0])
    mass_d = Decrypt(mass_m, secret_key1[0], public_key1[0])
    msg = bytearray.fromhex(hex(mass_d)[2:]).decode()
    mass_s = Sign(message, secret_key1[0], public_key1[0])
    mass_v = Verify(mass_s, message, public_key1[1], public_key1[0])
    print('\nDecrypted message: ', mass_m, '\nEncrypted message: ', msg, '\nSignature: ', mass_s, '\nVerify: ', mass_v)
    print_()


def verify_site_decrypt(hex_e, hex_n):
    demical_modulus = int(hex_n, 16)
    demical_public_exp = int(hex_e, 16)

    msg = int_message()

    hex_msg = hex(Encrypt(msg, demical_public_exp, demical_modulus))[2:].upper()
    return msg, demical_modulus, demical_public_exp, hex_msg


def verify_site_encrypt(e, n):
    msg = int_message()

    hex_n = hex(n)[2:].upper()
    hex_e = hex(e)[2:].upper()

    int_msg = Encrypt(msg, e, n)
    hex_msg = hex(int_msg)[2:].upper()

    return n, e, msg, hex_n, hex_e, hex_msg


def verify_site_sign(hex_e, hex_n, sign):
    demical_modulus = int(hex_n, 16)
    demical_public_exp = int(hex_e, 16)
    demical_sign = int(sign, 16)

    msg = int_message()

    verify = Verify(demical_sign, msg, demical_public_exp, demical_modulus)
    return demical_sign, verify


def verify_site():
    n = 26926241708254230750854269802663410683614241967803392343391714558069148660657297567725587527019155847453318380702729440108740406105001132973539649039020941
    e = 3447106746698012025419049284054744624256176074688828758450551104112792733671823379375983820638599560339162371553404418774232621294608078706964222078268753

    modulus = 'E65C98C1045DF67E947B6BFE3D1D3F3C0094DCD4073323DB4417F605C0E602EF'
    public_exp = '10001'
    signature = 'D000E36E74573F425D64C57C05B515B7CA428A62ED0DD52068B11BC8FC8D9E0D'

    msg1, demical_modulus, demical_public_exp, hex_msg1 = verify_site_decrypt(public_exp, modulus)

    print(f'\n{modulus = }\n{public_exp = }\n{demical_modulus = }\n{demical_public_exp = }')
    print_()
    print(f'Check decryption:\n{msg1 = }\n{hex_msg1 = }')

    print_()
    n, e, ms2, hex_n, hex_e, hex_msg2 = verify_site_encrypt(e, n)
    print(f'Check encryption:\n{n = }\n{e = }\n\n{hex_n = }\n{hex_e = }\n{hex_msg2 = }')

    print_()
    demical_sign, verify = verify_site_sign(public_exp, modulus, signature)
    print(f'Check verification:\n{signature = }\n{demical_sign = }\n{verify = }')
    print_()


if __name__ == '__main__':
    p = 165072043642971037485092457927589701746574998402252816184199736300212458995791
    q = 163118121724427938370395279090619557931144758547815711445975313577132727671651
    p1 = 188875449300751845152394052405139439236103778592153906038817785928665975130443
    q1 = 196346415693867814691019089530626563612968221509038801445814889435600142247623
    Abonent(p, q, p1, q1)
    verify_site()
    # p, q, p1, q1 = gen_pairs()
    # print_()
    # print(f'{p = }\n{q = }\n{p1 = }\n{q1 = }')






