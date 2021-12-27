import random

n0 = pow(2, 255) + 1
n1 = pow(2, 256) - 1


def ascii_to_int_value(text):
    return int(text.encode('utf-8').hex(), 16)


def int_value_to_ascii(text):
    return bytes.fromhex(hex(text)[2:]).decode('ASCII')


def gcd_extended(a, b) -> int:
    if b == 0:
        return a
    else:
        return gcd_extended(b, a % b)


def horner_scheme(number, power, mod) -> int:
    y = 1
    bin_power = format(power, "b")
    for iter in range(0, len(bin_power)):
        if bin_power[iter] == '1':
            y = ((y ** 2) * number) % mod
        elif bin_power[iter] == '0':
            y = (y ** 2) % mod
    return y


def miller_rabin(n, rounds=100):
    s = ((n - 1) & (1 - n)).bit_length() - 1
    d = n >> s
    for _ in range(rounds):
        base = random.randrange(2, n - 1)
        prime = horner_scheme(base, d, n)
        if prime == 1 or prime == (n - 1):
            continue
        for _ in range(1, s):
            prime = horner_scheme(prime, 2, n)
            if prime == (n - 1):
                break
        else:
            return False
    return True


def get_random_simple_number():
    number = random.randrange(n0, n1)
    while not miller_rabin(number):
        number = random.randrange(n0, n1)
    return number


def generate_keys():
    p: int = get_random_simple_number()
    q: int = get_random_simple_number()
    while p == q:
        q = get_random_simple_number()

    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)

    while gcd_extended(e, phi) != 1:
        e = random.randrange(2, phi)
    d = pow(e, -1, phi)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def encrypt_message(text, public_key):
    return horner_scheme(text, public_key[0], public_key[1])


def decrypt_message(text, private_key):
    return horner_scheme(text, private_key[0], private_key[1])


def message_signature(unsigned_text, d, n):
    return horner_scheme(unsigned_text, d, n)


def verify_message(encrypted_text, signed_text, e, n):
    return True if encrypted_text == horner_scheme(signed_text, e, n) else False


class Person:
    def __init__(self):
        self.public_key, self.private_key = generate_keys()

    def keys_pair_for_sender(self, n):
        nn = self.public_key[1]
        while self.public_key[1] > n:
            self.public_key, self.private_key = generate_keys()

    def completing_the_package(self, plain_text, public_key):
        self.keys_pair_for_sender(public_key[1])
        return encrypt_message(ascii_to_int_value(plain_text), public_key), message_signature(
            ascii_to_int_value(plain_text), self.private_key[0], self.public_key[1])

    def decrypt_received_message(self, package, public_key):
        decrypted_message_in_int_value = decrypt_message(package[0], self.private_key)
        if verify_message(decrypted_message_in_int_value, package[1], public_key[0], public_key[1]):
            return 'Verification passed\nReceived message: ' + (int_value_to_ascii(decrypted_message_in_int_value))
        else:
            return 'An error occured during verifying: incorrect values'


A = Person()
B = Person()

text = "ny kak bu da "

package = A.completing_the_package(text, B.public_key)
print(f"Encrypted message: {hex(package[0])}\nSignature of the message: {hex(package[1])}\n")
print(B.decrypt_received_message(package, A.public_key))

# def tuda_cyda():
#     message = 'tuda cyda'
#     H = Person()
#     package = H.completing_the_package(message, H.public_key)
#     print(f'modulus: {hex(H.public_key[1])[2:]}')
#     print(f'public exponent: {hex(H.public_key[0])[2:]}')
#     print(f'ciphertext: {hex(package[0])[2:]}')
#     print(f'signature: {hex(package[1])[2:]}')
#
#
# tuda_cyda()
