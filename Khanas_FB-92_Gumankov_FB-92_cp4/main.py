import random
from math import gcd


min_border = 1 << 255
max_border = min_border*2 -2


print("Chosen max: "+ str(max_border))
print("Chosen min: "+ str(min_border))

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def reverse_by_module(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# d = reverse_by_module(5, 792)
# print("Reverse : "+ str(d))


def gorner_quick_pow(X, alpha, module):
    alpha_binary_representation = bin(alpha)
    alpha_binary_representation_striped = alpha_binary_representation[2:len(alpha_binary_representation)]
    Y = 1
    for i in alpha_binary_representation_striped:
        Y = (pow(Y, 2)) % module
        if int(i) == 1:
            Y = (X * Y) % module
    return Y



def miller_rabin(n):
    k = 60 # The optimal number of rounds for this test is 40-60
    for i in range(k):
        a = random.randrange(1, n - 1)
        expo = n - 1
        s = 0
        while not expo & 1:
            expo >>= 1
            s += 1
        #if pow(a, expo, n) == 1:
        if gorner_quick_pow(a, expo, n) == 1:
            return True

        while expo < n - 1:
            if gorner_quick_pow(a, expo, n) == n - 1:
                return True

            expo <<= 1  # instead of multiplying by 2 
        return False
    return True


def is_prime(n):
    # Return True if num is a prime number. This function does a quicker
    # prime number check before calling miller_rabin().

    if (n < 2):
        return False # 0, 1, and negative numbers are not prime

    # About 1/3 of the time we can quickly determine if num is not prime
    # by dividing by the first few dozen prime numbers. This is quicker
    # than miller_rabin(), but unlike miller_rabin() is not guaranteed to
    # prove that a number is prime.
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if n in lowPrimes:
        return True

    # See if any of the low prime numbers can divide num
    for prime in lowPrimes:
        if (n % prime == 0):
            return False

    # If all else fails, call miller_rabin() to determine if num is a prime.
    return miller_rabin(n)


def gen_prime():
    while True:
        a = (random.randrange(min_border, max_border) << 1) + 1 #For better secutity against crypto attacksv  p = 2*p' + 1 
        if is_prime(a):
            return a




def gen_key_pairs(p, q):
    n = p * q
    oiler = (p - 1) * (q - 1)
    e = random.randint(2, oiler - 1)
    while not gcd(e, oiler) == 1:
        e = random.randint(2, oiler - 1)
    d = reverse_by_module(e, oiler)
    return [e, n, d, p, q]


class Receiver:
    def __init__(self,p, q, name):
        self.username = name
        self._keys = gen_key_pairs(p, q)
        self.e, self.n, self._d , self._p, self._q = self._keys[0],self._keys[1],self._keys[2],self._keys[3],self._keys[4],
        self._my_message = random.randint(0, self.n  - 1)
        self.signature = gorner_quick_pow(self._my_message, self._d, self.n)
        self.sender_e = None
        self.sender_n = None
        self.encrypted_message = None
        self._received_message = []
        self._decrypted_received_message = None
        #self._sender = slef.Sender(self.e, self.n, self._my_message)

    def send_keys(self):
        print("[*]" + self.username + " Sent public public keys")
        return [self.e, self.n]

    def receive_keys(self, e, n):
        self.sender_e = e
        self.sender_n = n

    def get_my_message():
        return self._my_message

    def get_decrypted_message():
        return self._decrypted_received_message

    #For testing purpose only
    def print_all_info(self):
        self.encrypt()
        print("_____________________________________")
        print("[*]" + self.username + "Information:")
        print("e: "+ str(self.e))
        print("n: "+ str(self.n))
        print("_d: "+ str(self._d))
        print("_p: "+ str(self._p))
        print("_q: "+ str(self._q))
        print("_my_message: "+ str(self._my_message))
        print("signature: "+ str(self.signature))
        print("encrypted message: "+ str(self.encrypted_message))
        print("_____________________________________")
        return





    def encrypt(self):
        if self.sender_e is not None and self.sender_n is not None:
            self.encrypted_message = gorner_quick_pow(self._my_message, self.sender_e, self.sender_n)

    def send_message(self):
        self.encrypted_message = gorner_quick_pow(self._my_message, self.sender_e, self.sender_n)
        return [self.encrypted_message, self.signature]

    def receive_message(self, message: list):
        self._received_message = message
        self._decrypted_received_message = gorner_quick_pow(self._received_message[0], self._d, self.n)
        print("[*]" + self.username + " Verifying message : ")
        print("Decrypted message: "+ str(self._decrypted_received_message))
        print("Decrypted signature: "+ str(gorner_quick_pow(self._received_message[1], self.sender_e, self.sender_n)))
        return self._decrypted_received_message == gorner_quick_pow(self._received_message[1], self.sender_e, self.sender_n)

    def get_decrypted_message(self):
        return self._decrypted_received_message

    # class Sender:
    #     def __init__(self, e, n, message):
    #         self.e = e
    #         self.n = n
    #         self.my_message = message
    
     



if __name__ == "__main__":
    while True:
        p, q, p1, q1 = gen_prime(),gen_prime(),gen_prime(),gen_prime()
        while True:
            p, q, p1, q1 = gen_prime(),gen_prime(),gen_prime(),gen_prime()
            if p * q <= p1 * q1:
                break

        Alice = Receiver(p, q, 'Alice')
        Bob = Receiver(p1, q1, 'Bob')

        Alice.receive_keys(Bob.send_keys()[0],Bob.send_keys()[1])
        Bob.receive_keys(Alice.send_keys()[0],Alice.send_keys()[1])

        Alice.print_all_info()
        Bob.print_all_info()

        print("1) Alice send message to Bob, and Bob verifies it")
        print("2) Bob send message to Alice, and Alice verifies it")
        print("3) Try yo intercept message using Dude as interface")
        input1 = input()

        if input1 == '1':
            if Bob.receive_message(Alice.send_message()):
                print("Bob receive: "+ str(Bob.get_decrypted_message()))
            else:
                print("Smth went wrong, Bob failed to succesfully receive and verify message")
        elif input1 == '2':
            if Alice.receive_message(Bob.send_message()):
                print("Alice receive: "+ str(Alice.get_decrypted_message()))
            else:
                print("Smth went wrong, Alice failed to succesfully receive and verify message")
        elif input1 == '3':
            p2, q2 = gen_prime(),gen_prime()
            Dude = Receiver(p2, q2, 'Dude')
            try:
                if Dude.receive_message(Alice.send_message()):
                    print("Alice receive: "+ str(Dude.get_decrypted_message()))
                else:
                    print("Smth went wrong, DUDE failed to succesfully receive and verify message")
            except TypeError:
                print("!!!!!!Detected Dude with malicious intent!!!!!!")
        else:
            break


