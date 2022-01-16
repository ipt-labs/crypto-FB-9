import random
import array
import math


          ############# Задание №1 ##########

def SystemSchislenia(n):
    alpha=[]
    b = ''
    while n > 0:
        alpha.append(n%2)
        b = str(n % 2) + b
        n = n // 2 
    #print(b)
    alpha=list(reversed(alpha))
    #print(alpha)
    return alpha


def shemaGornera(x, stepen, mod):
    alpha = SystemSchislenia(stepen)
    k = len(alpha)
    y=1
    i = 0
    while i <= k-1:
        y = (y**2)%mod
        y = y * (x**alpha[i]) % mod
        i+=1
    return y



def gcd(a, b):
    if(b == 0):
        return a
    return gcd(b, a%b)

arrQ = []
def AlgorithmEuclida(mod, a):

    if mod == 0:
        return
    a = a%mod
    if a == 0:
        return

    c = mod%a
    d = mod/a

    if c == 1:
        #print(mod, " = ", int(d), "*" , a, " + ", c)
        arrQ.append(int(d))
        return arrQ
    else:
        #print(mod, " = ", int(d), "*" , a, " + ", c)
        arrQ.append(int(d))
        AlgorithmEuclida(a,c)
    return arrQ


def FindInvertedElement(a, mod):

    arrQ = AlgorithmEuclida(mod, a)

    if gcd(a, mod) != 1:
        print("Обратного элемента не существует!")
        return

    a = a%mod
    if a == 1:
        #print("Обернений елемент: ", 1)
        return 1
    else:
        x = 1
        y = 0
        q = 0

        if arrQ == None:
            return

        for i in range(len(arrQ)):
            q = x * (-arrQ[i]) + y
            y = x
            x = q

        invertedElement = q
        if invertedElement < 0:
            invertedElement = (mod + invertedElement)
        #print("Обернений елемент: ", invertedElement)
        arrQ.clear()
        return invertedElement

# Тест Миллера-Раббина на простоту
def TestMilleraRabina(p):

    if(p%2==0):
        return False
    k=10
    d = p-1
    S = 0
    while d % 2 == 0:
        d//=2
        S+=1
    
    for i in range(0, k):
        a = random.randint(1, p-1)
        isProstoe = False
        num = shemaGornera(a, d, p)
        if num == 1:
            isProstoe = True
        for r in range(0, S):
            num=shemaGornera(a, d*(2**r), p)
            if num == p-1:
                isProstoe = True
        if isProstoe == False:
            return False
    return True
    


                  ############# Задание №2 ##########
