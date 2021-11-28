import re
import random

file = open("../docs/result.txt", "w", encoding='UTF8')  # result decode
file1 = open("../docs/1.txt", "r", encoding='UTF8').read()
text1 = re.sub(r"[^а-яё]+", "", file1.lower()).replace("ё", "е").replace("", "")  # encoding
file2 = open("../docs/2.txt", "r", encoding='UTF8')
text2 = file2.read()  # decoding
alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


def rand_key():
    mass = []
    print('Enter length of key:')
    long = int(input())
    j = 0
    while j < long:
        i = alphabet[random.randint(0, len(alphabet) - 1)]
        mass.append(i)
        j += 1
    key = ''.join(mass)
    print('key:', key)
    return key


def encrypt(text, key):
    keyindexes = []
    ciphertext = []
    for i in range(len(key)):
        keyindexes.append(alphabet.index(key[i]))
    for i in range(len(text)):
        EncodLeter = (keyindexes[i % len(keyindexes)] + alphabet.index(text[i])) % len(alphabet)
        ciphertext.append(alphabet[EncodLeter])

    cipheredtext = ''.join(ciphertext)
    return cipheredtext


def decrypt(text, key):
    keyindexes = []
    entrancetext = []
    for i in range(len(key)):
        keyindexes.append(alphabet.index(key[i]))
    for i in range(len(text)):
        DecodLeter = (alphabet.index(text[i]) - keyindexes[i % len(keyindexes)] + len(alphabet)) % len(alphabet)
        entrancetext.append(alphabet[DecodLeter])

    entrancedtext = ''.join(entrancetext)
    return entrancedtext


def compliance_index(text):
    arr = []
    for i in alphabet:
        letter = text.count(i)
        arr.append(letter * (letter - 1))
    I = sum(arr) / (len(text) * (len(text) - 1))
    return I


def ComplianceIndexForDecrypt(text, size):
    blocks = []
    index = []
    for i in range(size):
        blocks.append(text[i::size])
    for i in range(len(blocks)):
        index.append(compliance_index(blocks[i]))
    print("Len of key:", size, ",", "Compliance index for block:", sum(index) / len(blocks))
    return blocks


def MaxLetter(text):
    letter = []
    for i in alphabet:
        letter.append(text.count(i))
    return letter.index(max(letter))


def MakeKey(text, size, letter):
    keys = []
    blocks = ComplianceIndexForDecrypt(text, size)
    for i in range(len(blocks)):
        maxcount = MaxLetter(blocks[i])
        key = (maxcount - alphabet.index(letter)) % len(alphabet)
        keys.append(alphabet[key])
        key = ''.join(keys)
    return key


# main part
# task1

key1 = rand_key()
en = encrypt(text1, key1)
print("Encrypted text:", en)
print("Decrypted text:", decrypt(en, key1))
print("Compliance index:", compliance_index(en), '\n')

# task2
for r in range(1, len(alphabet)):
    ComplianceIndexForDecrypt(text2, r)
print('\n')
print('Make key:', MakeKey(text2, 12, 'о'))
key = 'вшекспирбуря'
print('Key:', key)
decode = decrypt(text2, key)
print("Decrypted text:", decode)
file.write(decode)