import random
from math import gcd
from cp3.tishkov_papucha_fb_93_cp3.lab3 import gcd_ext
from cp3.tishkov_papucha_fb_93_cp3.lab3 import calc_reverse_by_mod

default_interval_pair = [(2**255)+1, (2**256)-1]


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


def main():
    print(gen_random_prime_num())


if __name__ == '__main__':
    main()