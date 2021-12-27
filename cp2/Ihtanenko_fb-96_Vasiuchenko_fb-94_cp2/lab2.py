import regex
import collections
import unicodedata
import pandas as pd

Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
            'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
Alphabet_and_space = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
                      'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
Alphabet_num = []
for id, item in enumerate(Alphabet):
    Alphabet_num.append(id)
Alphabet_dict = dict(zip(Alphabet, Alphabet_num))

book = open(r"D:\Python stuff\Lab2_Crypta\b451.txt", encoding='utf-8').read()
book = book.lower()
book = book.replace("\n"," ")
book = regex.sub(r'[a-zA-Z]', r'', book).strip()
book = book.replace("і", "")
book = ' '.join(book.split())

# without space
text = ''.join(c for c in book if unicodedata.category(c).startswith('L'))

# with space
text_with_space = regex.sub(r'[^\w\s]+|[\d]+', r'', book).strip()
#print(text)


def encode(data, key, Alphabet_dict, Alphabet):
    temp = []
    for i in range(0, len(data)):
        temp.append((Alphabet_dict[data[i]] + Alphabet_dict[key[i % len(key)]]) % len(Alphabet))
    cipher = Alphabet[temp[0]]
    for i in range(1, len(text)):
        cipher = cipher + Alphabet[temp[i]]
    return cipher


def decode(cipher, key, Alphabet_dict, Alphabet):
    temp = []
    for i in range(0, len(cipher)):
        temp.append((Alphabet_dict[cipher[i]] - Alphabet_dict[key[i % len(key)]]) % len(Alphabet))

    plaintext = Alphabet[temp[0]]
    for i in range(1, len(cipher)):
        plaintext = plaintext + Alphabet[temp[i]]
    return plaintext


def ngram(data, n):
    ngramma = []
    for i in range(0, len(data), n):
        ngramma.append(data[i:i + n])
    return ngramma


def Letters_count(ngramma):
    return dict(collections.Counter(ngramma))


def I(Letters_count):
    i = []
    for key in list(Letters_count.keys()):
        i.append(Letters_count[key] * (Letters_count[key] - 1))
    return 1 / (sum(Letters_count.values()) * (sum(Letters_count.values()) - 1)) * sum(i)


keys = ["м", "ма", "луч", "зной", "топаю", "всесложноо", "уменятожеса", "попадаетонао",
        "ситечкеилипро", "чаятравяногохо", "спроситчтосказа", "помочьтакзайтивд",
        "явключустримиесли", "помочьскриптойустя", "интерпретированиедоп"]

#print(d)

d = encode(text, keys[0], Alphabet_dict, Alphabet)
f = open("task1-encoded.txt", 'a')
f.write(d)
f.close

cipher = []
decipher = []
for key in keys:
    cipher.append(encode(text, key, Alphabet_dict, Alphabet))

r = []
l = []
for i in range(0, len(cipher)):
    l.append(len(keys[i]))
    letters_count = Letters_count(ngram(cipher[i], 1))
    r.append(I(letters_count))
print(r)

cipher = []
decipher = []
for key in keys:
    cipher.append(encode(text, key, Alphabet_dict, Alphabet))

r = []
l = []
for i in range(0, len(cipher)):
    l.append(len(keys[i]))
    letters_count = Letters_count(ngram(cipher[i], 1))
    r.append(I(letters_count))
print(r)


table = pd.DataFrame()
table['r'] = l
table['I'] = r
table.to_excel("r.xlsx")


def block(data, r):
    bl = []
    for j in range(0, r):
        temp = ""
        for i in range(0, len(data) - j, r):
            temp = temp + data[i + j]
        if temp != "":
            bl.append(temp)
        else:
            continue
    return bl


def I_dict(cipher):
    bl = []
    for r in range(2, 31):
        bl.append(block(cipher, r))

    Iy = []
    for i in range(0, len(bl)):
        j = []
        for k in range(0, len(bl[i])):
            l_count = Letters_count(bl[i][k])
            j.append(I(l_count))
        Iy.append(sum(j) / len(j))
    return dict(zip([r for r in range(2, 31)], Iy))

I_ = I_dict(cipher)

cipher = open(r"D:\Python stuff\Lab2_Crypta\task2.txt", encoding='utf-8').read()
cipher = cipher.replace('\n', "")

Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п',
            'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
Alphabet_dict = dict(zip(Alphabet, Alphabet_num))
I_2 = I_dict(cipher)
print(I_2)

table2 = pd.DataFrame()
table2['r'] = [r for r in range(2, 31)]
table2['I'] = I_2.values()
table2.to_excel("r2.xlsx")


def search_key(r, cipher, Alphabet_dict, Alphabet):
    blocks = block(cipher, r)
    l_count = []
    for i in range(0, len(blocks)):
        l_count.append(Letters_count(blocks[i]))

    freq = []
    for i in range(0, len(blocks)):
        temp = []
        temp = {k: l_count[i][k] / len(blocks[i]) for k in l_count[i]}
        freq.append(temp)
    top = []
    for i in range(0, len(freq)):
        temp = []
        temp = sorted(freq[i], key=lambda x: l_count[i][x], reverse=1)
        top.append(temp[0])

    help = ['о', 'а', 'е', 'и', 'н', 'т', 'л', 'с', 'р', 'в', 'к', 'у', 'м', 'п', 'д', 'г',
            'я', 'з', 'ь', 'ы', 'ч', 'б', 'й', 'ж', 'ш', 'х', 'ю', 'щ', 'ц', 'э', 'ф', 'ъ']

    keys = []
    for j in range(0, len(help)):
        key = ""
        for i in range(0, len(top)):
            key = key + Alphabet[(Alphabet_dict[top[i]] - Alphabet_dict[help[j]]) % (len(Alphabet))]
        keys.append(key)
    return keys


k = search_key(14, cipher, Alphabet_dict, Alphabet)

plaintext = decode(cipher, k[0], Alphabet_dict, Alphabet)

k[0] = 'последнийдозор'
prev = 'жосвеыдиадозор'
plaintext = decode(cipher, k[0], Alphabet_dict, Alphabet)
plaintext