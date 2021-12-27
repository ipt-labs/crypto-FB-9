from array import *
from math import *
from collections import Counter
from operator import itemgetter
import itertools

 
#file_source = "file1_Source.txt"
#file_encrypted = "file2_Encrypted.txt"
file_decrypted = "file2_Decrypted.txt"
file_encrypted = "04.txt"

         # 0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30
Alphabet=['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ь','ы','э','ю','я']
FrequentBigramsPlainText = ['ст', 'но', 'то', 'на', 'ен']
banedBigrams = [ "аь", "уь", "оь", "еь", "иь", "ыь", "эь", "юь", "яь", "йь", "ьы", "ьь", "жы", "шы", "щы" ]


#AlphabetBigrams = []
#for i in range(len(Alphabet)):
#    for j in range(len(Alphabet)):
#        AlphabetBigrams.append(Alphabet[i]+Alphabet[j])
#print()


# тут переводим часто встречаемые биграммы открытого текста в числа
IndexFrequentBigramsPlainText = []
for i in range(len(FrequentBigramsPlainText)):
    x1 = 0
    x2 = 0
    for j in range (len(Alphabet)):
        for k in range(2):
            if FrequentBigramsPlainText[i][k] == Alphabet[j]:
                if k == 0:
                    x1 = j
                else:
                    x2 = j
    x = x1*len(Alphabet)+x2
    IndexFrequentBigramsPlainText.append(x)


########  убираем буквы, которых нет в алфавите #########
def filterText(text):
    string = text.lower()
    string = text.replace('ё', 'е')
    ssting = text.replace('ъ', 'ь')
    letters = []
    for char in string:
        if char not in Alphabet:
           char = ''
        else:
            letters.append(char)
    return ''.join(letters)


####  убираем повторяющиеся буквы ####
def deleteRepeatedElements(arr):
    noRepeatedElementsInArr = []
    noRepeatedElementsInSet = set()
    for char in arr:
        noRepeatedElementsInSet.add(char)
    for char in noRepeatedElementsInSet:
        noRepeatedElementsInArr.append(char)
    return noRepeatedElementsInArr



                                        ### Задание №1 ####
                         #### Поиск обратного элемента | Линейные сравнения ###

def gcd(a, b):
    if(b == 0):
        return a
    return gcd(b, a%b)

arrQ = []
def AlgorithmEuclida(mod, a):

    if mod == 0:
        return
    a = a%mod
    if a == 0:
        return

    c = mod%a
    d = mod/a

    if c == 1:
        #print(mod, " = ", int(d), "*" , a, " + ", c)
        arrQ.append(int(d))
        return arrQ
    else:
        #print(mod, " = ", int(d), "*" , a, " + ", c)
        arrQ.append(int(d))
        AlgorithmEuclida(a,c)
    return arrQ


def FindInvertedElement(arrQ, mod, a):

    if gcd(a, mod) != 1:
        print("Обратного элемента не существует!")
        return

    a = a%mod
    if a == 1:
        #print("Обернений елемент: ", 1)
        return 1
    else:
        x = 1
        y = 0
        q = 0

        if arrQ == None:
            return

        for i in range(len(arrQ)):
            q = x * (-arrQ[i]) + y
            y = x
            x = q

        invertedElement = q
        if invertedElement < 0:
            invertedElement = (mod + invertedElement)
        #print("Обернений елемент: ", invertedElement)
        arrQ.clear()
        return invertedElement

def LinearCompare(a, b, n):
    rootOfEquation = []
    d = gcd(n, a)
    if d == 1:
        x = FindInvertedElement(AlgorithmEuclida(n, a), n, a)*b%n
        rootOfEquation.append(x)
        return rootOfEquation
        #print(a, "*", x, " = ", b, "mod", n)
    elif d > 1:
        if b%d != 0:
           # print("Коренів нема")
            return
        else:
            #print("Кількість коренів: ", d)
            a1 = a/d
            b1 = b/d
            n1 = n/d
            if AlgorithmEuclida(n1, a1) == None:
                return
            x = FindInvertedElement(AlgorithmEuclida(n1, a1), n1, a1)*b1%n1
            for i in range(d):
                rootOfEquation.append(int(x+i*n1))
            #print(rootOfEquation)
            return rootOfEquation



################################# Шифровка/Расшифровка текста ###################################



