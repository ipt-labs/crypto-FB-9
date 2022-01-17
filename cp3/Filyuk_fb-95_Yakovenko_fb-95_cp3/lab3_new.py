import math
import os
from itertools import product
import time

### ваінати алфавіту 1.,2
other = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
global_alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
# other, global_alphabet = global_alphabet, other

alphabet = dict(zip(global_alphabet, range(len(global_alphabet))))
reverse_alphabet = dict((v, k) for k, v in alphabet.items())


def read_file(default="./07.txt"):
    with open(default, mode='r', encoding='utf-8') as infile:
        unfiltered = infile.read().lower()  # reading file, bringing to lowertext
        unfiltered = ''.join(unfiltered.split())
    ###Фільтрація
    allowed_no_whitespace = global_alphabet
    text = ''
    for char in unfiltered:
        if char in allowed_no_whitespace:
            text += char
        if char == 'ё':
            text += 'е'
        if char == 'ъ':
            text += 'ь'
    return text


### Фільтрація алфавіту
### Алфавіт в цифру
def to_numbers(text):
    global alphabet
    if isinstance(text, str):
        return alphabet.get(text)
    return [alphabet.get(x) for x in text]


### навпаки
def to_chars(text):
    global reverse_alphabet
    if isinstance(text, int):
        return reverse_alphabet.get(text)
    return [reverse_alphabet.get(x) for x in text]


### Створимо н-грами
from collections import Counter


def ngram_ctr(letters):
    keys = Counter(letters).keys()  # stores n-gram to keys
    values = [x / len(letters) for x in Counter(letters).values()]  # counts corresponding frequencies
    # creating a new dict
    retval = dict(zip(keys, values))
    return dict(sorted(retval.items(), key=lambda item: item[1], reverse=True))  # sorting dict from highest to lowest


def ngrams(letters, mode):
    result = []
    mode = str(bin(mode))[2:]
    if mode[0] == '1':
        result.append([letters[iter:iter + 1] for iter in
                       range(0, len(letters), 1)])  # stores each symbol to list, like [a, b, c, ...])
    if mode[1] == '1':
        result.append([letters[iter:iter + 2] for iter in
                       range(0, len(letters))])  # stores each 2 symbols to list, like [ab, bc, cd, ...]
    if mode[2] == '1':
        result.append([letters[iter:iter + 2] for iter in
                       range(0, len(letters), 2)])  # stores each 2 symbols to list, like [ab, cd, ef, ...]
    return tuple(result)


### Розповсюджені моно та біграми
common_mono = ['о', 'е', 'а', 'и', 'н', 'т']
common_bigr = ["ст", "но", "то", "на", "ен"]


### LAB3
### Напишемо функції для НСД, розширеного НСД, та обрененого елементу в кільці по модулю
def gcd(x, y):
    return x if y == 0 else gcd(y, x % y)


