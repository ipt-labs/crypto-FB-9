import random

min = 1+2**225
max = -1+2**256

def testmilrab(number):
    t, s = number - 1, 0
    while t % 2 == 0:
        t = t // 2
        s += 1

    for i in range(300):
        a = random.randint(2, number - 2)
        x = pow(a, t, number) 
        if (x == number- 1) or (x == 1):
            continue 
        x = pow(x, 2, number)  
        if x == 1 or x != number - 1:
            return False  
    return True  

def generate_random_number(min = min, max = max):
    number = random.randrange(min, max)
    while not testmilrab(number):
        number = random.randrange(min, max)

    return number

def create_pair():
    pair = (generate_random_number(), generate_random_number())
    while pair[0] == pair[1]:
        pair[1] = generate_random_number()
    
    return pair

def gcdExtended(a, b):
    if a == 0 :
        return b, 0, 1
    gcd, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b//a) * x1
    y = x1
    return gcd, x, y

def inverse(a, m):
    d, x, y = gcdExtended(a, m)
    if d != 1:
        return 0
    else:
        return x % m


def generate_rsa(pair):
    n = pair[0] * pair[1] 
    phi = (pair[0] - 1) * (pair[1] - 1)
    flag = False
    while flag == False:
        e = random.randint(2, phi)
        g, x, y = gcdExtended(e, phi)
        if g == 1:
            flag = True
    d = inverse(e, phi)
    open_key = (e, n)
    private_key = (d, pair[0], pair[1])
    return open_key, private_key

class Abonent():
    def __init__(self):
        pair = create_pair()
        self.open_key, self.private_key = generate_rsa(pair)

    def encrypt(self, text, open_key):
        return pow(text, open_key[0], open_key[1])

    def decrypt(self, text, private_key):
        return pow(text, private_key[0], private_key[1] * private_key[2])

    def sign(self, text, private_key):
        return pow(text, private_key[0], private_key[1] * private_key[2])

    def verify(self, sign, text, open_key):
        return text == pow(sign, open_key[0], open_key[1])

    def encrypt_message(self, text, open_key):
        enc_text = self.encrypt(text, open_key)
        sign = self.sign(text, self.private_key)
        return enc_text, sign

    def decrypt_verify_message(self, packet, open_key):
        text, sign = packet
        text = self.decrypt(text, self.private_key)

        if self.verify(sign, text, open_key):
            print(text)

a = Abonent()
b = Abonent()

text = 312
packet = a.encrypt_message(text, b.open_key)
b.decrypt_verify_message(packet, a.open_key)

f = open('log.txt', 'a', encoding='utf-8')
f.write('A open key: ' + str(a.open_key[0]) + str(a.open_key[1]) + '\n\n')
f.write('A priavte key: ' + str(a.private_key[0]) + str(a.private_key[1]) + str(a.private_key[2]) + '\n\n')
f.write('B open key: ' + str(b.open_key[0]) + str(b.open_key[1]) + '\n\n')
f.write('B priavte key: ' + str(b.private_key[0]) + str(b.private_key[1]) + str(b.private_key[2]) + '\n\n')
f.write('Sign :' + str(packet[1]))
f.close()