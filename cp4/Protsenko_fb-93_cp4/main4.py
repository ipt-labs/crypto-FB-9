import random
from random import getrandbits, randrange

length = 256


def ObjMillerRabin(n: int, k=128) -> bool:
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def ObjGeneratePrimeCandidate(size: int) -> int:
    p = getrandbits(size)
    p |= (1 << size - 1) | 1
    return p


def ObjGeneratePrimeNumber(size: int) -> int:
    p = 4
    while not ObjMillerRabin(p, 128):
        p = ObjGeneratePrimeCandidate(size)
    return p


def ObjGcd(a1: int, a2: int) -> tuple:
    if a1 == 0:
        return a2, 0, 1
    else:
        objgcd, x, y = ObjGcd(a2 % a1, a1)
        return objgcd, y - (a2 // a1) * x, x


def ObjObern(a1: int, mod_: int) -> int:
    objgcd, x, y = ObjGcd(a1, mod_)
    if objgcd == 1:
        return (x % mod_ + mod_) % mod_
    else:
        return -1


def ObjGeneratePairs() -> tuple:
    p, q, p_1, q_1 = ObjGeneratePrimeNumber(length), ObjGeneratePrimeNumber(length), ObjGeneratePrimeNumber(
        length), ObjGeneratePrimeNumber(length)
    while p * q > p_1 * q_1:
        print("{red}p_1 >>> {endcolor}".format(red='\033[91m', endcolor='\033[0m'), p_1)
        print("{red}q_1 >>> {endcolor}".format(red='\033[91m', endcolor='\033[0m'), q_1)
        p, q, p_1, q_1 = ObjGeneratePrimeNumber(length), ObjGeneratePrimeNumber(length), ObjGeneratePrimeNumber(length), ObjGeneratePrimeNumber(length)
    return p, q, p_1, q_1


def ObjGenerateKeyPairs(p: int, q: int) -> tuple:
    n = p * q
    φ_n = (p - 1) * (q - 1)
    while 1:
        e = random.randrange(2, φ_n)
        if ObjGcd(e, φ_n)[0] == 1:
            break
    d = ObjObern(e, φ_n)
    return [e, n], [d, p, q]


def ObjVerify(commonKey: int, info_int: int, indication: int) -> int:
    return pow(indication, commonKey[0], commonKey[1]) == info_int


def ObjSend(personalKeySender: int, commonKeyReceiver: int, info_int: int) -> list:
    encryptedinfo_int = ObjEncrypt(info_int, commonKeyReceiver)
    print(f"\nEncrypted info >>> {ObjEncrypt(info_int, commonKeyReceiver)}")
    indication = ObjSign(encryptedinfo_int, personalKeySender)
    print(f"\nIndication for encrypted info >>> {indication}")
    return [encryptedinfo_int, indication]


def ObjEncrypt(info_int: int, commonKey: int) -> int:
    return pow(info_int, commonKey[0], commonKey[1])


def ObjDecrypt(info_int: int, personalKey: int) -> int:
    return pow(info_int, personalKey[0], personalKey[1] * personalKey[2])


def ObjSign(info_int: int, personalKey: int) -> int:
    return pow(info_int, personalKey[0], personalKey[1] * personalKey[2])


def ObjReceive(personalKeyReceiver: int, commonKeySender: int, encryptedinfo_int: int, indication: int) -> int:
    if ObjVerify(commonKeySender, encryptedinfo_int, indication):
        print("\n{blue}The numbers is verified{endcolor}".format(blue='\033[96m', endcolor='\033[0m'))
        print(f"\nDecrypted info >>> {ObjDecrypt(encryptedinfo_int, personalKeyReceiver)}")
        return 0
    else:
        print("\n{red}The numbers is not verified{endcolor}".format(red='\033[91m', endcolor='\033[0m'))
        exit(0)


if __name__ == '__main__':
    p, q, p_1, q_1 = ObjGeneratePairs()
    Comm_A_, Pers_A_ = ObjGenerateKeyPairs(p, q)
    Comm_B_, Pers_B_ = ObjGenerateKeyPairs(p_1, q_1)

    print("\n{blue}(A) personal key >>>{endcolor}".format(blue='\033[96m', endcolor='\033[0m'))
    print(f"d >>> {Pers_A_[0]}")
    print(f"p >>> {Pers_A_[1]}")
    print(f"q >>> {Pers_A_[2]}")
    print("\n{blue}(A) common key >>>{endcolor}".format(blue='\033[96m', endcolor='\033[0m'))
    print(f"e >>> {Comm_A_[0]}")
    print(f"n >>> {Comm_A_[1]}")

    print("\n{blue}(B) personal key >>>{endcolor}".format(blue='\033[96m', endcolor='\033[0m'))
    print(f"d_1 >>> {Pers_B_[0]}")
    print(f"p_1 >>> {Pers_B_[1]}")
    print(f"q_1 >>> {Pers_B_[2]}")
    print("\n{blue}(B) common key >>>{endcolor}".format(blue='\033[96m', endcolor='\033[0m'))
    print(f"e_1 >>> {Comm_B_[0]}")
    print(f"n_1 >>> {Comm_B_[1]}")

    info_int = ObjGeneratePrimeNumber(400)
    print(f"\nPlain numbers >>> {info_int}")
    transfer_info_int = ObjSend(Pers_A_, Comm_B_, info_int)
    received_info_int = ObjReceive(Pers_B_, Comm_A_, transfer_info_int[0], transfer_info_int[1])


