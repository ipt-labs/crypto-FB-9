from random import randrange
from math import gcd


# розширений алгоритм Евкліда
def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b//a)*x1
    y = x1
    return g, x, y


# обернений елемент
def find_reverse_element(a, mod):
    gcd, x, y = gcd_extended(a, mod)
    if gcd == 1:
        return (x % mod + mod) % mod
    else:
        return -1


# тест Мілера-Рабіна простоти числа
def miller_rabin(num):

    if num % 2 == 0 or num % 3 == 0 or num % 5 == 0 or num % 7 == 0:
        return False

    d = num - 1
    r = 0

    while d % 2 == 0:
        d //= 2
        r += 1
    a = randrange(2, num-1)
    x = pow(a, d, num)
    if x == 1 or x == num-1:
        return True
    while r > 1:
        x = pow(x, x, num)
        if x == 1:
            return False
        if x == -1:
            return True
        r -= 1
    return False


# генерація простого великого числа
def gen_prime(bits):
    while True:
        a = (randrange(1 << bits - 1, 1 << bits) << 1) + 1
        if miller_rabin(a):
            return a
        else:
            with open("not_passed_test.txt",'a') as file:
                file.writelines("Test not passed "+str(a)+'\n')


# генерація чотирьох простих чисел
def gen_numbers_pair():
    pair = []
    for i in range(4):
        pair.append(gen_prime(256))
    while pair[0]*pair[1] >= pair[2]*pair[3]:
        pair = []
        for i in range(4):
            pair.append(gen_prime(256))
    return pair


# генерування публічного та приватного ключа
def generate_key_pair(p, q):
    n = p*q
    euler = (p-1)*(q-1)

    e = randrange(2, euler)
    while gcd(e, euler) != 1:
        e = randrange(2, euler)

    d = find_reverse_element(e, euler)

    return [e, n], [d, p, q]


# шифрування
def encrypt(msg, public_key):
    return pow(msg, public_key[0], public_key[1])


# розшифрування
def decrypt(encrypted_msg, private_key):
    return pow(encrypted_msg, private_key[0], private_key[1]*private_key[2])


# цифровий підпис
def sign(msg, private_key):
    return pow(msg, private_key[0], private_key[1]*private_key[2])


# перевірка цифрового підпису
def verify(msg, sign, public_key):
    return pow(sign, public_key[0], public_key[1]) == msg


# процедура протоколу - надсилання
def send_key(k, public, private):
    k1 = encrypt(k, public)
    s = sign(k, private)
    s1 = encrypt(s, public)
    return k1, s1


# процедура протоколу - отримання та верифікація повідомлення
def recieve_key(k1, s1, private, public):
    k = decrypt(k1, private)
    s = decrypt(s1, private)
    if verify(k, s, public):
        print("message: ",k)
        print("message verified! ")
    else:
        print("message not verified!")
    return k, s


# тестували "локально"
def my_test():
    # згенерували 4 простих числа
    #p, q, p1, q1 = gen_numbers_pair()
    p = 199678154031684671539430416713290906166999585391355487044350862215685268344879
    q = 205174100210673205200058779618100018279183148869024122379502109050216467008623
    p1 = 226252153381013260702479181319917934576168461407559243409221620798063872767099
    q1 = 186914172463734799398029317962633444089705791146136750986504945743094240325439

    print('\n')
    print("p = ", p)
    print("q = ", q)
    print("p1 = ", p1)
    print("q1 = ", q1)
    print("\n")

    # згенерували публічні та приватні ключі Бобу та Алісі
    alice_public, alice_private = generate_key_pair(p, q)
    bob_public, bob_private = generate_key_pair(p1, q1)

    # наше повідомлення
    msg = 12345678901234567890

    print("Alice public key: (e,n)", alice_public)
    print("Alice private key: (d,p,q)", alice_private)
    print("Bob public key: (e1,n1)", bob_public)
    print("Bob private key: (d1,p1,q1)", bob_private)
    print('\n')

    # частина для Аліси
    encrypted_alice = encrypt(msg,alice_public)
    print("Encrypted message by Alice:",encrypted_alice)
    decrypted_alice = decrypt(encrypted_alice,alice_private)
    print("Decrypted message by Alice:",decrypted_alice)

    # Аліса підписала повідомлення та перевірили його
    alice_sign = sign(msg,alice_private)
    print("Signature for Alice:",alice_sign)
    print("Sign check: ",verify(msg,alice_sign,alice_public))
    print("\n")

    # частина Боба
    encrypted_bob = encrypt(msg, bob_public)
    print("Encrypted message by Bob:", encrypted_bob)
    decrypted_bob = decrypt(encrypted_bob, bob_private)
    print("Decrypted message by Bob:", decrypted_bob)

    # Боб підписав повідомлення - ми його перевірили
    bob_sign = sign(msg, bob_private)
    print("Signature for Bob:", bob_sign)
    print("Sign check: ", verify(msg, bob_sign, bob_public))
    print("\n")

    # протокол обміну
    k1,s1 = send_key(msg,bob_public,alice_private)
    recieve_key(k1,s1,bob_private,alice_public)


def int_to_hex(number):
    return hex(number)[2:].upper()


def hex_to_int(hex_value):
    return int(hex_value, 16)


def encode_to_hex(string):
    string = (string.encode('utf-8'))
    return string.hex().upper()


def decode_from_hex(hex_value):
    return bytes.fromhex(hex_value).decode('utf-8')


def sever_test():
    # ключ з сервера
    modulus = 'B2243C28EB7E4C3DBF93BE6F37A2EE39489549857E793FB6FD1567D43ED5D5D7'
    exp = '10001'

    server_open = [hex_to_int(exp),hex_to_int(modulus)]

    msg = 'Great! We did it!'

    # складові нашого ключа (згенеровані у 1 частині для Аліси)
    e = 31811810397541411518390776294835057193314687426271862377448009668698747444709905182745849045723700219230766301737381579326438243281828096105520784648772369
    n = 40968785585179110685184299376332342832605494307488528671728507393914766727141639329418216226852424329933127753248984922917069362009463494923614991430891617
    d = 7195740480726333941257813343609756758476520065810118550975628695567716773384083132290873373314233700176193109954563146216146339386404509588001316335249745
    p = 199678154031684671539430416713290906166999585391355487044350862215685268344879
    q = 205174100210673205200058779618100018279183148869024122379502109050216467008623

    my_open = [e,n]
    my_private = [d,p,q]


    # site encryption
    print('mod =', int_to_hex(n))
    print('e = ', int_to_hex(e))
    enc = encrypt(hex_to_int(encode_to_hex(msg)),my_open)
    print('enc= ',int_to_hex(enc))


    # site decryption
    encrypted = encrypt(hex_to_int(encode_to_hex(msg)),server_open)
    print('Encrypted = ',int_to_hex(encrypted))


    # site sign
    site_sg = '6CA04253EBCD2B2C45C82D7B39FB7D1229E8C72105BA636723D9619351F12900'
    print(verify(hex_to_int(encode_to_hex(msg)),hex_to_int(site_sg),server_open))


    # my sign
    my_sg = sign(hex_to_int(encode_to_hex(msg)),my_private)
    print("My sign = ",int_to_hex(my_sg))



if __name__ == '__main__':
    my_test()
    sever_test()
