import random

def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        d, x, y = gcd(b % a, a)
    return (d, y - (b // a) * x, x)

def millerrabin_test(n):
    for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
        if n % prime == 0:
            return False
    if n == 3 or n == 2: # числа прості
        return True
    if n < 2 or n % 2 == 0: # парні тому не прості
        return False
    else:
        s = 0 # встановлюемо лічильник
        d = n - 1 # для розкладу
        while d % 2 == 0: # пока d \ на 2, увеличиваем счетчик
            s += 1
            d = d // 2
        for i in range(6):
            a = random.randrange(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for i in range(1, s):
                x = pow(x, 2, n)
                if x == 1:
                    return False
                if x == n - 1:
                    break
            if x != n - 1:
                return False
        return True

def KeyPair(bits): # парu простих чисел
    p_q = []
    i = False
    while i == False:
        p = random.getrandbits(bits-1) + (1 << bits-1)
        #print(p)
        i = millerrabin_test(p)
    p_q.append(p)
    i = False
    while i == False:
        q = random.getrandbits(bits-1) + (1 << bits-1)
        #print(q)
        i = millerrabin_test(q)
    p_q.append(q)
    return p_q

def Encrypt_message(message, e, n): #зашифрування
    if message > n - 1:
        print('Long message')
        return 0
    c_message = pow(message, e, n)
    return c_message

def Decrypt(c_message, d, n): #розшифрування
    d_message = pow(c_message,d,n)
    return d_message

def Sign(message, d, n):
    signature = pow(message, d, n)# message ** d % n
    return signature

def Verify(sign, e, n, message):
    m_s = Encrypt_message(sign, e, n) # sign ** e % n
    if m_s == message:
        return True
    else:
        return False

def SendKey(e1, n1, message): # Аліса відправляє n, e  k == message
    mes = Encrypt_message(message, e1, n1)
    p_and_q = KeyPair(256)  # Aліса генерує свою пару
    n = p_and_q[0] * p_and_q[1]
    while n > n1:
        p_and_q = KeyPair(256)
        n = p_and_q[0] * p_and_q[1]
    f = (p_and_q[0] - 1) * (p_and_q[1] - 1)
    if gcd(e, f)[0] != 1 :
        d= false
    else :
        d = (gcd(e, f)[1] % f + f) % f
    s = Sign(message, d, n)
    sign = Encrypt_message(s, e1, n1)
    return mes, sign, n

def ReceiveKey(message, signature, e, n): # Боб отримує повідомлення і розшифровує
    text = Decrypt(message, d1, n1)
    d_signature = Decrypt(signature, d1, n1)
    rs = Verify(d_signature, e, n, text)
    return text, rs


text = 123456789
e = 2 ** 16 + 1
p_and_q = KeyPair(256)  # пара для вк
f = (p_and_q[0] - 1) * (p_and_q[1] - 1)

if gcd(e, f)[0] != 1 :
    d1= false
else :
    d1 = (gcd(e, f)[1] % f + f) % f

n1 = p_and_q[0] * p_and_q[1]
print('шт з підписом')
message, signature, n = SendKey(e, n1, text)
print(message)
print('верифікований вт')
t, res = ReceiveKey(message, signature, e, n)
print((t))
print(res)

#Перевірка на сайті
print('------------перевірка на сайті-----------')
print('ключ: ')
k = random.randint(1, 965)
print(k)
e = 2 ** 16 + 3
e1 =2 ** 16 + 1
n1 = (int('C096C592FDD3D0B7BB7B34A6B5456BDA9B88D22D75AB977E6A23105D408BCF47DBD7316B5BB82AEA0E3602D348F2F1FD976D6A8F1AE19259CE6AE685C6DB60B9',16))
mes, Signature, n = SendKey(e1,n1,k)
print(hex(mes))
print('Signature: ', hex(Signature))
print('Modulus: ', hex(n))