import random

MIN = pow(2, 255)+1
MAX = pow(2, 256)-1

def egcd(a, b): # пошук найбільшого спільного кратного
    if(b == 0):
        return a
    else:
        return egcd(b, a % b)

def gorner(x, e, mod): # швидке піднесення до степення
    y = 1
    e = bin(e)[2:]
    for i in e:
        y = y**2
        if i == '1': y *= x 
        y %= mod
        #print(f"i={i}, y={y}")
    return y


def miller_rabin(n, t = 115):
    s = 0 # степінь двійки
    d = n-1

    while not d & 1: # поки d - дільник 2
        d >>= 1 # те саме що і ділення на 2
        s += 1

    # 2**s * d == n-1 
 
    for i in range(t): # перевірка з різними числами
        a = random.randrange(2, n)
        if gorner(a, d, n) == 1: # 2.1 
            continue
        check = False
        for i in range(s):
            if gorner(a, 2**i * d, n) == n-1: # 2.2 # gorner(a, 2**i * d, n) == -1
                check = True
        if check: continue
        else: return False 
    # якщо пройдені всі перевірки то число псевдопросте
    return True  

def get_num(low = MIN, high = MAX):
    p = random.randrange(low, high)
    while not miller_rabin(p):
        p = random.randrange(low, high)
    return p

def get_pair():
    pair = (get_num(), get_num())
    while pair[0] == pair[1]: pair[1] = get_num()
    return pair
    
def get_rsa(pair):
    phi = (pair[0]-1)*(pair[1]-1) # функція Ейлера
    e = random.randrange(2, phi)

    while egcd(e, phi) != 1: e = random.randrange(2, phi)

    private_key = (pow(e, -1, phi), pair[0], pair[1])  # е - обернене по модулю фі # (d, p, q)
    open_key = (pair[0] * pair[1], e) 

    return (open_key, private_key)

class Person():
    def __init__(self):
        self.key_to_get()
    
    def key_to_get(self):
        pair = get_pair()
        self.open_key, self.private_key = get_rsa(pair)
        # open_key = (n, e)
        # private_key = (d, p, q)

    def key_to_send(self, n):
        while self.open_key[0] > n: # генерація нового ключа якщо n > n1
            self.open_key, self.private_key = get_rsa(get_pair())

    def encode(self, text): # перевод симфолів ASCII у хекс
        text = text.encode('utf-8')
        return int(text.hex(), 16)

    def decode(self, text): # перевод цифр у букв
        return bytes.fromhex(hex(text)[2:]).decode('ASCII')

    def encrypt(self, text, e, n): 
        return gorner(text, e, n)

    def decrypt(self, text, d, n): 
        return gorner(text, d, n)

    def sign(self, text, d, n):
        return gorner(text, d, n) 

    def check(self, text, sign, e, n): # перевірка підпису
        return text == gorner(sign, e, n)

    def create_message(self, text, open_key): # n - отримувача
        n, e = open_key
        self.key_to_send(n)
        text = self.encode(text)
        msg = self.encrypt(text, e, n)
        sign = self.sign(text, self.private_key[0], self.open_key[0])
        return (msg, sign)

    def read_message(self, packet, open_key):
        msg, sign = packet
        n, e = open_key
        msg = self.decrypt(msg, self.private_key[0], self.open_key[0])
        
        if self.check(msg, sign, e, n):
            print(f'message: "{self.decode(msg)}"') 

        else: print("Error (")





A = Person()
B = Person()

text = "lol kek cheburek."

packet = A.create_message(text, B.open_key)
print(f"msg={packet[0]}\nsign={packet[1]}\n")
B.read_message(packet, A.open_key)

text = "Ok, Da."

packet = B.create_message(text, A.open_key)
print(f"msg={packet[0]}\nsign={packet[1]}\n")
A.read_message(packet, B.open_key)