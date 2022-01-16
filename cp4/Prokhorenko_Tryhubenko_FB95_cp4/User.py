from cp4.Prokhorenko_Tryhubenko_FB95_cp4.Sys import Sys


class User:

    def __init__(self):
        self.public_key, self.private_key = Sys.generate_keys()

    def keys_pair_for_sender(self, n):
        nn = self.public_key[1]
        while self.public_key[1] > n:
            self.public_key, self.private_key = Sys.generate_keys()

    def completing_the_package(self, plain_text, public_key):
        self.keys_pair_for_sender(public_key[1])
        return Sys.encrypt_message(Sys.ascii_to_int_value(plain_text), public_key), Sys.message_signature(
            Sys.ascii_to_int_value(plain_text), self.private_key[0], self.public_key[1])

    def decrypt_received_message(self, package, public_key):
        decrypted_message_in_int_value = Sys.decrypt_message(package[0], self.private_key)
        if Sys.verify_message(decrypted_message_in_int_value, package[1], public_key[0], public_key[1]):
            return 'Ok!\nMsg: ' + (Sys.int_value_to_ascii(decrypted_message_in_int_value))
        else:
            return 'Error!'
