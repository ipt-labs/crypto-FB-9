from array import *
from math import*
 
file_source = "file1.txt"
file_encrypted = "file2_encrypted.txt"
file_decrypted = "file2_dencrypted.txt"
file_var = "file3_var4.txt"
file_decrypted_var = "file3_dencrypted_var.txt"

 
Alphabet=['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']
AlphabetFrequentlyEncountered=['о','е','а','и','н','т','с','р','в','л','к','м','д','п','у','я','ы','ь','г','з','б','ч','й','х','ж','ш','ю','ц','щ','э','ф','ъ']
 
####  убираем буквы, которых нет в алфавите ####
def removeExtraLetters(s):
    arr = []
    for char in s:
        if char not in Alphabet:
           char = ''
        else:
            arr.append(char)
    return ''.join(arr)


####  убираем повторяющиеся буквы ####
def deleteRepeatedElements(arrC):
    arr = []
    thisset = set()
    for char in arrC:
        thisset.add(char)
    for c in thisset:
        arr.append(c)
    return arr


        ########## Задание № 1 ##########

#### Функция зашифровки текста ###

def Encryption(file, key):
    print("Размер ключа: ", len(key))
    cont_source = file.read()
    cont_source = removeExtraLetters(cont_source)

    # Находим индексы открытого текста
    arrIndexSourceText = []
    for i in range (0, len(cont_source)):
        for j in range (0, len(Alphabet)):
            if(cont_source[i] == Alphabet[j]):
                arrIndexSourceText.append(j)

    # Находим индексы ключа
    arrIndexKey = []                
    for i in range (0, len(key)):
        for j in range (0, len(Alphabet)):
            if(key[i] == Alphabet[j]):
                arrIndexKey.append(j)

    # Считаем индексы зашифрованного текста
    arrEncryptedTextIndex = []
    for i in range (0, len(arrIndexSourceText)):
        indexEncrypted = (arrIndexSourceText[i]+arrIndexKey[i%len(arrIndexKey)])%32
        arrEncryptedTextIndex.append(indexEncrypted);


    # Выводим зашифрованный текст
    encryptedText=''        
    for i in range (0, len(arrEncryptedTextIndex)):
        for j in range (0, len(Alphabet)):
            if(arrEncryptedTextIndex[i] == j):
                encryptedText+=Alphabet[j]
    #print("Зашифрованный текст: ", encryptedText)

    file2 = open(file_encrypted, "w")
    file2.write(encryptedText)
    file2.close()
    file.close()
    return encryptedText



### Функция расшифровки текста ####
def Decryption(file1, file2, key):

    print("Размер ключа: ", len(key))
    cont_EncryptedText = file1.read()
    cont_EncryptedText = removeExtraLetters(cont_EncryptedText)

    # Находим индексы зашифрованного текста
    IndexEncryptedText = []
    for i in range (0, len(cont_EncryptedText)):
        for j in range (0, len(Alphabet)):
            if(cont_EncryptedText[i] == Alphabet[j]):
                #print(j) 
                IndexEncryptedText.append(j)

    # Находим индексы ключа
    arrIndexKey = []                
    for i in range (0, len(key)):
        for j in range (0, len(Alphabet)):
            if(key[i] == Alphabet[j]):
                arrIndexKey.append(j)

    # Считаем индексы зашифрованного текста
    _arrDecryptedTextIndex = []
    for i in range (0, len(IndexEncryptedText)):
        indexDecrypted = (IndexEncryptedText[i]-arrIndexKey[i%len(arrIndexKey)])%32
        #print(x)
        _arrDecryptedTextIndex.append(indexDecrypted);

    # Выводим расшифрованный текст
    decryptedText=''        
    for i in range (0, len(_arrDecryptedTextIndex)):
        for j in range (0, len(Alphabet)):
            if(_arrDecryptedTextIndex[i] == j):
                decryptedText+=Alphabet[j]
    #print("Расшифрованный текст: ", decryptedText)


    file2.write(decryptedText)
    file1.close()
    return decryptedText


# тут зашифровуем текст
file1 = open(file_source, "r")
print("Введите ключ: ", end='')
_key = str(input())
Encr = Encryption(file1, _key)
file1.close()
print()
# тут расшифровуем текст
file2 = open(file_encrypted, "r")
file3 = open(file_decrypted, "w")
print("Введите ключ: ", end='')
_key = str(input())
Decryption(file2, file3, _key)
file2.close()
file3.close()





        ########## Задание № 2 ##########

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


