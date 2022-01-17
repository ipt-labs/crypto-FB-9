with open("decryption.txt", "r", encoding="utf-8") as reader:
    pre = reader.read()
    text = pre.lower().replace(",","").replace("!","").replace("?","").replace(".","").replace(":","").replace(";","").replace("\n","").replace("ё","е").replace("-","").replace("—","").replace("\xa0","").replace("[","").replace("]","").replace("(","").replace(")","").replace("…","").replace("=","").replace("*","").replace("/","").replace(" ","")
    r = 2
    c = 0
    isch = []


    #индекс соответствия
    def affinity_index(tekst):
        chars = {}
        summa = 0
        for i in range(len(tekst)):
            ch = tekst[i]
            if ch not in chars:
                chars[ch] = 0
            chars[ch] += 1
        for k, v in chars.items():
            summa += v * (v - 1)
        result = summa/(len(tekst)*(len(tekst)-1))
        return result

    #среднее значение величин элементов списка
    def avg(isch):
        return sum(isch)/len(isch)

 
    #Поиск самой часто встречаемой буквы
    def char_freq(t):
        ch_fr = {}
        for i in range(len(t)):
            ch = (t[i])
            if ch not in ch_fr:
                ch_fr[ch] = 0
            ch_fr[ch] += 1
        v=list(ch_fr.values())
        k=list(ch_fr.keys())
        return k[v.index(max(v))]



    #предполагаем, что в каждом блоке самая часто встречаемая буква - "о"
    def potencial_k1(r):
        c = 0
        potencial_key = []
        while c < r:
            often_y = alphabet[char_freq(text[c::r])]
            often_in_language = alphabet['о']
            key_num = (often_y - often_in_language) % 32
            potencial_key.append(get_letter(key_num))
            c += 1
        p_k = "".join(potencial_key)
        print(p_k)
        return p_k


    #подправляем вышеуказанную функцию
    def potencial_k2(r):
        c = 0
        potencial_key = []
        while c < r:
            if c == 7:
                often_y = alphabet[char_freq(text[c::r])]
                often_in_language = alphabet['г']
                key_num = (often_y - often_in_language) % 32
                potencial_key.append(get_letter(key_num))
                c += 1
            elif c == 8:
                often_y = alphabet[char_freq(text[c::r])]
                often_in_language = alphabet['е']
                key_num = (often_y - often_in_language) % 32
                potencial_key.append(get_letter(key_num))
                c += 1
            elif c == 15:
                often_y = alphabet[char_freq(text[c::r])]
                often_in_language = alphabet['а']
                key_num = (often_y - often_in_language) % 32
                potencial_key.append(get_letter(key_num))
                c += 1
            else:
                often_y = alphabet[char_freq(text[c::r])]
                often_in_language = alphabet['о']
                key_num = (often_y - often_in_language) % 32
                potencial_key.append(get_letter(key_num))
                c += 1
        p_k = "".join(potencial_key)
        print(p_k)
        return p_k



    #на вход - буква, на выход - ее число (из словаря alphabet)       
    def char_number(letter):
        number = alphabet[letter]
        return number

    #на вход - число, на выход - буква (из словаря alphabet)
    def get_letter(num):
        for k, v in alphabet.items():
            if v == num:
                return k

    #функция образования исходной буквы 
    def rotate(letter_char, key_char):
        return get_letter((char_number(letter_char) - key_char) % 32)


    #дешифровка
    def decoding(key):
        decrypted = []    
        starting_index = 0
        for letter in text:
            rotation = char_number(key[starting_index])            
            decrypted.append(rotate(letter, rotation))             

            if starting_index == (len(key) - 1): 
                starting_index = 0
            else: 
                starting_index += 1
        res = ''.join(decrypted) 
        return res


    


    alphabet = {}
    bukva_a = ord('а')
    nomer = 0
    for i in range(bukva_a, bukva_a + 32):
        alphabet[chr(i)] = nomer
        nomer +=1
    #print(alphabet)
    '''{'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9, 'к': 10, 'л': 11,

        'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 

        'ч': 23, 'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27, 'ь': 28, 'э': 29, 'ю': 30, 'я': 31}'''
    
    while r <= int(len(text)/40):
        while c < r:
            isch.append(affinity_index(text[c::r]))
            c += 1
        if c == r:
            z = avg(isch)
            if(0.05 < z and z < 0.06):
                print("Возможный ключ V1:")
                potencial_k1(r)
                print("\nВозможный ключ V2:")
                potencial_k2(r)
                print()
                ###############################################################################
                '''Далее ключ подбирался вручную на основании ранее полученных возможных ключей, 
                   а также частично проявившихся читаемых кусков слов в дешифрованном тексте.
                   В итоге получился ключ, помещенный в файл remote_key.txt'''
                ###############################################################################
                with open("remote_key.txt", "r", encoding="utf-8") as r:
                    re = r.read()
                    kluch = re.lower().replace(",","").replace("!","").replace("?","").replace(".","").replace(":","").replace(";","").replace("\n","").replace("ё","е").replace("-","").replace("—","").replace("\xa0","").replace("[","").replace("]","").replace("(","").replace(")","").replace("…","").replace("=","").replace("*","").replace("/","").replace(" ","")
                    with open("remote_decoded_text.txt", "w", encoding="utf-8") as writer:
                        writer.write(decoding(kluch))
                    print("\n+++++++++KEY+++++++++\n" + "+ " + kluch + " +\n" + "+++++++++++++++++++++\n")
                    print("+Decrypted text:\n" + decoding(kluch))
                break
            else:
                isch.clear()    
        r += 1
        c = 0

    

    

    



        
           