from collections import Counter
import operator
file = open("var3.txt", encoding="utf-8")
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
fileread = file.read().replace('\n',"")

def linear_equation(a, b, n):
    d = gcd(a, n)
    rev_a = revers(a, n)
    x = []
    if d == 1:
        x.append((rev_a * b) % n)
    else:
        if (b % d) == 0:
            a1 = a/d
            b1 = b/d
            n1 = n/d
            res = (revers(a1 * b1, n1)) % n1
            for i in range(d):
                x.append(res + i * n1)
    return x

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def revers(elem, mod):
    if gcd(elem, mod) == 1:
        for x in range(0, mod - 1):
            ans = (elem * x) % mod
            if ans == 1:
                return x
    else:
        return 0


def get_ngram_freq(string, n=2, step=1):
    grams = Counter([string[i:i + n] for i in range(0, len(string) - n + 1, step)])
    size = sum(grams.values())
    grams = dict(((gram, grams[gram] / size) for gram in grams))
    return list(dict(sorted(grams.items(), key=operator.itemgetter(1), reverse=True)))


def decription(a, b):
    opentext = ''
    for i in range(0, len(fileread) - 1, 2):
        bi=(a * (alphabet.find(fileread[i]) * 31 + alphabet.find(fileread[i + 1]) - b)) % (len(alphabet)**2)
        opentext += alphabet[bi//31]+alphabet[bi % 31]
    return opentext



def check(text):
    if 'о' not in get_ngram_freq(text, 1)[0:7]:
        return False
    if 'е' not in get_ngram_freq(text, 1)[0:7]:
        return False
    if 'а' not in get_ngram_freq(text, 1)[0:7]:
        return False
    if 'ст' not in get_ngram_freq(text)[0:7]:
        return False
    if 'но' not in get_ngram_freq(text)[0:7]:
        return False
    else:
        return True


def FindKey():
    for i in range(5):
        for j in range(5):
            for n in range(5):
                for m in range(5):
                    if i==j or n==m:
                        continue

                    x=alphabet.find(pop_bigr_from_language[i][0]) * len(alphabet) + alphabet.find(pop_bigr_from_language[i][1])
                    y=alphabet.find(pop_bigr_from_language[j][0]) * len(alphabet) + alphabet.find(pop_bigr_from_language[j][1])
                    z=alphabet.find(pop[n][0]) * len(alphabet) + alphabet.find(pop[n][1])
                    d=alphabet.find(pop[m][0]) * len(alphabet) + alphabet.find(pop[m][1])
                    a=linear_equation(x-y, z-d, 31**2)
                    for numer in a:
                        if numer != -1:
                            b = (z-numer*x) % (31**2)
                            if check(decription(revers(numer, 31 ** 2), b)): return decription(revers(numer, 31 ** 2), b), numer, b

pop_bigr_from_language=["ст","но","то","на","ен"]
pop=get_ngram_freq(fileread)[0:5]
print("Популярні біграми російської мови:")
print(pop_bigr_from_language)
print("Найчастіші біграми нашого шифротексту:")
print (pop)

decrypted,a,b=FindKey()
print('Текст розшифрований цими ключами\n',a,b,'\nСам текст має такий вигляд',decrypted)