# Функция, которая генерирует пары q и p
def GenerateKeyPair():

    ot = 57896044618658097711785492504343953926634992332820282019728792003956564819969
    do = 115792089237316195423570985008687907853269984665640564039457584007913129639935

    q1 = random.randint(ot//2, do//2)*2+1
    p1 = random.randint(ot//2, do//2)*2+1
    q = random.randint(ot//2, do//2)*2+1
    p = random.randint(ot//2, do//2)*2+1


    while TestMilleraRabina(q)==False:
        q+=2
    while TestMilleraRabina(p)==False:
        p +=2
    while TestMilleraRabina(q1)==False:
        q1 +=2
    while TestMilleraRabina(p1)==False:
        p1 +=2

    if p*q>p1*q1:
        tempQ = q1
        tempP = p1
        q1 = q
        p1 = p
        q = tempQ
        p = tempP
    return p, q, p1, q1


                  ############# Задание №3 ##########      
# функция, которая генерирует ключи        
def RSA(p, q):
    n = p*q
    fiOtN= (p-1)*(q-1)
    e = random.randint(2, fiOtN)

    while gcd(e, fiOtN) !=1 :
        e+=1

    d = FindInvertedElement(e, fiOtN)
    PrivateKeys = [d, p, q]
    PublicKeys = [n, e]

    print("\t\tprivate key:", "\nd: ", d, "\np: ", p, "\nq: ", q, "\n\t\tpublic key: ", "\nn: ", n, "\ne: ", e, "\n")
    
    return PrivateKeys, PublicKeys


                  ############# Задание №4 ##########
# Функция шифрования собщения
def Encrypt(M, PublicKeys):
    n = PublicKeys[0]
    e = PublicKeys[1]
    C = shemaGornera(M, e, n)
    print("Encrypted Text: ", C)
    return C

# Функция расшифрования сообщения
def Decrypt(C, PrivateKeys):
    d = PrivateKeys[0]
    p = PrivateKeys[1]
    q = PrivateKeys[2]
    n = p*q
    M = shemaGornera(C, d, n)
    print("Decrypted Text: ", M)
    return M
# Функция получения цифровой подпси
def Sign(M, PrivateKeys):
    d = PrivateKeys[0]
    p = PrivateKeys[1]
    q = PrivateKeys[2]
    n = p*q

    S = shemaGornera(M, d, n)
    print("\nSignature:", "\nM: ", M, "\nS: ", S)
    return M, S

# Функция, в которой провереется правильность цифровой подписи
def Verify(sign, PublicKeys):
    n = PublicKeys[0]
    e = PublicKeys[1]
    M = sign[0]
    S = sign[1]
    test=shemaGornera(S, e, n)
    if M == shemaGornera(S, e, n):
        print(" :) ")
        return True
    else:
        print(" :( ")
        return False


                  ############# Задание №5 ##########


# функция отправки зашифрованного текста
def SendKey(BPublicKeys, APrivateKeys, M):
    C = Encrypt(M, BPublicKeys)
    signature = Sign(C, APrivateKeys)
    S = signature[1]
    return C, S


# функция получения сообщения, расшифровывание сообщения, проверка цифровой подписи
def ReceiveKey(APublicKeys, BPrivateKeys, sign):
    C = sign[0]
    Verify(sign, APublicKeys)
    M = Decrypt(C, BPrivateKeys)
    return M



pq = GenerateKeyPair()
p = pq[0] 
q = pq[1]
p1 = pq[2]
q1 = pq[3]

print("\t\t\t\tFor A")
KeysForA = RSA(p, q)
print("\t\t\t\tFor B")
KeysForB = RSA(p1, q1)
APrivateKeys = KeysForA[0]
APublicKeys = KeysForA[1]
BPrivateKeys = KeysForB[0]
BPublicKeys = KeysForB[1]


    

# отправка сообщения от А к В
print("Enter Message: ", end='')
M = int(input())
CS = SendKey(BPublicKeys, APrivateKeys, M)
ReceiveKey(APublicKeys, BPrivateKeys, CS)




# функции, которые проверют корректность работи программы с помощью сайта
def VerifySite_1():
    #генерируем ключи на сайте, шифруем в программе, расшифровуем на сайте
    e = int("10001", 16)
    n = int("810EEE9AD50DC862DD031A82E1961D9EAAAB7C320EC0A421E26DB3024D7F03B9", 16)
    publicKey = n, e
    # encryption
    M = int("969", 16)
    C = Encrypt(M, publicKey)
    print("Encrypted message: " + str(hex(C)))

    #генерируем цифровую подпись на сайте, проверяем в программе
    S = int("0859F7D2C01D4D2DBFE953A25BD550A9B83A1572818193B1C6681B0B5A2A1FF9", 16)     
    print("Sign: " + str(hex(S)))
    sign = [M, S]
    Verify(sign, publicKey)

    

def VerifySite_2():
    #генерируем ключи в программе, шифруем на сайте, расшифровуем в программе
    pq = GenerateKeyPair()
    p = pq[0]
    q = pq[1]
    keys = RSA(p, q)
    privateKeys = keys[0]
    publicKeys = keys[1]
    n = publicKeys[0]
    e = publicKeys[1]

    print("hex(e): ", hex(e), "\nhex(n): ", hex(n))
    print("enter C: ", end='')
    ChiperText = input()
    C = int(ChiperText, 16)
    m = Decrypt(C, privateKeys)
    print("Decrypted message: ", hex(m))


    #генерируем цифровую подпись в программе, проверяем на сайте
    sign = Sign(m, privateKeys)
    S = sign[1]
    print("signature: ", hex(S))


VerifySite_1()
VerifySite_2()