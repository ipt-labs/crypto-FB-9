Keys = ["ам", "рой", "яйцо", "кошка", "абитуриент", "авиаконструктор"]
Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
            'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
t = open("texten.txt", encoding='utf-8').read()
t1 = open("nospaceslab2.txt").read()

def Index(text):
    ind = 0
    for i in range(32):
        letterCount=text.count(Alphabet[i])
        ind+=letterCount*(letterCount-1)
    ind*=1/(len(text)*(len(text)-1))
    return ind

def Blocks(text, len):
    blocks = [(text[i::len]) for i in range(len)]
    return blocks

def IndexForBlocks(text, size):
    blocks = Blocks(text, size)
    index = 0
    for i in range(len(blocks)):
        index=index+Index(blocks[i])
    index=index/len(blocks)
    return index

def Key(text, size, letter):
    blocks=Blocks(text, size)
    key = ""
    for i in range(len(blocks)):
        mostFr = max(blocks[i], key=lambda c: blocks[i].count(c))
        key+=Alphabet[(Alphabet.index(mostFr)-Alphabet.index(letter))%32]
    return key

def Enc (text):
    x = int(input("==Шифрование с длиной ключа==:\n1. 2\n2. 3\n3. 4\n4. 5\n5. 10\n6. 15\nВведите число = "))
    match x:
        case 1:
            len_key = len(Keys[0])
            keyindex = [ord (i)for i in Keys[0]]
            textindex = [ord (i) for i in text]
            encrypted = []
            for i in range(len(textindex)):
                value = (textindex[i]+keyindex[i % len_key]) % 32
                #print (value)
                encrypted.append(chr(value + 1072))
            str_enc = ''.join(encrypted)
            enc = open("encrypt1.txt", "w")
            enc.writelines(encrypted)
            enc.close()
            print("Шифрование завершено!")
            y = int(input("Хотите увидеть ИС? (0/1): "))
            match y:
                case 1:
                    a = open("encrypt1.txt").read()
                    arr = [print('Длина ключа =', i, '| ИС =', IndexForBlocks(a, i)) for i in range(1, 32)]
                    return arr
                case 0:
                    print("Ну...ну ок.")
                case _:
                    print("Не то нажал), удачи")
        case 2:
            len_key = len(Keys[1])
            keyindex = [ord(i) for i in Keys[1]]
            textindex = [ord(i) for i in text]
            encrypted = []
            for i in range(len(textindex)):
                value = (textindex[i] + keyindex[i % len_key]) % 32
                #print(value)
                encrypted.append(chr(value + 1072))
            str_enc = ''.join(encrypted)
            enc = open("encrypt2.txt", "w")
            enc.writelines(encrypted)
            enc.close()
            print("Шифрование завершено!")
            y = int(input("Хотите увидеть ИС? (0/1): "))
            match y:
                case 1:
                    a = open("encrypt2.txt").read()
                    arr = [print('Длина ключа =', i, '| ИС =', IndexForBlocks(a, i)) for i in range(1, 32)]
                    return arr
                case 0:
                    print("Ну...ну ок.")
                case _:
                    print("Не то нажал), удачи")
        case 3:
            len_key = len(Keys[2])
            keyindex = [ord(i) for i in Keys[2]]
            textindex = [ord(i) for i in text]
            encrypted = []
            for i in range(len(textindex)):
                value = (textindex[i] + keyindex[i % len_key]) % 32
                #print(value)
                encrypted.append(chr(value + 1072))
            str_enc = ''.join(encrypted)
            enc = open("encrypt3.txt", "w")
            enc.writelines(encrypted)
            enc.close()
            print("Шифрование завершено!")
            y = int(input("Хотите увидеть ИС? (0/1): "))
            match y:
                case 1:
                    a = open("encrypt3.txt").read()
                    arr = [print('Длина ключа =', i, '| ИС =', IndexForBlocks(a, i)) for i in range(1, 32)]
                    return arr
                case 0:
                    print("Ну...ну ок.")
                case _:
                    print("Не то нажал), удачи")
        case 4:
            len_key = len(Keys[3])
            keyindex = [ord(i) for i in Keys[3]]
            textindex = [ord(i) for i in text]
            encrypted = []
            for i in range(len(textindex)):
                value = (textindex[i] + keyindex[i % len_key]) % 32
                #print(value)
                encrypted.append(chr(value + 1072))
            str_enc = ''.join(encrypted)
            enc = open("encrypt4.txt", "w")
            enc.writelines(encrypted)
            enc.close()
            print("Шифрование завершено!")
            y = int(input("Хотите увидеть ИС? (0/1): "))
            match y:
                case 1:
                    a = open("encrypt4.txt").read()
                    arr = [print('Длина ключа =', i, '| ИС =', IndexForBlocks(a, i)) for i in range(1, 32)]
                    return arr
                case 0:
                    print("Ну...ну ок.")
                case _:
                    print("Не то нажал), удачи")
        case 5:
            len_key = len(Keys[4])
            keyindex = [ord(i) for i in Keys[4]]
            textindex = [ord(i) for i in text]
            encrypted = []
            for i in range(len(textindex)):
                value = (textindex[i] + keyindex[i % len_key]) % 32
                #print(value)
                encrypted.append(chr(value + 1072))
            str_enc = ''.join(encrypted)
            enc = open("encrypt5.txt", "w")
            enc.writelines(encrypted)
            enc.close()
            print("Шифрование завершено!")
            y = int(input("Хотите увидеть ИС? (0/1): "))
            match y:
                case 1:
                    a = open("encrypt5.txt").read()
                    arr = [print('Длина ключа =', i, '| ИС =', IndexForBlocks(a, i)) for i in range(1, 32)]
                    return arr
                case 0:
                    print("Ну...ну ок.")
                case _:
                    print("Не то нажал), удачи")
        case 6:
            len_key = len(Keys[5])
            keyindex = [ord(i) for i in Keys[5]]
            textindex = [ord(i) for i in text]
            encrypted = []
            for i in range(len(textindex)):
                value = (textindex[i] + keyindex[i % len_key]) % 32
                #print(value)
                encrypted.append(chr(value + 1072))
            str_enc = ''.join(encrypted)
            enc = open("encrypt6.txt", "w")
            enc.writelines(encrypted)
            enc.close()
            print("Шифрование завершено!")
            y = int(input("Хотите увидеть ИС? (0/1): "))
            match y:
                case 1:
                    a = open("encrypt6.txt").read()
                    arr = [print('Длина ключа =', i, '| ИС =', IndexForBlocks(a, i)) for i in range(1, 32)]
                    return arr
                case 0:
                    print("Ну...ну ок.")
                case _:
                    print("Не то нажал), удачи")
        case _:
            exit()