def AffineCipherEncryption(text, a, b):

    mod = len(Alphabet)**2
    if gcd(a, len(Alphabet)) != 1:
        print(a, " не взаимнопростое с ", len(Alphabet), "\nЗашифрока невозможна!")
        return

    # разбиваем текст на биграммы
    arrBigrams = []
    i = 0
    while i < len(text)-1:
        char = text[i] + text[i+1] 
        arrBigrams.append(char)
        i+=2

    # переводим биграммы в числа
    arrX = []
    for bigram in arrBigrams:
        arrIndexX = []
        for i in range (2):
            for j in range (len(Alphabet)):
                if bigram[i] == Alphabet[j]:
                    arrIndexX.append(j)
        X = arrIndexX[0]*31+arrIndexX[1]
        arrX.append(X)


     # Считаем индексы зашифрованного текста и записываем буквы в массив
    arrY = []
    for x in arrX:
        y = (a*x+b)%961
        y1 = int(y/31)
        y2 = y%31
        arrY.append(Alphabet[y1])
        arrY.append(Alphabet[y2])
            


    encryptedText = ''
    for i in arrY:
        encryptedText += i
   

    #print("Зашифрованный текст:\n", encryptedText)
    file2 = open(file_encrypted, "w")
    file2.write(encryptedText)
    file2.close()
    return encryptedText


def AffineCipherDecryption(text, a, b):

    if gcd(a, len(Alphabet)) != 1:
        print(a, " не взаимнопростое с ", len(Alphabet), "\nРасшифрока невозможна!")
        return

    mod = len(Alphabet)**2
    inverted = FindInvertedElement(AlgorithmEuclida(mod, a), mod, a)

    
    # разбиваем текст на биграммы
    arrBigrams = []
    i = 0
    while i < len(text)-1:
        char = text[i] + text[i+1] 
        arrBigrams.append(char)
        i+=2

    # переводим биграммы в числа
    arrY = []
    for bigram in arrBigrams:
        arrIndexY = []
        for i in range (2):
            for j in range (len(Alphabet)):
                if bigram[i] == Alphabet[j]:
                    arrIndexY.append(j)
        Y = arrIndexY[0]*31+arrIndexY[1]
        arrY.append(Y)

     # Считаем индексы pашифрованного текста и записываем буквы в массив
    arrX = []
    for y in arrY:
        x = inverted*(y-b)%961
        x1 = int(x/31)
        x2 = x%31
        arrX.append(Alphabet[x1])
        arrX.append(Alphabet[x2])
            

    decryptedText = ''
    for i in arrX:
        decryptedText += i

    #print("Расшифрованный текст:\n", decryptedText)
    #file2 = open(file_decrypted, "w")
    #file2.write(decryptedText)
    #file2.close()
    return decryptedText




                                    ### Задание №2 ####
                            ## Поиск самых частых биграмм в шифротексте ##

# функция, которая ищет 5 самых частых биграмм
def FindFrequentBigramsInCipherText(text):
    # разбиваем текст на биграммы
    bigramms = []
    i = 0
    while i < len(text)-1:
        char = text[i] + text[i+1] 
        bigramms.append(char)
        i+=2


    sumOfCountOfBigrams = 0
    for i in range(0, len(bigramms)):    # тут мы считаем сумму количества каждой биграммы
        sumOfCountOfBigrams+=text.count(bigramms[i])

    CountOfBigrams = ''
    bigramsAndCount = dict()

    for i in range(0, len(bigramms)):
        CountOfBigrams = text.count(bigramms[i])
        bigramsAndCount.update({bigramms[i]: CountOfBigrams})
 
    # выводим самые частые биграммы
    mostCommonBigrams = dict(Counter(bigramsAndCount).most_common(5))
    FrequentBigramsCipherText = []
    for i in mostCommonBigrams.items():
        FrequentBigramsCipherText.append(i[0])

    print("Самые часто встречаемые биграммы в шифротексте по спаданию:")
    print(FrequentBigramsCipherText)
    print("\nСамые часто встречаемые биграммы в открытом тексте по спаданию:")
    print(FrequentBigramsPlainText)

    return FrequentBigramsCipherText



                                     ### Задание №3 ####
                         #### Поиск предполагаемых ключей ###
