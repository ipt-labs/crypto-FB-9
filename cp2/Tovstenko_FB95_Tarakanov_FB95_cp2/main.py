from collections import Counter
import re

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

file = open("mytext.txt", "r", encoding='utf-8')
a = file.read()
a = a.lower()
a = re.sub("[^А-аЯ-я]", "", a)


def encode_function(text, key):
    key_length = len(key)
    encoded_text = []
    for i in range(len(text)):
        char = (alphabet.index(text[i]) + alphabet.index(key[i % key_length])) % 32
        if char == 6:
            char = 'е'
        else:
            char = chr(char + 1072)
        encoded_text.append(char)
    return ''.join(encoded_text)


def conformity_index(text):
    n = len(text)
    index = 0
    text = Counter(text)
    for i in text:
        index += text[i]*(text[i]-1)
    index = index/(n*(n-1))
    return index

def nearest(lst, target):
  return min(lst, key = lambda x: abs(x-target))

def compare_indexes(text):
    i_list = []
    our_i = conformity_index(a)
    i1 = conformity_index(encode_function(text, key1))
    i2 = conformity_index(encode_function(text, key2))
    i3 = conformity_index(encode_function(text, key3))
    i4 = conformity_index(encode_function(text, key4))
    i5 = conformity_index(encode_function(text, key5))
    i6 = conformity_index(encode_function(text, key6))
    print(i1,i2,i3,i4,i5,i6, our_i)

def find_key(text):
    key = []
    for word_length in range(2,32):
        index_sum = 0
        for i in range(word_length):
            a = []
            for j in range(i, len(text), word_length):
                a.append(text[j])

            #print(conformity_index(''.join(a)))
            index_sum += conformity_index(''.join(a))
            #print(a)
        key.append(index_sum/word_length)
        print()
    nearest_val = nearest(key, 0.055)
    print(key.index(nearest_val) + 2)
    print(nearest_val)
    
    print(key)


find_key(a)

def key_value(text, key_length,most_popular):
    b = []
    k = []
    z = ''
    for i in range(0,key_length):
        z = ''
        for j in range(i, len(text), key_length):
            #Текст по "блокам"
            z +=text[j]
        b.append(z)
    print(b)
    for l in range(key_length):
        most_popular_fragment = list(dict(Counter(b[l]).most_common(1)).keys())[0]
        x = (alphabet.index(most_popular_fragment) - alphabet.index(most_popular) ) % 32
        x = chr(x + 1072)
        k.append(x)
        #Адекватный ключик в строку
    return k

keyf = ''.join(key_value(a, 28, 'о'))
print("\nКлюч який пропонує программа:" +keyf)



keyprint = ['э', 'к', 'о', 'м', 'а', 'я', 'т', 'н', 'и', 'к', 'ф', 'у', 'к', 'о', 'э', 'к', 'о', 'м', 'а', 'я', 'т', 'н', 'и', 'к', 'ф', 'у', 'к', 'о']
print("\nНаш ключ:")
print(keyprint)
def decrypt_function(text, key):
    decoded_text = []
    for i in range(len(text)):
        func = (alphabet.index(text[i]) - alphabet.index(key[i % 28]) + 32) % 32
        func = chr(func + 1072)
        decoded_text.append(func)
    return ''.join(decoded_text)

print(decrypt_function(a,keyprint))
print("\nДля первого Задания")
#Для 1го задания
file = open("text.txt", encoding='utf-8')
text = file.read()
text = re.sub("[^А-аЯ-я]", "", text)
text = text.lower()

key1 = 'ку'
key2 = 'хай'
key3 = 'хело'
key4 = 'логик'
key5 = 'телефонист'
key6 = 'неперпендикулярность'

open('text1.txt', 'w').write(encode_function(text, key1))
open('text2.txt', 'w').write(encode_function(text, key2))
open('text3.txt', 'w').write(encode_function(text, key3))
open('text4.txt', 'w').write(encode_function(text, key4))
open('text5.txt', 'w').write(encode_function(text, key5))
open('text6.txt', 'w').write(encode_function(text, key6))

print('Key1= '+key1,"\n"+encode_function(text, key1)+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key1)))
print('Key2= '+key2,"\n"+encode_function(text, key2)+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key2)))
print('Key3= '+key3,"\n"+encode_function(text, key3)+ "\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key3)))
print('Key4= '+key4,"\n"+encode_function(text, key4)+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key4)))
print('Key5= '+key5,"\n"+encode_function(text, key5)+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key5)))
print('Key6= '+key6,"\n"+encode_function(text, key6)+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key6)))
print("index vidpovidnosti BT:")
print(conformity_index(text))