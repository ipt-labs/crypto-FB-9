import random


class Sys:

    @staticmethod
    def ascii_to_int_value(ascii_text) -> int:
        return int(ascii_text.encode('utf-8').hex(), 16)

    @staticmethod
    def int_value_to_ascii(int_value) -> str:
        return bytes.fromhex(hex(int_value)[2:]).decode('ascii')

    @staticmethod
    def calculate_gcd(first_number, second_number) -> int:
        return first_number if second_number == 0 else Sys.calculate_gcd(second_number,
                                                                         first_number % second_number)

    @staticmethod
    def horner(number, power, module) -> int:
        y = 1
        binary_power = format(power, "b")
        for iterator in range(0, len(binary_power)):
            if binary_power[iterator] == '1':
                y = ((y ** 2) * number) % module
            elif binary_power[iterator] == '0':
                y = (y ** 2) % module
        return y

    @staticmethod
    def miller_rabin(number, rounds=100) -> bool:
        s = ((number - 1) & (1 - number)).bit_length() - 1
        d = number >> s
        for _ in range(rounds):
            base = random.randrange(2, number - 1)
            prime = Sys.horner(base, d, number)
            if prime == 1 or prime == (number - 1):
                continue
            for _ in range(1, s):
                prime = Sys.horner(prime, 2, number)
                if prime == (number - 1):
                    break
            else:
                return False
        return True

    @staticmethod
    def get_random_simple_number() -> int:
        number = random.randrange(pow(2, 255) + 1, pow(2, 256) - 1)
        while not Sys.miller_rabin(number):
            number = random.randrange(pow(2, 255) + 1, pow(2, 256) - 1)
        return number

    @staticmethod
    def generate_keys() -> tuple:
        p: int = Sys.get_random_simple_number()
        q: int = Sys.get_random_simple_number()
        while p == q:
            q = Sys.get_random_simple_number()

        n = p * q
        phi = (p - 1) * (q - 1)
        e = random.randrange(2, phi)

        while Sys.calculate_gcd(e, phi) != 1:
            e = random.randrange(2, phi)
        d = pow(e, -1, phi)
        public_key = (e, n)
        private_key = (d, n)
        return public_key, private_key

    @staticmethod
    def encrypt_message(plain_text, public_key) -> int:
        return Sys.horner(plain_text, public_key[0], public_key[1])

    @staticmethod
    def decrypt_message(cipher_text, private_key) -> int:
        return Sys.horner(cipher_text, private_key[0], private_key[1])

    @staticmethod
    def message_signature(unsigned_text, d, n) -> int:
        return Sys.horner(unsigned_text, d, n)

    @staticmethod
    def verify_message(encrypted_text, signed_text, e, n) -> bool:
        return True if encrypted_text == Sys.horner(signed_text, e, n) else False


