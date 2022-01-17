with open("text.txt", "r", encoding="utf-8") as reader:
    pre = reader.read()
    text = pre.lower().replace(",","").replace("!","").replace("?","").replace(".","").replace(":","").replace(";","").replace("\n","").replace("ё","е").replace("-","").replace("—","").replace("\xa0","").replace("[","").replace("]","").replace("(","").replace(")","").replace("…","").replace("=","").replace("*","").replace("/","").replace(" ","")

    l = len(text)

    #Алфавит из 32 букв (БЕЗ "Ё": "Ё" == "Е")
    alphabet = {}
    bukva_a = ord('а')
    nomer = 0
    for i in range(bukva_a, bukva_a + 32):
        alphabet[chr(i)] = nomer
        nomer +=1
    
    #на вход - буква, на выход - ее число (из словаря alphabet)
    def char_number(letter):
        number = alphabet[letter]
        return number
        
    #Ключи
    keys = {'key2': 'ом',
            'key3': 'куб',
            'key4': 'роль',
            'key5': 'въезд',
            'key18': 'родионраскольников'}

    #на вход - число, на выход - буква (из словаря alphabet)
    def get_letter(num):
        for k, v in alphabet.items():
            if v == num:
                return k

    #функция образования шифрованной буквы
    def rotate(letter, rot):
        return get_letter((char_number(letter) + rot) % 32)

    #шифрование
    def encrypt(text, key):
        encrypted = []    
        starting_index = 0
        for letter in text:
            rotation = char_number(key[starting_index])            
            encrypted.append(rotate(letter, rotation))             

            if starting_index == (len(key) - 1): 
                starting_index = 0
            else: 
                starting_index += 1
        res = ''.join(encrypted)        
        return res

    #функція обчислення індексу відповідності
    def affinity_index(tekst):
        chars = {}
        summa = 0
        for i in range(l):
            ch = tekst[i]
            if ch not in chars:
                chars[ch] = 0
            chars[ch] += 1
        for k, v in chars.items():
            summa += v * (v - 1)
        result = summa/(l*(l-1))
        return result

        

    with open('Encrypted_own_text.txt', 'w') as f:
        f.write("***Открытый текст:\n" + text + '\n'*2 + "***Шифрованные тексты:\n" + '\n')
        for n, z in keys.items():
            f.write("--" + n+':' + " " + z + '\n' + encrypt(text,z) + '\n'*3)


    with open('Affinity_index.txt', 'w') as f:
        f.write("***Открытый текст:" + '\n'*2 + str(affinity_index(text)) + '\n'*3)
        f.write("***Шифрованные тексты:" + '\n'*2)
        for n, z in keys.items():
            f.write("--" + n+':' + " " + z + '\n' + str(affinity_index(encrypt(text,z))) + '\n'*2)
            




            