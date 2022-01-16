from math import gcd
from random import randint
import logging
log=logging.getLogger("from rsa_tools")

k = 1000
min_value_of_key = 2 ** 256 - 1
e_by_default = 2 ** 16 + 1
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def decompose(a: int):
    a = a - 1
    str_bin = str(bin(a))
    S = len(str_bin) - str_bin.rfind('1') - 1
    d = a // (2 ** S)
    return d, S


def quick_pow(base: int, pow2: int, mod: int):
    pow1 = list(str(bin(pow2 % mod)))
    pow=pow1[2:]
    y = 1
    for i in map(int, pow):
        y = (y ** 2) % mod
        y = (y * base ** i) % mod
    return y


def is_prime_by_basis(number: int, basis: int, d, S):
    xd = quick_pow(basis, d, number)
    if xd == 1 or xd == number - 1:
        return True
    else:
        xr = quick_pow(basis, d * 2, number)
        for r in range(1, S):
            if xr == number - 1:
                return True
            elif xr == 1:
                return False
            xr = quick_pow(xr, 2, number)


def test_miller_rabin(p: int):
    d, S = decompose(p)
    for i in range(k):
        x = randint(2, p - 1)
        if gcd(x, p) > 1:
            return False
        if not is_prime_by_basis(p, x, d, S):
            return False
    return True


def random_prime(from_num: int, to_num: int):
    cnt = 0
    if from_num > to_num:
        raise AssertionError(f"The range from {from_num} to {to_num} does not exist")
    for x in range(from_num,to_num+1):
        x = randint(from_num, to_num)
        if x % 2 == 0:
            m0 = x + 1
        else:
            m0 = x
        for i in range(m0, to_num + 1, 2):
            c = False
            for j in primes:
                if i % j == 0: break
            else:
                c = True
            if c and test_miller_rabin(i):
                log.debug(f'There was {cnt} retry')
                return i
            log.debug(f"Candidate {i} is not suitable")
            cnt+=1

    raise ArithmeticError(f"There are no prime numbers in range from {from_num} to {to_num}")


def reverse_element(a: int, b: int):
    k= euclid_ext(a, b)[1]
    if k==1:
        raise ArithmeticError(f"There are no revers element for number {a} by module {b}")
    else:
        return (k+b)%b


def euclid_ext(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = euclid_ext(b, a % b)
        return d, y, x - y * (a // b)


def generate_key(subscriber: str):
    if subscriber == 'A':
        p = random_prime(min_value_of_key, 2 * min_value_of_key - 2)
        q = random_prime(2 * min_value_of_key - 1, 4 * min_value_of_key - 4)
    else:
        p = random_prime(4 * min_value_of_key - 3, 8 * min_value_of_key - 8)
        q = random_prime(8 * min_value_of_key - 7, 16 * min_value_of_key - 16)
    n = p * q
    oyler_f = (p - 1) * (q - 1)
    if gcd(e_by_default, oyler_f) == 1:
        e = e_by_default
    else:
        for i in range(oyler_f // 2 - 2, oyler_f - 1):
            if gcd(i, oyler_f) == 1:
                e=i
                break
    d = reverse_element(e, oyler_f)
    log.info(f'Key data for subscriber {subscriber}:\n\t p={p}\n\t q={q}\n\t n={n}\n\t oyler_f={oyler_f}\n\t e={e}\n\t d={d}')
    return (e, n), d


def encrypt(key: tuple, M: int):
    return quick_pow(M, *key)


def decrypt(privat_key: int, public_key: tuple, C: int):
    return quick_pow(C,privat_key,public_key[1])


def get_sign(privat_key: int, public_key: tuple, M: int):
    return quick_pow(M,privat_key,public_key[1])


def verify_sign(public_key: tuple, M: int, S: int):
    return M == quick_pow(S, *public_key)


class Subscriber:
    def __init__(self, name:str, public_key:tuple, privat_key:int):
        self.name=name
        self.privat_key=privat_key
        self.public_key=public_key
        self.comrade_public_key=None

    def get_public_key(self):
        return self.public_key

    def set_public_key_of_comrade(self, comrade_public_key:tuple):
        self.comrade_public_key = comrade_public_key

    def send_key(self,k:int):
        k1=encrypt(self.comrade_public_key,k)
        S=get_sign(self.privat_key, self.public_key, k)
        S1=encrypt(self.comrade_public_key, S)
        log.info(f'Subscriber {self.name} has encrypted k:\n\t S={S}\n\t k1={k1}\n\t S1={S1}')
        return k1, S1

    def receive_key(self, k1:int, S1:int):
        k=decrypt(self.privat_key,self.public_key,k1)
        S=decrypt(self.privat_key,self.public_key,S1)
        log.info(f'Subscriber {self.name} has decrypted k1 and S1:\n\t k={k}\n\t S={S}\n\t S1={S1}')
        return verify_sign(self.comrade_public_key,k,S)