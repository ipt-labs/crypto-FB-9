from collections import Counter
import math
file = open("03.txt", encoding="utf-8")
fileread = file.read().replace('\n',"")
popularbigram =["ст","но","то","на","ен"]
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
lenf=len(fileread)
def Bigram(text):
    bigram=[]
    for i in range(0,len(text) - 1,2):
        bigram.append(text[i] + text[i + 1])
    return bigram

def Bigram_counter(arr):
    count = Counter(arr)
    return count

def PopularBigramShT(arr):
    popularbigramsht=[]
    a = arr.most_common(5)
    for i in range(5):
        popularbigramsht.append(a[i][0])
    return popularbigramsht

def IndexLetters(arr):
    indexlet =[]
    for i in range(len(arr)):
        indexlet.append((alphabet.find(arr[i][0])*len(alphabet)+alphabet.find(arr[i][1])))
    return indexlet

# обернений елемент
def ReElement(elem):
    mod = pow(len(alphabet),2)
    if math.gcd(elem, mod) == 1:
        for x in range(0, mod - 1):
            ans = (elem * x) % mod
            if ans == 1:
                return x
    else:
        return 0
def bigr_to_indx(bigr):
    a=bigr[0]
    b=bigr[1]
    return alphabet.find(a)*31+alphabet.find(b)

def indx_to_bigr(indx):
    return alphabet[indx//31]+alphabet[indx%31]

def Decrypt(a,b):
    opentext=''
    a = ReElement(a)
    for i in range(0, len(fileread) - 1, 2):
        y = bigr_to_indx(fileread[i] + fileread[i + 1])
        x = (a*(y - b)) % pow(len(alphabet),2)
        opentext = opentext + indx_to_bigr(x)
    return opentext

def check(text):
    popular=dict(Counter(text).most_common())
    if 'о' in popular and (popular['о']/lenf)<0.07:return 0
    if 'а' in popular and (popular['а']/lenf)<0.06:return 0
    if 'е' in popular and (popular['е']/lenf)<0.06:return 0
    if 'ф' in popular and (popular['ф']/lenf)>0.01:return 0
    if 'щ' in popular and (popular['щ']/lenf)>0.01:return 0
    if 'ь' in popular and (popular['ь']/lenf)>0.02:return 0
    return 1

def FindKey():
    bigrSht = IndexLetters(PopularBigramShT(Bigram_counter(Bigram(fileread))))
    bigrPop = IndexLetters(popularbigram)
    for i in bigrPop:
        for j in bigrPop:
            for n in bigrSht:
                for m in bigrSht:
                    if i==j or n==m:
                        continue
                    a=int(ReElement(i-j)*(n-m))%(31**2)
                    if a!=0:
                        b=(n-a*i)%(31**2)
                        if check(Decrypt(a, b)) == 1: return Decrypt(a , b) , a , b

print("Popularni bigrami",popularbigram)
print("Popularni bigrami shifru",PopularBigramShT(Bigram_counter(Bigram(fileread))))
# a = (y-Y**)((x-x**)^-1)mod(m^2)
decrypted,a,b=FindKey()
print('Rozwifrovka\n',decrypted,'\nwith keys\n',a,b)