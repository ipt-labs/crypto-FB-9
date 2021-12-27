import re
from collections import Counter
from itertools import permutations

grammar = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
main_mod = len(grammar)
LetterToIndex = dict(zip(grammar, range(len(grammar))))
IndexToLetter = dict(zip(range(len(grammar)), grammar))
with open("variant_08.txt", "r", encoding="utf-8") as txt:
    content = re.sub('[^а-я]+', '', txt.read().lower().replace("ё", "е").replace("ъ", "ь"))


def Bg_To_Index(bg: str) -> int:
    return LetterToIndex[bg[0]] * main_mod + LetterToIndex[bg[1]]


def Index_To_Bg(index: int) -> int:
    return IndexToLetter[(index // main_mod)] + IndexToLetter[(index % main_mod)]


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
        return 0


def ObjDec(a: int, b: int, content: str) -> str:
    dec = ""
    for bg in re.findall(r"[а-я]{2}", content):
        _Y_ = Bg_To_Index(bg)
        _X_ = (ObjObern(a, main_mod ** 2) * (_Y_ - b)) % (main_mod ** 2)
        dec += Index_To_Bg(_X_)
    return dec


def ObjScan(content: str) -> int:
    if (content.count('а') / len(content)) < 0.07 or (content.count('о') / len(content)) < 0.1:
        return 0
    else:
        return 1


def ObjLinear(x1: int, x2: int, mod_: int) -> int:
    gcd, x, y = ObjGcd(x1, mod_)
    if gcd == 1:
        return ((ObjObern(x1, mod_)) * x2) % mod_
    elif gcd > 1:
        if x2 % gcd != 0:
            return 0
        else:
            a_1 = x1 / gcd
            b_1 = x2 / gcd
            n_1 = mod_ / gcd
            x__0 = ObjLinear(a_1, b_1, n_1)
            return x__0


def ObjTop(content: str) -> list:
    result = Counter(content[idx: idx + 2]
                     for idx in range(0, len(content) - 1, 2)).most_common(5)
    return list(dict(result))


def ObjFindKeys(content: str) -> list:
    obj_rus_top = []
    obj_myfile_top = []
    for bg in ObjTop(content):
        obj_myfile_top.append(Bg_To_Index(bg))
    for bg in ['ст', 'но', 'то', 'на', 'ен']:
        obj_rus_top.append(Bg_To_Index(bg))
    obj_list_x = list(permutations(obj_rus_top, 2))
    obj_list_y = list(permutations(obj_myfile_top, 2))

    for y in obj_list_y:
        Y_ = (y[0] - y[1]) % (main_mod ** 2)
        for x in obj_list_x:
            X_ = (x[0] - x[1]) % (main_mod ** 2)
            a = ObjLinear(X_, Y_, main_mod ** 2)
            if a != -1:
                b = (y[0] - a * x[0]) % (main_mod ** 2)
                if ObjScan(ObjDec(a, b, content)) == 1:
                    return [a, b]


print(ObjFindKeys(content))
# with open("Finally_08.txt", "w+", encoding="utf-8") as txt:
#     txt.write(ObjDec(ObjFindKeys(content)[0], ObjFindKeys(content)[1], content))
