import string
import collections

MostFrequent = ('о', 'е', 'и', 'а', 'н', 'т')
BigramsRussian = ('ст', 'но', 'ен', 'то', 'на')
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
letter_with_number = {k: v for v, k in enumerate(alphabet[:])}
number_with_letter = {v: k for v, k in enumerate(alphabet[:])}
alphabet_length = len(alphabet)

def gcd(a, b): # розширений алгоритм евкліда
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcd(b, a % b)
        return d, y, x - (a // b) * y #y ta x taki shco ay+bx = d(ax+by = d)

def countFun(movy, shT, n): #function 
    result = [] 
    gcdOfAB = gcd(movy, n)[0]
    if gcdOfAB == 1:# obernenyi element isnue tolyko esli chisla vzaimno prostye
        result.append((shT * gcd(movy, n)[1]) % n)# result v konec spiska (variant kliucha a)
        return result
    elif gcdOfAB > 1:
        if shT % gcdOfAB == 0:
            x0 = countFun(movy / gcdOfAB, shT / gcdOfAB, n / gcdOfAB)[0]
            result.append(int(x0))
            for i in range(0, gcdOfAB - 1):
                x0 = x0 + n / gcdOfAB
                result.append(int(x0))
            return result
        else:
            result.append(0)
            return result

def bigram(ready_for_use_text):
    bigram_freq = {}
    length = len(ready_for_use_text[:])
    for i in range(0, length, 2):
        bigram = ready_for_use_text[i:i + 2]
        if bigram not in bigram_freq:
            bigram_freq[bigram] = 1 / length
            continue
        bigram_freq[bigram] += 1 / length
    return bigram_freq


def monogram(ready_for_use_text):
    sym_freq = {}
    length = len(ready_for_use_text[:])
    for i in ready_for_use_text:
        if i not in sym_freq:
            sym_freq[i] = 1 / length
            continue
        sym_freq[i] += 1 / length
    return sym_freq


def findKeys(ab1, cd1, ab2, cd2):
    a = countFun(ab1 - cd1, ab2 - cd2, alphabet_length ** 2)
    result = []
    if len(a) == 1:
        b = (ab1 - ab2 * a[0]) % (alphabet_length ** 2)
        result.append((a[0], b))
        return result
    else:
        for value in a:
            b = (ab1 - ab2 * value) % (alphabet_length **2)
            result.append((value, b))
        return result

def checking_numb_elements_match(list1, list2):
    result = 0
    for elem in list1:
        if elem in list2:
            result += 1
    return result

def decrypt(bigrams, k):
    result = ""
    for bigr in bigrams:
        ab = dscore(countFun(k[0], bigr - k[1], alphabet_length ** 2))
        result = result + ab
    return result

def count_frequency_all(text):
    frequency = {}
    text = text.replace(' ', '').upper()
    counts = collections.Counter(text)
    for i in counts:
        frequency[i] = counts[i]
    return frequency


def dscore(bigram):
    a = bigram[0] % alphabet_length
    b = (bigram[0] - a) / alphabet_length
    ab = number_with_letter[b] + number_with_letter[a]
    return ab

def count_index(text):
    length = len(text)
    if length == 1:
        result = 1 / ((length) * length)
    else:
        result = 1 / ((length - 1) * length)

    freq = count_frequency_all(text)
    sum = 0
    for letter in freq:
        sum += (freq[letter] - 1) * freq[letter]
    return result * sum


def countFrequency(text):
    result = []
    monograms = sorted(monogram(text).items(), key=lambda x: x[1])
    for i in range(0, 6):
        result.append(monograms.pop())
    for i in range(0, len(result)):
        result[i] = result[i][0]
    return result

def match(popular, decrypted):
    popNumber = []
    for bigram in popular:
        popNumber.append(letter_with_number[bigram[0]] * alphabet_length + letter_with_number[bigram[1]])
    decNumber = []
    for bigram in decrypted:
        decNumber.append(letter_with_number[bigram[0]] * alphabet_length + letter_with_number[bigram[1]])
    
    popComb = []
    copylist = popNumber
    for item in popNumber:
        for item2 in copylist:
            popComb.append((item2,item))
    decComb = []
    copylist = decNumber
    for item in decNumber:
        for item2 in copylist:
            decComb.append((item2,item))    
    result = []
    for i in range(0, len(decComb)):
        for y in range(0, len(popComb)):
            keyValues = findKeys(decComb[i][0], decComb[i][1], popComb[y][0], popComb[y][1])
            if len(keyValues) == 1:
                result.append(keyValues[0])
            else:
                for value in keyValues:
                    result.append(value)
    result = list(dict.fromkeys(result))
    return result

def Decryptionfulltext(text, keys):
    bigrams =[]
    for bigr in bigram(text):
        bigrams.append(letter_with_number[bigr[0]] * alphabet_length + letter_with_number[bigr[1]])
    final_Key = 0
    final_Index = 0
    for key in keys:
        if key[0] == 0:
            continue
        decryptedText = decrypt(bigrams, key)
        freq = countFrequency(decryptedText)
        index = count_index(decryptedText)
        if checking_numb_elements_match(freq, MostFrequent) >= 5:
            print("можливий ключ:", key)
            print("індекс ", index)
            if (index >= final_Index)&(index< 0.9):
                final_Index = index
                final_Key = key

        else:
            continue
    decryptedText = decrypt(bigrams, final_Key)
    freq = countFrequency(decryptedText)
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.")
    print("ключ яким був розшифрован текст : ", final_Key)
    print("найпопулярніші літери в тексті : ", freq)
    print(decryptedText)
    print("індекс = ", final_Index)
    return decryptedText

text = open("02.txt", encoding="utf8").read().replace('\n', '').replace(' ', '').lower()
print(text)
print(countFrequency(text))
print(bigram(text))
# 5 more popular Bigrams from text
fiveBigrams = []
bigrams = sorted(bigram(text).items(), key=lambda x: x[1])
for i in range(0, 5):
    fiveBigrams.append(bigrams.pop())
for i in range(0, len(fiveBigrams)):
    fiveBigrams[i] = fiveBigrams[i][0]
print(fiveBigrams)
keys = match(BigramsRussian, fiveBigrams)
VT=Decryptionfulltext(text, keys)