def ExtendedGCD(a, b):
    if a == 0:
        return b, 0, 1
    Gcd, x1, y1 = ExtendedGCD(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return Gcd, x, y


def reversal(x, m=len(global_alphabet)):
    Gcd, a, b = ExtendedGCD(x, m)
    if Gcd == 1:
        return (a % m + m) % m


### Кодування і декодування біграми
### Кодування
def encode_bigr(bigr):
    bigr = [to_numbers(x) for x in bigr]
    return bigr[0] * len(global_alphabet) + bigr[1]


def encrypt_bigr(bigr, key):
    a = key[0]
    b = key[1]
    return (a * bigr + b) % (len(global_alphabet) ** 2)


### Декодування
def decode_bigr(encoded_bigr):
    for a in global_alphabet:
        a = to_numbers(a)
        for b in global_alphabet:
            b = to_numbers(b)
            a_r = reversal(a)
            if a_r is None:
                break
            else:
                if len(global_alphabet) == (a_r * (encoded_bigr - b) % (len(global_alphabet) ** 2)):
                    return to_chars(a) + to_chars(b)
                if 0 == (a_r * (encoded_bigr - b) % (len(global_alphabet) ** 2)):
                    return to_chars(0) + to_chars(b)


### Шифрування
def decrypt_bigr(bigr, key):
    a = key[0]
    a_r = reversal(a, m=len(global_alphabet) ** 2)
    if a_r is None:
        return
    b = key[1]
    return (a_r * (bigr - b) % (len(global_alphabet) ** 2))


### Лінійне порівняння
def LinCompare(a, b, m=len(global_alphabet) ** 2):
    d = gcd(a, m)
    if d == 1:
        return [reversal(a, m) * b % m]
    if d > 1 and (b // d == 0):
        a_1 = a / d
        b_1 = b / d
        m_1 = m / d
        first = reversal(a_1, m_1) * b_1 % m_1
        return [first + m_1 * i for i in range(d)]


if __name__ == "__main__":
    start_time = time.time()
    filtered_text = read_file()
    monogr_no_whitespaces, bigr_no_cross_no_whitespaces = ngrams(filtered_text, 5)
    print("######")
    print("Н-грами зашифрованого тексту")
    print(monogr_no_whitespaces[:10])
    print(bigr_no_cross_no_whitespaces[:10])
    print("######\n")

    print("######")
    print("Частоти н-грам зашифрованого тексту")
    ctd_monogr_no_whitespaces = ngram_ctr(monogr_no_whitespaces)
    ctd_bigr_no_cross_no_whitespaces = ngram_ctr(bigr_no_cross_no_whitespaces)
    print("\tМогонрами")
    for item in list(ctd_monogr_no_whitespaces.items())[:5]:
        print(f"\t Буква: '{item[0]}' частота: {item[1]}")
    print("\tБіграми")
    for item in list(ctd_bigr_no_cross_no_whitespaces.items())[:5]:
        print(f"\t Буква: '{item[0]}' частота: {item[1]}")
    print("######\n")
    print("######")
    print("найрозповсюдженіші монограми та біграми")
    print(common_mono)
    print(common_bigr)
    print("######\n")

    ### Закодування біграм
    encoded_bigrs = [encode_bigr(item) for item in bigr_no_cross_no_whitespaces]

    ### перебір всіх комбінацій для порівняння найрозповюдженіших біграм ШТ і ВТ
    print("######")
    enc_common_bigr = list(ctd_bigr_no_cross_no_whitespaces.keys())[:5]
    print("Перебір всіх комбінацій для порівняння найрозповюдженіших біграм ШТ і ВТ")
    for i, item in enumerate(enc_common_bigr[:5]):
        print(f"\t {i + 1} Біграма:'{item}'")
    print("######\n")

    ### Перебір розповсюджених біграм ШТ з розповсюдженими біграмами ВТ
    keys = []
    for x in (product(range(5), repeat=4)):
        X_ = encode_bigr(common_bigr[x[0]])
        X__ = encode_bigr(common_bigr[x[1]])
        Y_ = encode_bigr(enc_common_bigr[x[2]])
        Y__ = encode_bigr(enc_common_bigr[x[3]])
        open_dist = (X_ - X__) % len(global_alphabet) ** 2
        cypher_dist = (Y_ - Y__) % len(global_alphabet) ** 2
        if open_dist == 0 or cypher_dist == 0:
            continue
        Solutions = LinCompare(open_dist, cypher_dist)
        if Solutions is not None:
            for a_ in Solutions:
                b_ = (Y_ - a_ * X_)
                while b_ < 0:
                    b_ += len(global_alphabet) ** 2
                b_ = b_ % len(global_alphabet) ** 2
                if not isinstance(a_, int) or not isinstance(b_, int):
                    continue
                new_key = [int(a_), b_]
                if new_key not in keys:
                    keys.append(new_key)

    banned_lst = ["уы", "ыа", "йй", "хщ", "йь", "чщ", "шщ", "чэ", "фц"]
    banned_bigrams = [encode_bigr(a) for a in banned_lst]
    results = []
    for key in keys:
        temp_text = []
        for bigr in encoded_bigrs:
            temp_item = decrypt_bigr(bigr, key)
            if temp_item is not None and temp_item not in banned_bigrams:
                temp_item = decode_bigr(temp_item)
                temp_text.append(temp_item)
            else:
                temp_text = []
                break
        if temp_text:
            candidate = ''.join(temp_text)
            print(candidate[:30], key)
            results.append([candidate, key])
            monogr_no_whitespaces = (candidate, 4)[0]
            ctd_monogr_no_whitespaces = ngram_ctr(monogr_no_whitespaces)
            ctd_bigr_no_cross_no_whitespaces = ngram_ctr(temp_text)
            print("\tМогонрами")
            for item in list(ctd_monogr_no_whitespaces.items())[:5]:
                print(f"\t Буква: '{item[0]}' частота: {item[1]}")
            print("\tБіграми")
            for item in list(ctd_bigr_no_cross_no_whitespaces.items())[:5]:
                print(f"\t Буква: '{item[0]}' частота: {item[1]}")
            print()

    print("--- %s seconds ---" % (time.time() - start_time))

    for item in results:
        print(item[0][:30], item[1])
        reply = input("""Зберегти файл? ("yes" yo yes/ any other to no)\t""")
        if reply == "yes":
            with open(f"./{item[0][:10]}_A{item[1][0]}_B{item[1][1]}.txt", 'w', encoding='utf-8') as outfile:
                outfile.write(item[0])
