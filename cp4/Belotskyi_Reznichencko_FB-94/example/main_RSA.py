from additional_functions import *

prostoe_list = [2, 3, 5, 7]

class algorithm_RSA():
    def __init__(self, name, key_size):
        self.name = name
        self.key_size = key_size
        self.key = []
        self.n = None
        self.e = None
        self.d = None

    def generate_primitive_numbers_pair(self, key_b = None):
        f = open('logfile.log', 'a')
        if (key_b == None):
            f.write("Numbers that did not fit the first pair simplicity test:\n")
        else:
            f.write("Numbers that did not fit the second pair simplicity test:\n")

        j = 1
        for i in range (0, 2):
            while True:
                if (key_b == None):
                    min_candidat = int('1' + '0' * self.key_size)
                    max_candidat = int('1' + '0' * (self.key_size + 1))
                    candidat = random.randint(min_candidat, max_candidat)
                else:
                    candidat = 2 * j * key_b[i] + 1

                for p in prostoe_list:
                    if (candidat % p == 0):
                        candidat = candidat + p - 1

                result = miller_rabbin_test(candidat)

                if (result == True):
                    self.key.append(candidat)
                    break
                else:
                    f.write(f"{str(candidat)}\n")

                j += 1

    def make_crypto_RSA(self):
        self.n = self.key[0] * self.key[1]

        fi_n = (self.key[0] - 1) * (self.key[1] - 1)

        while True:
            e = random.randint(2, fi_n)
            if (math.gcd(e, fi_n) == 1):
                self.e = e
                break

        self.d = pow(self.e, -1, fi_n)

    def show_info(self):
        print(f"User name: {self.name}")
        print(f"Generate primitive numbers: {self.key}")
        print(f"Public key (e, n): ({self.e}, {self.n})")
        print(f"Private key d: {self.d}")

    def Encrypt(self, M, e, n):
        C = pow(M, e, n)
        return C

    def Decrypt(self, C):
        M = pow(C, self.d, self.n)
        return M

    def Sign(self, M):
        S = pow(M, self.d, self.n)
        return S

    def Verify(self, M, S, e, n):
        M_decrypt = pow(S, e, n)
        if M_decrypt == M:
            return True
        else:
            return False

    def SendKey(self, k, e1, n1):
        k1 = pow(k, e1, n1)
        S = self.Sign(k)
        print(f"{self.name} signed k with S: {S}")
        S1 = pow(S, e1, n1)
        return (k1, S1)

    def ReceiveKey(self, k1, S1):
        k = pow(k1, self.d, self.n)
        S = pow(S1, self.d, self.n)
        return (k, S)

    def sign_check(self, k, S, e, n):
        k_check = pow(S, e, n)
        if k == k_check:
            return True
        else:
            return False

Alice = algorithm_RSA("Alice", 64)
Bob = algorithm_RSA("Bob", 64)

Bob.generate_primitive_numbers_pair()
Alice.generate_primitive_numbers_pair(Bob.key)

Alice.make_crypto_RSA()
Bob.make_crypto_RSA()

Alice.show_info()
Bob.show_info()

M = random.randint(0, Bob.n)
print(f"{Alice.name} choose message M: {M}")
C = Alice.Encrypt(M, Bob.e, Bob.n)
print(f"{Alice.name} encrypt message with {Bob.name} public key: {C}")

M_decrypt = Bob.Decrypt(C)
print(f"{Bob.name} decrypt C with his/her private key. M_decrypt: {M_decrypt}")

if M == M_decrypt:
    print("Verification was successful (M = M_decrypt)")

S = Alice.Sign(M)
print(f"{Alice.name} signed message M (M,S): ({M}, {S})")

verify_state = Bob.Verify(M, S, Alice.e, Alice.n)
print(f"Sign verification state: {verify_state}")

k = random.randint(1, Bob.n)
print(f"{Bob.name} choose message k: {k}")
k1_S1 = Bob.SendKey(k, Alice.e, Alice.n)
print(f"{Bob.name} send message (k1, S1): ({k1_S1[0]}, {k1_S1[1]})")
k_res_S_res = Alice.ReceiveKey(k1_S1[0], k1_S1[1])
print(f"{Alice.name} receive (k, S): ({k_res_S_res[0]}, {k_res_S_res[1]})")
verify = Alice.sign_check(k_res_S_res[0], k_res_S_res[1], Bob.e, Bob.n)
print(f"Sign verification state: {verify}")