#ConformityIndex(Encr)



          ########## Задание № 3 ##########

#### Функция, которая ищет размер ключа ###
def findKeySize(text):
    arrText = []
    arrMid = []
    for i in range (2, 30):
        mid = 0
        for k in range (0, i):
            j=k
            arrText = []
            while(j<len(text)):
                arrText.append(text[j])
                #print(text[j], end='')
                j+=i

            arrNoRepeatText = deleteRepeatedElements(arrText)
            sumP = 0
            sumK = 0
            for l in range (0, len(arrNoRepeatText)):
                countLetter = arrText.count(arrNoRepeatText[l])
                p = countLetter*(countLetter-1)
                #print(arrText[l], " : --- : ", countLetter)
                sumP+=p
                sumK+=countLetter
            common = sumP/(sumK*(sumK-1))
            #print("common: \t", common)
            mid+=common
        mid/=i
        arrMid.append(float(format(mid, ".2f")))
       # print("key: ", i, "\tmid: \t", mid)


    # Ищем ключ, при котором был скачок
    x=-1
    for i in range(0, len(arrMid)):
        if(arrMid[i]>x):
            x = arrMid[i]
    for i in range(0, len(arrMid)):
        if(x == arrMid[i]):
            x = i
    print("Предпологаемый размер ключа: ", x+2)
    return x+2


#### Функция, которая делит текст на части и находит в каждом кусочке самую часто встречаемую букву ###
def SlipText(text, keyLen):
    arrMaxLetters = []
    for i in range (0, keyLen):
        #print("key size: ", i)

        arrLetters = []
        j=i
        while(j < len(text)):
            #print(text[j], end='')
            arrLetters.append(text[j])
            j+=keyLen

        
           # тут мы считаем сумму количество каждой буквы
        CountLetters = dict()
        for k in range(0, len(arrLetters)):
            sumOfLetters=arrLetters.count(arrLetters[k])
            #print(arrLetters[k], " : ", sumOfLetters)
            deleteRepeatedElements(arrLetters)
            CountLetters.update({arrLetters[k]: sumOfLetters})


        #print(dict(CountLetters.items()))

        # тут записываем самые повторяющиеся буквы
        maxLetter = max(CountLetters.values())
        #final_dict2 = {k:v for k, v in CountLetters.items() if v == maxLetter}
        #print("max: ", final_dict2)
        final_dict = dict([max(CountLetters.items(), key=lambda k_v: k_v[1])])
        #print("Самая встречаемая буква в кусочке: ", final_dict)
        for key in final_dict.keys():
            arrMaxLetters.append(str(key))
    result = ''
    for i in range(0, len(arrMaxLetters)):
        result += arrMaxLetters[i]

    return result

#### Функция, которая ищет предпологаемый ключ ###
def findKey(arrMaxLetters):
    arrKeys = []

    # Находим индексы частовстречаемых букв в частях текста
    arrIndexLetters = []
    for i in range (0, len(arrMaxLetters)):
        for j in range (0, len(Alphabet)):
            if(arrMaxLetters[i] == Alphabet[j]):
                arrIndexLetters.append(j)

    # Находим индексы частовстречаемых букв алфавита
    arrIndexFE = []
    for i in range (0, len(AlphabetFrequentlyEncountered)):
        for j in range (0, len(Alphabet)):
            if(AlphabetFrequentlyEncountered[i] == Alphabet[j]):
                arrIndexFE.append(j)

    # Считаем предпологаемые индексы ключа
    arrResult = []
    for i in range (0, 3):  #len(Alphabet)
        arrResult = []
        for j in range (0, len(arrMaxLetters)):
            arrResult.append(Alphabet[(arrIndexLetters[j] - arrIndexFE[i])%32])
        arrKeys.append(arrResult)
     
    # Выводим предпологаемый ключ
    print("\nПредпологаемый ключ:")
    for i in range (0, 3):  #len(arrKeys)
        print("'", AlphabetFrequentlyEncountered[i], "' : ", end='')
        print(arrKeys[i])
        #break
    return arrKeys


file1 = open(file_var, "r")
EncodedText = file1.read()
file1.close()
EncodedText = removeExtraLetters(EncodedText)
findKey(SlipText(EncodedText, findKeySize(EncodedText)))  


# тут расшифровуем текст
file2 = open(file_var, "r")
file3 = open(file_decrypted_var, "w")
print("Введите ключ: ", end='')
_key = str(input())
Decryption(file2, file3, _key)
file2.close()
file3.close()