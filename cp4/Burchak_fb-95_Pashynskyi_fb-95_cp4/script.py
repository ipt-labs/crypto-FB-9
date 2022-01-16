import random


# ф-я знаходження найбільшого спільного дільника
def nsd(a, m):
    if a == 0:
        return (m, 0, 1)
    else:
        d, y, x = nsd(m % a, a)
        return (d, x - (m // a) * y, y)


# ф-я знаходження оберненого елемента
def re(a, m):
    d, x, y = nsd(a, m)
    if d != 1:
        return 0
    else:
        return x % m


# тест числа на простоту
def Miller_Rabin_Test(num):
    # попередні перевірки
    if (num == 2) or (num == 3):
        return True
    if (num % 2 == 0) or (num % 3 == 0) or (num % 5 == 0) or (num % 7 == 0):
        return False
    if (num < 2):
        return False

    # num - 1 = 2^s * t
    t, s = num - 1, 0
    while t % 2 == 0:
        t = t // 2
        s += 1

    # раунди тесту (чим більше раундів - тим більша ймовірність отримати вірний результат)
    for i in range(228):
        a = random.randint(2, num - 2)
        x = pow(a, t, num)  # x = (a^t)mod(num)
        if (x == num - 1) or (x == 1):
            continue    # перехід на наступний раунд
        x = pow(x, 2, num)  # x = (x^2)mod(num)
        if x == 1 or x != num - 1:
            return False  # число не просте
    return True  # число пройшло всі перевірки і скоріш за все просте


# ф-я, що генерує довільне просте число
def Generate_Random_Simple_Num():
    bibr = 1
    while bibr == 1:
        bit_arr = []
        bit_arr.append(str(1))
        for i in range(255):
            bit_arr.append(str(random.randint(0, 1)))
        bits = ''.join(bit_arr)
        # print(bits)
        num = int(bits, 2)
        # print(str(num))
        if Miller_Rabin_Test(num):
            bibr = 0
            return num


# ф-я генерації p, q для абонента А i p1, q1 для абонента B
def Generate_P_Q():
    bibr = 1
    while bibr == 1:
        p_q = []
        p1_q1 = []
        for i in range(2):
            p_q.append(Generate_Random_Simple_Num())
            p1_q1.append(Generate_Random_Simple_Num())
        pq = p_q[0] * p_q[1]
        p1q1 = p1_q1[0] * p1_q1[1]
        if pq <= p1q1:
            bibr = 0
            return p_q, p1_q1


# ф-я генерації public та private ключів
def RSA_Key_Gen(p, q):
    n = p * q   # обчислення модуля
    fi = (p - 1) * (q - 1)  # ф-я Ейлера
    bibr = 1
    while bibr == 1:
        e = random.randint(2, fi)   # public key
        g, x, y = nsd(e, fi)
        if g == 1:
            bibr = 0
    d = re(e, fi)   # private key
    public_key = (e, n)
    private_key = (d, p, q)
    return public_key, private_key


# ф-я шифрування повідомлення
def RSA_Encryption(m, pub_key):
    e = pub_key[0]
    n = pub_key[1]
    C = pow(m, e, n)    # c = (m^e)modn
    return C


# ф-я розшифрування повідомлення
def RSA_Decryption(C, pr_key):
    d = pr_key[0]
    n = pr_key[1] * pr_key[2]
    P = pow(C, d, n)    # p = (c^d)modn
    return P


# ф-я генерації ЦП
def RSA_Sign_Gen(m, pr_key):
    d = pr_key[0]
    n = pr_key[1] * pr_key[2]
    S = pow(m, d, n)    # s = (m^d)modn
    return S


# ф-я перевірки ЦП
def RSA_Verify_Sign(S, pub_key, M):
    e = pub_key[0]
    n = pub_key[1]
    if pow(S, e, n) == M:
        print("Signature Verification successfull")
        return 1
    else:
        print("Signature verification failure")
        # print("Real encrypted: " + str(C))
        # print("Fake: " + str(pow(S, e, n)))
        return 0


# ф-я відправки зашифрованого повідомлення
def Send_Message(pub_, _pr, m):
    # шифрування повідомлення з відкритим ключем отримувача
    C = RSA_Encryption(m, pub_)
    # підписання з закритим ключем відправника
    S = RSA_Sign_Gen(C, _pr)

    print("Message after encryption:\n" + str(C))
    print("Didital Signature:\n" + str(S))
    return C, S


# ф-я отримання повідомлення, перевірки ЦП і розшифровки отримувачем
def Receive_Message(_pub, pr_, C, S):
    # перевірка ЦП
    RSA_Verify_Sign(S, _pub, C)
    P = RSA_Decryption(C, pr_)
    print("Message after decryption:\n" + str(P))
    return P


p_q, p1_q1 = Generate_P_Q()
A_pub, A_pr = RSA_Key_Gen(p_q[0], p_q[1])   # генерація ключів для А
B_pub, B_pr = RSA_Key_Gen(p1_q1[0], p1_q1[1])   # генерація ключів для B

# збереження параметрів в файл
f = open(".\\data_dump.txt", "w")
s = "\tPair for A:\n" + "p: " + str(p_q[0]) + "\nq: " + str(p_q[1])
s += "\n\tPair for B:\n" + "p1: " + str(p1_q1[0]) + "\nq1: " + str(p1_q1[1])
s += "\n\tA Public key:\n" + "e: " + str(A_pub[0]) + "\nn: " + str(A_pub[1])
s += "\n\tA Private key:\n" + "d: " + \
    str(A_pr[0]) + "\np: " + str(A_pr[1]) + "\nq: " + str(A_pr[2])
s += "\n\tB Public key:\n" + "e: " + str(B_pub[0]) + "\nn: " + str(B_pub[1])
s += "\n\tB Private key:\n" + "d: " + \
    str(B_pr[0]) + "\np: " + str(B_pr[1]) + "\nq: " + str(B_pr[2])
f.write(s)
f.close()


print("\n---------------------------------------------------------------------------------------------------------------")
# процес відправки повідомлення від А до В
print("A --> B")
M = random.randint(0, A_pub[1] - 1)  # повідомлення
print("Message to transfer:\n" + str(M))
C, S = Send_Message(B_pub, A_pr, M)
Receive_Message(A_pub, B_pr, C, S)

print("---------------------------------------------------------------------------------------------------------------")


# ф-я для перевірки коректності роботи реалізованих ф-й за допомогою сайту
def Server_Check():
    # server key
    e = int("10001", 16)
    n = int("84B29D74642F5E9CFA52E4677818722C6220A71C64FBB569610602B74356B603", 16)
    serv_key = e, n
    # encryption
    M = int("666", 16)
    C = RSA_Encryption(M, serv_key)
    print("Encrypted message: " + str(hex(C)))
    # signing
    S = int("23991792CE76804AF686D5CA8821878BF8841C846DF2B79BF9162747835949DD", 16)
    print("Digital Sign: " + str(hex(S)))
    RSA_Verify_Sign(S, serv_key, M)


Server_Check()
