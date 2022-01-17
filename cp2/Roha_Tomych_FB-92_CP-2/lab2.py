from collections import Counter
from itertools import chain
import random
import math
import sys
import re

keylist = ['ыу', 'кян', 'дуоу', 'трхчр', 'ишчдрцжзсж', 'юдаюшшрщюыс', 'шхюфсмсядцры', 'бтчъмцжгсвыщт', 'тиоахулцоэуйон', 'ыжхнгэйаъшнзвмй', 'щкцвяфкуэмпзыщон', 'щпжчвыкъэйэаянчмэ', 'шдтщгпбчхэымбошавк', 'чнкдзхюожфжшрэчпадя', 'мекьякгааьоюикцяияэй']

alphabet = [chr(i) for i in range(ord("а"), ord("а") + 32)]

puretext = ''
fin = open('text.txt', 'r', encoding='utf-8')
puretext = fin.read()
fin.close()
puretext=puretext.lower().replace('\n', '').replace('\r', '').replace('','').replace('ё', 'е')
for char in puretext[:]:
        if char not in alphabet:
            puretext = puretext.replace(char, '')
fout = open('puretext.txt', 'w', encoding='utf-8')
fout.write(puretext)
fout.close()

def encode_text(key):
    encoded = []
    for index, char in enumerate(puretext):
        index_of_key = index % len(key)
        index_of_cipher = (alphabet.index(char) + alphabet.index(key[index_of_key])) % len(alphabet)
        encoded.append(alphabet[index_of_cipher])
    return encoded

def decode_text(text, key):
    decoded = []
    for index, char in enumerate(text):
        index_of_key = index % len(key)
        index_of_decipher = (alphabet.index(char) - alphabet.index(key[index_of_key])) % len(alphabet)
        decoded.append(alphabet[index_of_decipher])
    return ''.join(decoded)

def coincidence_index(cipher):
    I = 0
    n = len(cipher)
    for Y in dict(Counter(cipher[index] for index in range(len(cipher)))).values():
        I = I + (Y * (Y - 1))
    return I * (1/(n * (n - 1)))

def split_blocks(text, r):
    blocks = []
    for i in range(r):
        blocks.append(text[i::r])
    return blocks

def find_r(text):
    theoretical_index = {}
    for r in range(2, 31):
        index = 0
        blocks = split_blocks(text, r)
        for block in blocks:
            index = index + coincidence_index(block)
        index = index / r
        theoretical_index[r] = index
    print(theoretical_index)
    return theoretical_index

def key_found(text, true_key_length):
    possible_keys = {}
    blocks = split_blocks(text, true_key_length)
    most_used_letters = 'оеаинтсрвлкмдпуяыьгзбчйхжшюцщэф'
    for letter in most_used_letters:
        result = ''
        for block in blocks:
            freq = Counter(block[index] for index in range(len(block)))
            max_freq = max(freq, key=freq.get)
            result = result + alphabet[(alphabet.index(max_freq) - alphabet.index(letter)) % len(alphabet)]
        possible_keys[letter] = result
    return possible_keys

def task1_2():
    indexes={}
    for key in keylist:
        ciphered = encode_text(key)           
        indexes = [coincidence_index(ciphered)]
        print(indexes)

def task3():

    fin = open('var10pure.txt', 'r', encoding='utf-8')
    var10text = fin.read()
    fin.close()
    key_length = find_r(var10text)
    print(key_length)
    true_key_length = input()
    print(key_found(var10text, int(true_key_length)))
    print('ВВЕДІТЬ КЛЮЧ')
    key_final = input() 
    print(decode_text(var10text, key_final))

task1_2()
task3()
