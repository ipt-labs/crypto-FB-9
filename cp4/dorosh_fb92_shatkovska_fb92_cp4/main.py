# # This is the 4th lab on Cryptology done by Dorosh and Shatkovska FB-92
import random
rand = random.SystemRandom()


# from lab3
def gcd(a, b):
    p = [0, 1]
    gcd_val = b
    a, b = max(a, b), min(a, b)
    while b != 0:
        q = a // b
        gcd_val = b
        a, b = b, a % b
        p.append(p[-1] * (-q) + p[-2])
    return gcd_val, p[-2]  # returns gdc and a^-1


def decompose(p):
    # decomposes p to s and d values in p-1 = d* 2^s
    d = p - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    return s, d


# Miller-Rabin primality test
def miller_rabin(p, k):
    # part 0
    s, d = decompose(p)
    counter = 0
    while counter < k:
        # part 1
        x = rand.randint(1, p)
        if gcd(x, p)[0] > 1:
            return False
        elif gcd(x, p)[0] == 1:
            # part 2
            if pow(x, d, p) in [1, -1]:
                return True
            else:
                xr = pow(x, 2 * d, p)  # if r == 1
                for r in range(2, s - 1):
                    xr = pow(xr, d * (2 ** r), p)
                    if xr == -1:
                        return True
                    elif xr == 1:
                        return False
                    else:
                        continue
        counter += 1
    return True


# print(miller_rabin(97, 10))             # prime
# print(miller_rabin(21881, 10))          # prime
# print(miller_rabin(11, 10000))


def generate_prime(bits):
    while True:
        a = (rand.randrange(1 << bits - 1, 1 << bits) << 1) + 1  # making sure its odd
        if miller_rabin(a, 1000):
            return a


def generate_pq_pair(bits):
    pair0 = (generate_prime(bits), generate_prime(bits))
    return pair0


def generate_e(phin):
    while True:
        e = rand.randrange(2, phin)
        if gcd(e, phin)[0] == 1:
            return e


def decode(message):
    message = int(message.encode('utf-8').hex(), 16)
    return message


def encode(message):
    message = bytes.fromhex(hex(message)[2:]).decode('ASCII')
    return message


class User:
    def __init__(self):
        self.p = 0
        self.q = 0
        self.n = 0
        self.e = 0
        self.d = 0
        self.other_e = 0
        self.other_n = 0

    def generate_keys(self):
        bits = 256
        self.p, self.q = generate_pq_pair(bits)
        print("p: ", self.p)
        print("q: ", self.q)
        self.n = self.p * self.q
        print("n: ", self.n)
        phin = (self.p - 1) * (self.q - 1)
        print("phi(n): ", phin)
        self.e = generate_e(phin)
        print("e: ", self.e)
        self.d = (gcd(self.e, phin)[1] + phin) % phin
        print("d: ", self.d)
        return self.n, self.e

    # !!!may be combined with generate_keys() later
    def generate_correct_keys(self):  # for user A to choose correct keys (other.n <= n)
        keys = self.generate_keys()
        while self.other_n > keys[0]:
            print("--regenerating keys--")
            keys = self.generate_keys()
        return keys

    def encrypt(self, message):  # message needs to be decoded from utf-8
        encrypted = pow(message, self.other_e, self.other_n)
        return encrypted

    def decrypt(self, message):
        decrypted = pow(message, self.d, self.n)
        return decrypted  # message needs to be encoded as utf-8

    def sign(self, message):
        signed = pow(message, self.d, self.n)
        return signed

    def verify(self, signed, decrypted_message):
        return self.encrypt(signed) == decrypted_message

    def send_keys(self):
        return self.e, self.n

    def receive_keys(self, ne):
        other_e, other_n = ne
        self.other_e = other_e
        self.other_n = other_n

    def send_message(self, text):
        print('----Sending message----')
        message = decode(text)
        print("Message: ", message)
        encrypted = self.encrypt(message)
        print("Encrypted message: ", encrypted)
        signed = self.sign(message)
        print("Sign: ", signed)

        return encrypted, signed

    def receive_message(self, mess):
        print('----Receiving message----')
        encrypted, signed = mess
        decrypted_message = self.decrypt(encrypted)

        if self.verify(signed, decrypted_message):
            print("Received message: ", encode(decrypted_message))
            return encode(decrypted_message)
        else:
            return -1


# full process of A sending a message to B
# B creates its keys and shares open keys (eb, nb) with A
B = User()
print('----B(receiver)----')
B.generate_keys()

# A receives keys
A = User()
A.receive_keys(B.send_keys())

# A creates its keys (nb < na) and shares its keys (ea, na) with B
# B receives A's keys and message
print('----A(sender)----')
A.generate_correct_keys()
B.receive_keys(A.send_keys())

# A sends signed message and encrypted message to B
# B receives A's message and sign, decrypts encrypted message and verifies sign
M = "Hi there!"
received = B.receive_message(A.send_message(M))
