import random
from math import gcd
from cp3.tishkov_papucha_fb_93_cp3.lab3 import gcd_ext
from cp3.tishkov_papucha_fb_93_cp3.lab3 import calc_reverse_by_mod
from cp2.Tishkov_Papucha_FB_93_cp2.Lab2 import VigenereCypherModule

rus_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']

default_interval_pair = [(2**255)+1, (2**256)-1]


def int_to_hex(number):
    return hex(number)[2:].upper()


def hex_to_int(hex_value):
    return int(hex_value, 16)


def encode_to_hex(string):
    string = (string.encode('utf-8'))
    return string.hex().upper()


def decode_from_hex(hex_value):
    return bytes.fromhex(hex_value).decode('utf-8')


def gen_random_prime_num(min_interval=default_interval_pair[0], max_interval=default_interval_pair[1]):
    while True:
        random_num = random.randint(min_interval, max_interval)
        if is_prime(random_num):
            return random_num


def is_prime(num):
    if num % 2 == 0 or num % 3 == 0 or num % 5 == 0 or num % 7 == 0:
        return False
    else:
        return miller_rabin(num)


def miller_rabin(num):
    d, s = num - 1, 0
    while d % 2 == 0:
        d = d // 2
        s += 1
    a = random.randint(2, num-1)
    x = pow(a, d, num)
    if x == 1 or x == num-1:
        return True
    while s > 1:
        x = pow(x, x, num)
        if x == 1:
            return False
        if x == -1:
            return True
        s -= 1
    return False


class RSA:
    def __init__(self, name, verbose=True):
        self.vigenere = VigenereCypherModule(rus_alphabet)
        self.private_keys = dict()
        self.public_keys = dict()
        self.encryption_key = None
        self.name = name
        self.verbose = verbose

    def f_n(self):
        p = self.private_keys['p']
        q = self.private_keys['q']
        res = (p - 1) * (q - 1)
        return res

    def generate_keys(self):
        p = gen_random_prime_num()
        q = gen_random_prime_num()
        self.private_keys.update({'p': p, 'q': q})
        n = p * q
        self.public_keys.update({'n': n})
        phi = self.f_n()
        e = gen_random_prime_num(2, phi - 1)
        d = calc_reverse_by_mod(e, phi)
        self.public_keys.update({'e': e})
        self.private_keys.update({'d': d})
        if self.verbose:
            print("Generate " + self.name + "'s private keys: ")
            print("p: \n" + str(p))
            print("q: \n" + str(q))
            print("d: \n" + str(d))
            print("Generate " + self.name + "'s public keys: ")
            print("e: \n" + str(e))
            print("n: \n" + str(n))
        return self.public_keys

    def encrypt(self, msg):
        return pow(msg, self.public_keys['e'], self.public_keys['n'])

    def decrypt(self, msg):
        d = self.private_keys['d']
        p = self.private_keys['p']
        q = self.private_keys['q']
        return pow(msg, d, p*q)

    def set_encryption_key(self, new_key):
        self.encryption_key = new_key

    def get_encryption_key(self):
        return self.encryption_key

    def generate_auth_msg(self, e1, n1):
        key = self.get_encryption_key()
        d = self.private_keys['d']
        n = self.public_keys['n']
        k1 = pow(key, e1, n1)
        s = pow(key, d, n)
        s1 = pow(s, e1, n1)
        # print(self.name + " generate sign (s): \n" + str(int_to_hex(s)))
        if self.verbose:
            print(self.name + "'s key message: " + str(key))
            print(self.name + " generate sign (s): \n" + str(s))
            print(self.name + " generate k1: \n" + str(k1))
            print(self.name + " generate s1: \n" + str(s1))
            print(self.name + " return s1, k1")
        return s1, k1

    def generate_auth_response(self, s1, k1):
        d = self.private_keys['d']
        n = self.public_keys['n']
        check_s = pow(s1, d, n)
        check_key = pow(k1, d, n)
        if self.verbose:
            print(self.name + " earn s1: \n" + str(s1))
            print(self.name + " earn k1: \n" + str(k1))
            print(self.name + " generate s: \n" + str(check_s))
            print(self.name + " generate key: \n" + str(check_key))
            print(self.name + " return s")
        return check_s, check_key

    def check_auth_response(self, check_s, check_k):
        key = self.get_encryption_key()
        d = self.private_keys['d']
        n = self.public_keys['n']
        s = pow(key, d, n)
        if self.verbose:
            print(self.name + " checks (s) from other abonent")
        if s != check_s:
            print("Authentication failed!")
            return False
        print("Authentication success!")
        print("Key is " + str(self.encrypt(s)))
        return s

    def generate_key_by_response(self, s, e, n):
        key = pow(s, e, n)
        self.set_encryption_key(key)
        print(key)


def rsa_test():
    server_e = hex_to_int('10001')
    server_n = hex_to_int('B14A1D5BFC441D0A0FFB804CA478C2DF46E6ECCF09A8C83A0EAEE047FB81694D')
    abonent_a = RSA('Alice', False)
    abonent_b = RSA('Server', False)
    abonent_b.public_keys.update({'e': server_e})
    abonent_b.public_keys.update({'n': server_n})
    a_public_keys = abonent_a.generate_keys()
    print("A - e: ")
    print(int_to_hex(a_public_keys['e']))
    print("A - n: ")
    print(int_to_hex(a_public_keys['n']))
    msg = "Hello world!"
    enc_msg = abonent_a.encrypt(hex_to_int(encode_to_hex(msg)))
    print("Msg = " + msg)
    print("Encrypted msg: ")
    print(int_to_hex(enc_msg))
    server_msg = "Hello server!"
    enc_server_msg = abonent_b.encrypt(hex_to_int(encode_to_hex(server_msg)))
    print("Message for website = " + server_msg)
    print("Encrypted msg: ")
    print(int_to_hex(enc_server_msg))

    print("Generate sign:")
    origin_msg = hex_to_int(encode_to_hex('My sign'))
    abonent_a.set_encryption_key(origin_msg)
    abonent_a.generate_auth_msg(server_e, server_n)


def main():
    abonent_a = RSA('Alice')
    abonent_b = RSA('Bob')
    a_public_keys = abonent_a.generate_keys()
    b_public_keys = abonent_b.generate_keys()
    e_a = a_public_keys['e']
    e_b = b_public_keys['e']
    n_a = a_public_keys['n']
    n_b = b_public_keys['n']
    abonent_a.set_encryption_key(20)
    auth_msg = abonent_a.generate_auth_msg(e_b, n_b)
    auth_response = abonent_b.generate_auth_response(auth_msg[0], auth_msg[1])
    abonent_a.check_auth_response(auth_response[0], auth_response[1])


if __name__ == '__main__':
    main()
