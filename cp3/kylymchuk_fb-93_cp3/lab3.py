from collections import Counter
import math

with open("text.txt") as file:
    f = file.read()

alph = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
popbig = ["ст", "но", "то", "на", "ен"]

bigram = []
for i in range(0, len(f)-1, 2):
    bigram.append(f[i]+f[i+1])

mcbig = []
for i in range(0, 5):
    mcbig.append(Counter(bigram).most_common(5)[i][0])

def verify(text):
    entr = 0
    for i in Counter(text):
        p = Counter(text)[i] / len(text)
        entr -= p*math.log(p, 2)
    if 4.3 < entr < 4.5:
        print("текст змістовний")
        return 1
    else:
        print("текст не є змістовним")
        return 0

def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a+b

def reverse(a, b):
    if a == 1:
        return 1
    for u in range(0, b):
        for v in range(-500, 0):
            if a*u+b*v == 1:
                return u

def euclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = euclid(b, a % b)
        return d, y, x - y * (a // b)

def euclidreverse(a, b):
    x = euclid(a, b)[1]
    return x % b

def decrypt(a, b):
    text=[]
    for i in range(0, len(bigram)):
        y=alph.index(bigram[i][0])*31+alph.index(bigram[i][1])
        x=(euclidreverse(a, 961)*(y-b))%961
        text.append(alph[x//31])
        text.append(alph[x%31])
    return("".join(text))

def findkey(xb1, yb1, xb2, yb2):
    X1=alph.index(xb1[0])*31+alph.index(xb1[1])
    Y1=alph.index(yb1[0])*31+alph.index(yb1[1])
    X2=alph.index(xb2[0])*31+alph.index(xb2[1])
    Y2=alph.index(yb2[0])*31+alph.index(yb2[1])
    a=[]
    for i in range(0, 961):
        if (Y1-Y2)%961 == (i*(X1-X2))%961:
            a.append(i)
    for i in a:
        b=(Y1-i*X1)%961
        print("a=", a[a.index(i)], "b=", b)

print(decrypt(703, 956))