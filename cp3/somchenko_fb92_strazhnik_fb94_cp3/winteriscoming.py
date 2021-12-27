import re
from collections import Counter
from itertools import permutations, combinations

most_common_bigrams_in_russian_lang = ['ст', 'но', 'то', 'на', 'ен']
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
cyphered_text = re.sub(r'[^а-яА-Я]', '', open('ciphertext_v4.txt').read()).lower()

impossible_bigrams_in_ru_language = ['аы', 'аь', 'еэ', 'жф', 'жч', 'жш', 'жщ', 'зп', 'зщ', 'йь', 'оы', 'уы', 'уь', 'фц',
                                     'хщ', 'цщ', 'цэ', 'чщ', 'чэ', 'шщ', 'ьы']


def gcd_extended(a, b):
    if b == 0:
        return a
    else:
        return gcd_extended(b, a % b)


def get_most_common_bi_in_text(text):
    bigrams = Counter(text[bi: bi + 2] for bi in range(0, len(text) - 1, 2))
    bigrams = list(dict(sorted(bigrams.items(), key=lambda x: x[1], reverse=True)).keys())[:5]
    return bigrams


def get_all_bigrams_from_text(text):
    return [text[idx:idx + 2] for idx in range(0, len(text) - 1, 2)]


def get_bi_in_int_value(bigram) -> int:
    return alphabet.index(bigram[0]) * len(alphabet) + alphabet.index(bigram[1])


def get_bi_from_int_value(bigram_int_value) -> str:
    return (alphabet[bigram_int_value // len(alphabet)]) + (alphabet[bigram_int_value % len(alphabet)])


def differences(first_number, second_number) -> int:
    return first_number - second_number


def permutation(most_comm_ru_bigrams_value, most_comm_text_bigrams_value):
    permuteted_values = permutations(most_comm_ru_bigrams_value)
    ready_made_permutations = []
    for p in permuteted_values:
        combinations = {}
        for i in range(len(most_comm_text_bigrams_value)):
            combinations[most_comm_text_bigrams_value[i]] = p[i]
        ready_made_permutations.append(combinations)
    return ready_made_permutations


def a_calculation(diff_X, diff_Y, mod=len(alphabet) ** 2) -> int:
    try:
        return int((diff_Y * int(pow(int(diff_X), -1, int(len(alphabet) ** 2)))) % mod)
    except Exception as ex:
        pass


def b_calculation(a, value_of_plain_bi, value_of_cipher_bi):
    try:
        return (value_of_cipher_bi - a * value_of_plain_bi) % (len(alphabet) ** 2)
    except Exception as ex:
        pass


def affine_cipher_crack(text):
    most_comm_bigrams_in_text = get_most_common_bi_in_text(text)
    most_comm_bigrams_in_text_value = []
    for bi in most_comm_bigrams_in_text:
        most_comm_bigrams_in_text_value.append(get_bi_in_int_value(bi))
    most_comm_bigrams_in_ru_value = []
    for bi in most_common_bigrams_in_russian_lang:
        most_comm_bigrams_in_ru_value.append(get_bi_in_int_value(bi))

    pairs = permutation(most_comm_bigrams_in_ru_value, most_comm_bigrams_in_text_value)

    all_pairs = []
    for i in range(len(pairs)):
        for x, y in pairs[i].items():
            all_pairs.append((x, y))
    all_pairs = list(set(all_pairs))
    all_pairs = list(combinations(all_pairs, 2))

    keys = []
    for pair in all_pairs:
        y1, y2 = pair[0][0], pair[1][0]
        x1, x2 = pair[0][1], pair[1][1]

        diff_Y = int(differences(y1, y2))
        diff_X = int(differences(x1, x2))

        gcd = gcd_extended(diff_X, (len(alphabet) ** 2))
        if diff_X != 0 or diff_Y != 0:
            if gcd == 1:
                a = a_calculation(diff_X, diff_Y, len(alphabet) ** 2)
                b = b_calculation(a, x1, y1)
                keys.append((a, b))
            elif gcd > 1 and diff_Y % gcd == 0:

                diff_Y /= gcd
                diff_X /= gcd

                mod = len(alphabet) ** 2 / gcd
                a = a_calculation(diff_X, diff_Y, mod)
                if not a: continue
                while a < len(alphabet) ** 2:
                    b = b_calculation(a, x1, y1)
                    keys.append((a, b))
                    a += gcd
    return list(set(keys))


def decrypt_cipher_text(text, key_tuple) -> str or None:
    a, b = key_tuple
    bigrams = get_all_bigrams_from_text(text)
    decrypted_text: str = ""
    try:
        for bigram in bigrams:
            decrypted_bigram = get_bi_from_int_value(
                (int(get_bi_in_int_value(bigram)) - int(b)) * int(pow(int(a), -1, int(len(alphabet) ** 2))) % (
                        len(alphabet) ** 2))
            decrypted_text += decrypted_bigram
        number_of_bad_bi = Counter(decrypted_text[bi: bi + 2] for bi in range(0, len(decrypted_text) - 1, 2))
        for bigr in number_of_bad_bi.keys():
            if bigr in impossible_bigrams_in_ru_language:
                if number_of_bad_bi.get(bigr) >= 3:
                    return
                else:
                    continue
        return decrypted_text
    except Exception as ex:
        pass


def find_right_key(keys):
    for key in keys:
        temp = decrypt_cipher_text(cyphered_text, key)
        if temp:
            print(temp)
            print(key)


cyphered_text = "".join([i for i in cyphered_text if i in alphabet])
keys = affine_cipher_crack(cyphered_text)
find_right_key(keys)
