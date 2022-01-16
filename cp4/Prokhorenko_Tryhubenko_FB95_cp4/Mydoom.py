from cp4.Prokhorenko_Tryhubenko_FB95_cp4.User import User


class Mydoom:
    @staticmethod
    def RSA():
        FirstUser = User()
        SecondUser = User()
        package = FirstUser.completing_the_package("Test text 1234", SecondUser.public_key)
        print(f"Encrypted message: {hex(package[0])}\nSignature of the message: {hex(package[1])}\n")
        print(SecondUser.decrypt_received_message(package, FirstUser.public_key))


if __name__ == "__main__":
    Mydoom.RSA()

