from math import gcd

def euclidean_algorithm(a, b):
    if (a==0):
        return b,0,1

    r = b % a
    d, q, r = euclidean_algorithm(r, a)
    return d, r - (b//a) * q, q

def reverse_element(a, n):
    if (gcd(a, n) == 1):
        temp = euclidean_algorithm(a, n)[1]
        element = temp % n
        return element
    else:
        return 0

def modular_solution(a, b, n):
    if (gcd(a, n) == 1):
        x = reverse_element(a, n) * b
        return x % n
    elif (b % gcd(a, n) != 0):
        return 0
    elif (b % gcd(a, n) == 0):
        d = gcd(a, n)
        x = modular_solution(int(a/d), int(b/d), int(n/d))
        return x