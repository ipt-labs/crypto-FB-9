from collections import Counter
import math
from sympy import mod_inverse

fileread = open("lab3.txt", encoding="utf-8").read().replace('\n',"")
topVT =["ст","но","то","на","ен"]
topShT = ['рн','ыч','нк','цз','иа']
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

def bigrindx(bigr):
    a = bigr[0]
    b = bigr[1]
    return alphabet.find(a)*31+alphabet.find(b)

def indxbigr(indx):
    return alphabet[indx//31]+alphabet[indx % 31]

def Decrypt(a, b):
    opentext = ''
    a = mod_inverse(a, 961)
    for i in range(0, len(fileread) - 1, 2):
        y = bigrindx(fileread[i] + fileread[i + 1])
        x = (a*(y - b)) % pow(31 ,2)
        opentext = opentext + indxbigr(x)
    return opentext

def check(text):
    popular=dict(Counter(text).most_common())
    if 'о' in popular and (popular['о']/len(fileread))<0.07:return 0
    if 'а' in popular and (popular['а']/len(fileread))<0.06:return 0
    if 'е' in popular and (popular['е']/len(fileread))<0.06:return 0
    if 'ф' in popular and (popular['ф']/len(fileread))>0.01:return 0
    if 'щ' in popular and (popular['щ']/len(fileread))>0.01:return 0
    if 'ь' in popular and (popular['ь']/len(fileread))>0.02:return 0
    return 1

def linear_equation(a, b, n):
    x = []
    if math.gcd(a, n) == 1:
        x.append((mod_inverse(a, n) * b) % n)
    else:
        if (b % math.gcd(a, n)) == 0:
            a1 = a/math.gcd(a, n)
            b1 = b/math.gcd(a, n)
            n1 = n/math.gcd(a, n)
            res = (mod_inverse(a1 * b1, n1)) % n1
            for i in range(math.gcd(a, n)):
                x.append(res + i * n1)
        else:
            x.append(-1)
    return x

def FindKey():
    Sht = [(alphabet.find(topShT[i][0])*31+alphabet.find(topShT[i][1])) for i in range(len(topShT))]
    Pop = [(alphabet.find(topVT[i][0])*31+alphabet.find(topVT[i][1])) for i in range(len(topVT))]

    for i in Pop:
        for j in Pop:
            for n in Sht:
                for m in Sht:
                    if i==j or n==m:
                        continue
                    for number in linear_equation(i-j, n-m, 961):
                        if number != 0: b = (n-number*i) % (961)
                        if check(Decrypt(number, b)) == 1: return Decrypt(number, b), number, b

def main():
    print("Популярные биграммы в русском языке:", topVT)
    print("Популярные биграммы в шифре:", topShT)
    decrypted, a, b = FindKey()
    print('Дешифровка:', decrypted, '\nНаши ключи', "\nа =", a, "\nb =", b)

if __name__ == "__main__":
    main()