def FindKeys(FrequentBigramsCipherText):
    #file = open(file_encrypted, "r")
    #cont_source = file.read()
    #file.close()
    #context = filterText(cont_source)  
    
    mod = len(Alphabet)**2

    # переводим биграммы в числа 
    IndexOfBigramsInCipherText = []
    for y in FrequentBigramsCipherText:
        arrIndexY = []
        for i in range (2):
            for j in range (len(Alphabet)):
                if y[i] == Alphabet[j]:
                    arrIndexY.append(j)
        Y = arrIndexY[0]*31+arrIndexY[1]
        IndexOfBigramsInCipherText.append(Y)
            

    counter = 0
    KeyCandidates = []
    ## ищем перестановки биграмм
    permutationsOfIndexOfBigramsInPlainText = []
    permutationsX = list(itertools.permutations(IndexFrequentBigramsPlainText))
    for IndexesX in permutationsX:
        IndexesOfBigramsInPlainText = []
        for x in IndexesX:
            IndexesOfBigramsInPlainText.append(x)
        permutationsOfIndexOfBigramsInPlainText.append(IndexesOfBigramsInPlainText)

    
    # переставлем между собой биграммы и составлем систему уравнений
    print("\nКандидаты на  a  и  b :\n")
    for j in range (len(permutationsOfIndexOfBigramsInPlainText)):
        k=0
        for i in range(4):
            k=i+1
            while k <= 4:
                x1 = permutationsOfIndexOfBigramsInPlainText[j][i]
                x2 = permutationsOfIndexOfBigramsInPlainText[j][k]
                y1 = IndexOfBigramsInCipherText[i]
                y2 = IndexOfBigramsInCipherText[k]
               # print("\n  x* ->  ", AlphabetBigrams[arrXXX[j][i]], "\tx** ->  ", AlphabetBigrams[arrXXX[j][k]], "\n  y* ->  ", AlphabetBigrams[arrY[i]], "\ty** ->  ", AlphabetBigrams[arrY[k]])
                k+=1


                reverse = LinearCompare((x1-x2)%mod, (y1-y2)%mod, mod)
                if reverse == None:
                    continue
                for r in reverse:
                    a =  r % mod
                    b = (y1 - a * x1)%mod
                    if ([a, b] in KeyCandidates) or (a == 0) or (gcd(a, len(Alphabet)) != 1):
                        continue

                    else:
                        KeyCandidates.append([a, b])
                       # print("x*: ", x1, "y*: ", y1, "\nx**: ", x2, "y**:" , y2)
                        print("a:  ", a, " \t|   b:  ", b)
                        print("-----------------------------")
                        counter+=1
    print("Всего ", counter, " вариантов\n")   
    return KeyCandidates



                                    ### Задание №4 ####
                         #### Откидываем несодержательные тексты ###

#### Функция, которая считает индекс соответствия ###
def ConformityIndex(text):

    arrNoRepeatText = deleteRepeatedElements(text) 
    sumP = 0
    sumK = 0

    for i in range (0, len(arrNoRepeatText)):
        countLetter = text.count(arrNoRepeatText[i])
        p = countLetter*(countLetter-1)
        sumP+=p
        sumK+=countLetter
    index = sumP/(sumK*(sumK-1))
    print("Индекс соответствия: ", index)
    return index

## откидываем неподходящие тексты
def ChooseCorrectText(keys, text):
    GoodTextes = []
    arrKeys = []
    #counter = 0
    for key in keys:
        #counter+=1
        for i in range (len(key)):
            if i == 0:
                a = key[i]
            else:
                b = key[i]
       # print(counter)

        ourText = AffineCipherDecryption(text, a, b)
       # print("a: ", a, "b: ", b)

       # проверем есть ли в тексте запрещенные биграммы, если есть, то откидываем его
        bigrams = []
        for i in range (len(ourText)-1):
            char = ourText[i] + ourText[i+1]
            bigrams.append(char)
        isRightText = True
        for bigram in bigrams:
            if bigram in banedBigrams:
                isRightText = False
                break
        if isRightText == True:

            CIndex = ConformityIndex(ourText)
            if (CIndex < 0.05) or (CIndex > 0.06):
                continue

            GoodTextes.append(ourText)
            print("a: ", key[0], '\tb: ', key[1])
            print("Расшифрованный текст:")
            print(ourText)
            arrKeys.append(key)

    print("\nПредполагаемые ключи:")
    for keys in arrKeys:
        print("a: ", keys[0], "  b: ", keys[1])
    return arrKeys



file = open(file_encrypted, "r")
cont_source = file.read()
file.close()
contextE = filterText(cont_source)
ChooseCorrectText(FindKeys(FindFrequentBigramsInCipherText(contextE)), contextE)


# записываем расшифрованный текст в файл
print("Введите  a:  ", end='')
a = int(input())
print("Введите  b:  ", end='')
b = int(input())
file = open(file_encrypted, "r")
cont_source = file.read()
file.close()
contextE = filterText(cont_source)
decryptedText = AffineCipherDecryption(contextE, a, b)
file = open(file_decrypted, "w")
file.write(decryptedText)
file.close()