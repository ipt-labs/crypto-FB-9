import random
import math

def miller_rabbin_test(p):
    rounds = 20
    d = int(p) - 1
    s = 0
    while (d % 2 == 0):
        d >>= 1
        s += 1

    for round in range (rounds):
        x = random.randint(2, p-1)

        if (math.gcd(x, p) != 1):
            return False

        if (pow(x, d, p) == 1 or pow(x, d, p) == p - 1):
            continue
        else:
            for r in range (0, s):
                x_r = pow(x, d * (2 ** r), p)

                if (x_r == 1):
                    return False
                elif (x_r == (p - 1)):
                    break
                elif (r == s - 1):
                    return False
    return True