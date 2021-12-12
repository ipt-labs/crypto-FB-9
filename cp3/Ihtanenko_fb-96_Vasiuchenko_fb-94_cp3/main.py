import pandas as pd
import itertools
from collections import Counter

def gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcd(b, a % b)
        return d, y, x - y * (a // b)


def opp_element(a, mod):
    return gcd(a, mod)[1] % mod


def bigram(text):
    bg = []
    for j in range(0, len(text), 2):
        bg.append(text[j] + text[j+1])
    return bg


def freq_bg(bg):
    bg_2 = []
    for j in range(0, len(text) - 2, 2):
        bg_2.append(text[j] + text[j+1])
    bg_2_count = dict(Counter(bg_2))
    fr_bg_2 = {f: bg_2_count[f] / len(bg_2) for f in bg_2_count}
    return fr_bg_2

text = open(r"D:\Python stuff\Lab3_Crypta\variants\02.txt").read()
text = text.replace("\n", "")
bg = bigram(text)
fr_bg = freq_bg(bg)

dataframe = pd.DataFrame.from_dict(fr_bg, 'index').stack().reset_index(level=0)
print(dataframe.columns)
dataframe = dataframe.sort_values(by=0, ascending=False)
dataframe = dataframe.rename(columns={'level_0': 'Bigram', 0: 'Frequency'})
dataframe = dataframe.reset_index(inplace=False).drop(columns=['index'])
tt_bigrams = list(dataframe['Bigram'].head())
print(tt_bigrams)

print(dataframe.head())

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
            'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']

d = dict(zip(alphabet, list(r for r in range(0, len(alphabet)))))

def transposition(bg, mod, d):
    v = d[bg[0]] * mod + d[bg[1]]
    return v % mod ** 2


def a_value(X1, Y1, X2, Y2, mod):
    div_x = X1 - X2
    div_y = (Y1 - Y2)
    a_obr = div_x * opp_element(div_y, mod ** 2) % mod ** 2
    if a_obr != 'infinity' and a_obr != None:
        return opp_element(a_obr, (mod ** 2))
    else:
        return None


def b_value(y, x, a, mod):
    if a!= None:
        b = (y - a * x) % (mod ** 2)
        return b
    else:
        return None


def get_key(d, transposition):
    for k, v in d.items():
        if v == transposition:
            return k


def decode(bg, a, b, mod, d):
    x = []
    plaintext = []
    for y in bg:
        x.append(((transposition(y, mod, d) - b) * opp_element(a, mod ** 2)) % (mod ** 2))
    for i in range(0, len(x)):
        plaintext.append(get_key(d, x[i] // mod))
        plaintext.append(get_key(d, x[i] - (x[i] // mod) * mod))
    return plaintext

ru_bigrams =  ['ст', 'но', 'то', 'на', 'ен']
tt_bigrams

x = []
y = []
for i in range(0, len(tt_bigrams)):
    #print
    y.append(transposition(tt_bigrams[i], len(alphabet), d))
for i in range(0, len(ru_bigrams)):
    x.append(transposition(ru_bigrams[i], len(alphabet), d))

xy = list(itertools.product(x, y))
x1y1x2y2 = list(itertools.product(xy, xy))

ab = []
for xy in x1y1x2y2:
    #print(xy[0][0],xy[0][1],xy[1][0],xy[1][1])
    a = a_value(xy[0][0], xy[0][1], xy[1][0], xy[1][1], len(alphabet))
    b = b_value(xy[0][1], xy[0][0], a, len(alphabet))
    ab.append([a, b])
    #print(a, b)

plaintext = []
i = 0
for i in range(0, len(ab)):
    a = ab[i][0]
    b = ab[i][1]
    if a != None and b != None and a != 0:
        plaintext.append(''.join(decode(bg, a, b, len(alphabet), d)))
        if(plaintext[len(plaintext)-1][:6] == 'однако'):
            print(a, b)
            print(i)


def filter(text):
    if text[0] == 'ы' or text[0] == 'ь':
        return False
    vowels = ['о', 'а', 'е', 'и', 'у', 'ы']
    tacit = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м',
             'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    round = 0
    for i in range(0, 50):
        if text[i] == 'ь' and (text[i+1] in vowels or text[i-1] in vowels):
            return False
        if text[i] == text[i+1] and text[i+1] == text[i+2]:
            return False
        if text[i] in tacit and text[i+1] in tacit and text[i+2] in tacit and text[i+3] in tacit and text[i+4] in tacit:
            return False
        if text[i] in tacit and text[i+1] in tacit and text[i+2] in tacit and text[i+3] in tacit:
            round += 1
            if round == 4:
                return False
    return True

ab[169]

for i in range(0, len(plaintext)):
    if(filter(plaintext[i])):
        print(i)
        print(plaintext[i], '\n')