def Dec (key):
    x = int(input("Дешифровать текст?\nДа/нет(1/0): "))
    match x:
        case 1:
            with open("nospaceslab2.txt") as fp:
                for line in iter(fp.readline, ''):
                    print (line)
            len_key = len(key)
            keyindex = [ord (i)for i in key]
            textindex = [ord (i) for i in line]
            decrypted = []
            for i in range(len(textindex)):
                value = (textindex[i]-keyindex[i % len_key]) % 32
                #print (value)
                decrypted.append(chr(value + 1072))
            str_enc = ''.join(decrypted)
            enc = open("decrypt.txt", "w")
            enc.writelines(decrypted)
            enc.close()
            print("Дешифрование завершено!")
            print(''.join(decrypted))
        case 0:
            exit("Ну...Ну ок")
        case _:
            return Dec(key)
def main():
    a = int(input("Выбирайте задание:\n1. Задание 1 и 2\n2. Задание 3\n3. Выход с программы\nВведите число: "))
    b = True
    while b:
        match a:
            case 1:
                Enc(t)
                return main()
            case 2:
                print("==Cчитаем ИС==")
                arr = [print('Длина ключа =', i, '| ИС =', IndexForBlocks(t1, i)) for i in range(1, 32)]
                print("==Подсчет окончен==")
                d = int(input("Введите длину ключа = "))
                k = Key(t1, d, 'о')
                print("Ваш ключ:", k)
                k1 = str(input("Введите ключ: "))
                Dec(k1)
                return main()
            case 3:
                print("Удачи!!!")
                b = False
            case _:
                print("Чтобы выйти с программы, нажми 3")
                return main()

main()