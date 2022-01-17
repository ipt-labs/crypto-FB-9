from collections import Counter
import re

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

file = open("var3.txt", "r", encoding='utf-8')
a = file.read().lower().replace("\n", "")


def encode_function(text, key):
    encoded_text = []
    key_index=[]
    for i in key:
        key_index.append(alphabet.index(i))
    for x,y in enumerate(text):
        add=alphabet[(alphabet.index(y) + key_index[x % len(key)]) % 32]
        encoded_text.append(add)
    return ''.join(encoded_text)

def conformity_index(text):
    index=0
    for i in Counter(text):
        index += Counter(text)[i]*(Counter(text)[i]-1)
    index = index/(len(text)*(len(text)-1))
    return index



def find_key(text):
    key = []
    for word_length in range(2,32):
        index_sum = 0
        for i in range(word_length):
            a = ""
            for j in range(i, len(text), word_length):
                a+=text[j]

            #print(conformity_index(''.join(a)))
            index_sum += conformity_index(''.join(a))
            #print(a)
        key.append(index_sum/word_length)
    nearest_val = max(key)
    print(key.index(nearest_val) + 2)
    print(nearest_val)
    
    print(key)


find_key(a)

def key_value(text, key_length):
    b = []
    k = []
    for i in range(key_length):
        z = ''
        for j in range(i, len(text), key_length):
            #Текст по "блокам"
            z +=text[j]
        b.append(z)
    #print(b,"qwe")
    for l in range(key_length):
        most_popular_fragment = list(dict(Counter(b[l]).most_common(1)).keys())[0]
        x = (alphabet.index(most_popular_fragment) - 14 ) % 32
        x = alphabet[x]
        k.append(x)
        #Адекватный ключик в строку
    return k

keyf = ''.join(key_value(a, 14))
print("\nКлюч який пропонує программа:" +keyf)



keyprint = ['э', 'к', 'о', 'м', 'а', 'я', 'т', 'н', 'и', 'к', 'ф', 'у', 'к', 'о']
print("\nНаш ключ:")
print(keyprint)

def decrypt_function(text, key):
    decoded = []
    key_index=[]
    for i in key:
        key_index.append(alphabet.index(i))
    for x,y in enumerate(text):
        add=alphabet[(alphabet.index(y) - key_index[x % len(key)]) % 32]
        decoded.append(add)
    return ''.join(decoded)

print(decrypt_function(a,keyprint))
print("\nДля первого Задания")
#Для 1го задания
file = open("text.txt", encoding='utf-8')
text = file.read().lower().replace("\n", "")
text = re.sub("[^А-аЯ-я]", "", text)

key_list=['ку', 'хай', 'хело','логик','телефонист','неперпендикулярность']


open('text1.txt', 'w').write(encode_function(text, key_list[0]))
open('text2.txt', 'w').write(encode_function(text, key_list[1]))
open('text3.txt', 'w').write(encode_function(text, key_list[2]))
open('text4.txt', 'w').write(encode_function(text, key_list[3]))
open('text5.txt', 'w').write(encode_function(text, key_list[4]))
open('text6.txt', 'w').write(encode_function(text, key_list[5]))

print('Key1= '+key_list[0],"\n"+encode_function(text, key_list[0])+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key_list[0])))
print('Key2= '+key_list[1],"\n"+encode_function(text, key_list[1])+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key_list[1])))
print('Key3= '+key_list[2],"\n"+encode_function(text, key_list[2])+ "\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key_list[2])))
print('Key4= '+key_list[3],"\n"+encode_function(text, key_list[3])+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key_list[3])))
print('Key5= '+key_list[4],"\n"+encode_function(text, key_list[4])+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key_list[4])))
print('Key6= '+key_list[5],"\n"+encode_function(text, key_list[5])+"\nindex vidpovidnosti:")
print(conformity_index(encode_function(text, key_list[5])))
print("index vidpovidnosti BT:")
print(conformity_index(text))