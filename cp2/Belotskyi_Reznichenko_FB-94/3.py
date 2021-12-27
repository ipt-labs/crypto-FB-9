from itertools import permutations
file1 = open("1.txt", "r").read()
file2 = open("2.txt", "w")
file3 = open("result.txt", "r").read()

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

bigram1 = list(permutations([['с', 'т'], ['н', 'о'], ['т', 'о'], ['н', 'а'], ['е', 'н']], 2))
bigram2 = list(permutations([['р', 'н'], ['ы', 'ч'], ['н', 'к'], ['ц', 'з'], ['и', 'а']], 2))

#Розширений алгоритм Евкліда
def euclid_ext(a, n):
    if n == 0:
        return a, 1, 0
    else:
        d, x, y = euclid_ext(n, a % n)
        return d, y, x - y * (a // n)

#Пошук оберненого
def reverse(a, n):
    gcd, x, y = euclid_ext(a, n)
    if gcd == 1:
        return (x % n + n) % n
    else:
        return False

#Обробка окремих випадків
def euclid(a, y, n):
    gcd, y1, x1 = euclid_ext(a, n)
    if gcd == 1:         # знаходимо обернений
        x = reverse(a,n)
        return x
    elif y % gcd != 0: # немає розв`язкі
        return False
    else:
        euclid(a/gcd, y/gcd, n/gcd)

#Функція пошуку найчастіших біграм
def max_bigram(text):
    mass = []
    mass1 = []
    line = [text[k:k + 2] for k in range(0, len(text), 2)]
    new_line = set(line)
    for i in new_line:
        number = line.count(i)
        mass.append([i, number])
    sorted_bigrams = sorted(mass, key=lambda x: x[1])
    for i in range(5):
        mass1.append(sorted_bigrams[-(i+1)])
        mass.clear()
    for i in range(len(mass1)):
        mass.append(mass1[i][0])
    print(mass)

#Функція пошуку індексу відповідності
def compliance_index(text):
    arr = []
    for i in alphabet:
        letter = text.count(i)
        arr.append(letter * (letter-1))
    I = sum(arr) / (len(text)*(len(text)-1))
    return I

#Функція для пошуку Х та У для роз'язку системи
def index():
    mass = []
    arr = []
    for i in range(len(bigram1)):
        for j in range(len(bigram2)):
            mass.append(bigram1[i] + bigram2[j])
    for j in mass:
        X1 = alphabet.index(j[0][0]) * 31 + alphabet.index(j[0][1])
        Y1 = alphabet.index(j[2][0]) * 31 + alphabet.index(j[2][1])
        X2 = alphabet.index(j[1][0]) * 31 + alphabet.index(j[1][1])
        Y2 = alphabet.index(j[3][0]) * 31 + alphabet.index(j[3][1])
        #print(f'{X1=}, {Y1=}, {X2=},{Y2=}')
        arr.append([X1, Y1, X2, Y2])
    return arr

#Функція пошуку ключів
def find_key():
    mass = []
    XY = index()
    for i in range(len(XY)):
        X1 = XY[i][0]
        Y1 = XY[i][1]
        X2 = XY[i][2]
        Y2 = XY[i][3]
        a = (euclid(X1 - X2, Y1 - Y2, 31 ** 2) * (Y1 - Y2)) % (31 ** 2)
        b = (Y1 - a * X1) % (31 ** 2)
        mass.append([a, b])
    return mass

#Функція розшифрування
def decrypt(text):
    arr = []
    arr1 = []
    AB = find_key()
    line = [text[k:k + 2] for k in range(0, len(text), 2)]
    for j in range(len(AB)):#цикл розшифрування одного й того самого тексту для різних ключів
        for i in range(len(line)):
            A = AB[j][0]
            B = AB[j][1]
            Y = alphabet.index(line[i][0])*31 + alphabet.index(line[i][1])#знаходимо біграму У
            X = (reverse(A, 31**2) * (Y - B)) % 31**2#знаходимо біграму Х
            arr.append(X)
        for i in range(len(arr)):
            letter = alphabet[arr[i] // 31] + alphabet[arr[i] % 31]#знаходимо букву в залежності від біграми Х
            arr1.append(letter)
        answer = ''.join(arr1)
        arr1.clear()
        arr.clear()
        
#аналізатор російської мови
        if 0.47 <= compliance_index(file3) and compliance_index(file3) <= 0.67 and (answer.count('о')/len(answer) < 0.11 or answer.count('а')/len(answer) < 0.06):
            continue
        else:
            print(answer)
            return file2.write(answer)

