import re
from collections import Counter
import math
alphabet = ('а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц','ч','ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я')

popbigr = ('ст', 'но', 'то', 'на', 'ен')
dict = {}
keylist = []
m = 31


def openfile(file):
    text = open(file, 'r', encoding='utf-8')
    text = text.read().replace('\n', '')
    result_file = open("filtered.txt", 'w', encoding='utf-8')
    result_file.write(text)
    result_file = open("filtered.txt", 'r', encoding='utf-8')
    return result_file.read()


def bigrams(filteretext):
    finaldic = []
    bigram = re.findall(r'([а-яА-Я]{2})', filteretext)
    bigram.sort()
    for i in Counter(bigram):
        result_file = open("filtered.txt", 'r', encoding='utf-8')
        n = result_file.read().count(i) / m
        dict[i] = str(round(n, 7))
    sort_orders = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    j = 0
    for i in sort_orders:
        if j != 5:
            finaldic.append(i[0])
        else:
            break
        j += 1
    return finaldic


def posiblek(massiv, massiv1):
    for i in massiv:
        for j in massiv:
            for k in massiv1:
                for n in massiv1:
                    if i == j:
                        continue
                    if k == m:
                        continue
                    else: keygenerator(i, j, k, n)


def keygenerator(x1, x2, y1, y2):
    X1 = alphabet.index(x1[0]) * m + alphabet.index(x1[1])
    X2 = alphabet.index(x2[0]) * m + alphabet.index(x2[1])
    Y1 = alphabet.index(y1[0]) * m + alphabet.index(y1[1])
    Y2 = alphabet.index(y2[0]) * m + alphabet.index(y2[1])
    XX = (X1 - X2) % (m ** 2)
    YY = (Y1 - Y2) % (m ** 2)
    a = (obernene(XX, m ** 2) * YY) % (m ** 2)
    b = (Y1 - a * X1) % (m ** 2)
    nod = math.gcd(XX, m ** 2)
    if nod > 1:
        if YY % nod == 0:
            a = (obernene(XX, (m ** 2) // nod) * YY) % (m ** 2 // nod)
            while a < m ** 2:
                b = (Y1 - a * X1) % (m ** 2)
                tuplekeys = (a, b)
                keylist.append(tuplekeys)
                a += (m ** 2) // nod
            return keylist
        if YY % nod != 0:
                tuplekeys = (a, b)
                keylist.append(tuplekeys)
                return keylist

    else:
        a = (obernene(XX, m ** 2) * YY) % (m ** 2)
        b = (Y1 - a * X1) % (m ** 2)
        tuplekeys = (a, b)
        keylist.append(tuplekeys)
        return keylist


def obernene(a, mod):
    a %= mod
    for x in range(1, mod):
        if ((a * x) % mod == 1): return x
    return 1


def analiz(text):
    o = e = a = 0
    ok = 0
    for i in text:
        if 'о' in i:
            o += 1
        if 'е' in i:
            e += 1
        if 'а' in i:
            a += 1
    ao = o / len(text)
    ae = e / len(text)
    aa = a / len(text)
    if ao > 0.1:
        ok += 1
    if ae > 0.08:
        ok += 1
    if aa > 0.07:
        ok += 1
    if ok > 2:
        return True
    else:
        return False


def decript(keyslist, name_of_text):
    text = open(name_of_text, "r", encoding="utf8")
    text = text.read()
    textlen = len(text)
    buff_text = ''
    for a, b in keyslist:
        for i in range(0, textlen, 2):
            y = alphabet.index(text[i]) * m + alphabet.index(text[i + 1])
            x = (obernene(a, m ** 2) * (y - b)) % (m ** 2)
            x = alphabet[x // m] + alphabet[x % m]
            buff_text += x
        if analiz(buff_text):
            global bigr
            print("- - - - - - - - - - - - - - \n" + "Text bigrams: " + str(bigr) + "\n" + "(" + str(a) + " , " + str(
                b) + ")" + " key was aproved!\n" + "Decoded Text:" + "\n" + buff_text)
            break
        else:
            print("(" + str(a) + " , " + str(b) + ")" + " key was NOT aproved!")
        buff_text = ''


file = openfile("var3.txt")
bigr = bigrams(file)
posiblek(popbigr, bigr)
decript(keylist, "filtered.txt")