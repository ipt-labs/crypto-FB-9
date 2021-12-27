from itertools import cycle, combinations

from cp3.Prokhorenko_Tryhubenko_FB95_cp3.PetyaUtils import PetyaUtils
from cp3.Prokhorenko_Tryhubenko_FB95_cp3.Sys import Sys


class Petya:
    @staticmethod
    def crack(path_to_file):

        possible_keys: list = []
        most_frequent_ru_bigrams = Sys.get_most_frequent_ru_bigrams()
        most_frequent_text_bigrams = Sys.get_most_frequent_text_bigrams(Sys.get_text(path_to_file))

        all_generated_permutations = PetyaUtils.generate_permutations(most_frequent_ru_bigrams,
                                                                      most_frequent_text_bigrams)
        temp_for_permutations: list = []
        for permutation in all_generated_permutations:
            for lower_permutation in list(permutation.items()):
                temp_for_permutations.append(lower_permutation)
        clear_permutations = list(set(temp_for_permutations))
        all_generated_combinations = combinations(clear_permutations, 2)
        if True:
            for combination in all_generated_combinations:
                most_frequent_text_bigram_int_value_1, most_frequent_text_bigram_int_value_2 = PetyaUtils.convert_bigram_to_int_value(
                    combination[0][0]), PetyaUtils.convert_bigram_to_int_value(combination[1][0])
                most_frequent_ru_bigram_int_value_1, most_frequent_ru_bigram_int_value_2 = PetyaUtils.convert_bigram_to_int_value(
                    combination[0][1]), PetyaUtils.convert_bigram_to_int_value(combination[1][1])

                difference_X = PetyaUtils.calculate_difference(most_frequent_ru_bigram_int_value_1,
                                                               most_frequent_ru_bigram_int_value_2)
                difference_Y = PetyaUtils.calculate_difference(most_frequent_text_bigram_int_value_1,
                                                               most_frequent_text_bigram_int_value_2)

                gcd = PetyaUtils.calculate_gcd(difference_X, len(Sys.get_alphabet()) ** 2)

                if gcd == 1:
                    a = PetyaUtils.calculate_linear_a(difference_X, difference_Y, len(Sys.get_alphabet()) ** 2)
                    b = PetyaUtils.calculate_linear_b(a, most_frequent_ru_bigram_int_value_1,
                                                      most_frequent_text_bigram_int_value_1)
                    possible_keys.append((a, b))
                elif difference_Y % gcd == 0 and gcd > 1:
                    difference_X /= gcd
                    difference_Y /= gcd
                    module = len(Sys.get_alphabet()) ** 2 / gcd
                    a = PetyaUtils.calculate_linear_a(difference_X, difference_Y, module)
                    while a < len(Sys.get_alphabet()) ** 2:
                        b = PetyaUtils.calculate_linear_b(a, most_frequent_ru_bigram_int_value_1,
                                                          most_frequent_text_bigram_int_value_1)
                        possible_keys.append((a, b))
                        a += gcd
        possible_keys = list(set(possible_keys))
        for key in possible_keys:
            plain_text = PetyaUtils.decrypt_cipher_test(Sys.get_text(path_to_file), key)
            if plain_text:
                print(key)
                print(plain_text)


if __name__ == "__main__":
    Petya.crack("../../tasks/cp3/variants.utf8/06.txt")
