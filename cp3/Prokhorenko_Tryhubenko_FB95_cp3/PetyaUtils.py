from itertools import permutations

from cp3.Prokhorenko_Tryhubenko_FB95_cp3.Sys import Sys


class PetyaUtils:
    @staticmethod
    def generate_permutations(most_frequent_ru_bigrams, most_frequent_text_bigrams) -> list:
        all_generated_permutations: list = []
        temp_for_permutations = permutations(most_frequent_ru_bigrams)
        for permutation in temp_for_permutations:
            temp_for_permutations_dictionary = {}
            for i in range(len(most_frequent_text_bigrams)):
                temp_for_permutations_dictionary[most_frequent_text_bigrams[i]] = permutation[i]
            all_generated_permutations.append(temp_for_permutations_dictionary)
        return all_generated_permutations

    @staticmethod
    def calculate_gcd(first_number, second_number) -> int:
        return first_number if second_number == 0 else PetyaUtils.calculate_gcd(second_number,
                                                                                first_number % second_number)

    @staticmethod
    def convert_bigram_to_int_value(bigram) -> int:
        return int(Sys.get_alphabet().index(bigram[0]) * len(Sys.get_alphabet()) + Sys.get_alphabet().index(bigram[1]))

    @staticmethod
    def convert_int_value_to_bigram(int_value) -> str:
        return str(Sys.get_alphabet()[int_value // len(Sys.get_alphabet())]) + str(
            Sys.get_alphabet()[int_value % len(Sys.get_alphabet())])

    @staticmethod
    def calculate_difference(first_number, second_number) -> int:
        return (first_number - second_number) % (len(Sys.get_alphabet()) ** 2)

    @staticmethod
    def calculate_linear_a(difference_X, difference_Y, module) -> int:
        try:
            return int((difference_Y * pow(int(difference_X), -1, len(Sys.get_alphabet()) ** 2)) % module)
        except Exception as ex:
            print(ex)

    @staticmethod
    def calculate_linear_b(a, plain_bigram_int_value, cipher_bigram_int_value) -> int:
        return (cipher_bigram_int_value - a * plain_bigram_int_value) % (len(Sys.get_alphabet()) ** 2)

    @staticmethod
    def decrypt_cipher_test(text, key_tuple) -> str or None:
        a, b = key_tuple
        bigrams = Sys.get_all_bigrams_from_text(text)
        plain_text: str = ""
        try:
            for bigram in bigrams:
                plain_bigram: str = str(PetyaUtils.convert_int_value_to_bigram(
                    (int(PetyaUtils.convert_bigram_to_int_value(bigram)) - int(b)) * int(
                        pow(int(a), -1, int(len(Sys.get_alphabet()) ** 2))) % (len(Sys.get_alphabet()) ** 2)))
                if plain_bigram in Sys.get_unavailable_bigrams():
                    raise "unavailable bigram"
                plain_text += plain_bigram
            return plain_text
        except Exception as ex:
            Sys.log("Decrypt error: " + str(ex))
