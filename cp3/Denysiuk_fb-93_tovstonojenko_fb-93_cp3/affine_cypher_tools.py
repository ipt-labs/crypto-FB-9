import sys

sys.path.insert(0, '../../cp1/Denysiuk_fb-93_tovstonojenko_fb-93_cp1')
import my_lib
from collections import Counter

LETTERS = sorted(list('абвгдежзийклмнопрстуфхцчшщыьэюя'))

MOST_FREQUENT_BIGRAM = ['ст', 'но', 'ен', 'то', 'на']#, 'ов', 'ни']#, 'ра', 'во', 'ко']


def bigrams_to_values(bigrams: list[str]) -> list[int]:
    values = []
    n_letters = len(LETTERS)
    for i in bigrams:
        values.append(LETTERS.index(i[0]) * n_letters + LETTERS.index(i[1]))
    return values


def values_to_bigrams(values: list[int]) -> list[str]:
    bigrams = []
    n_letters = len(LETTERS)
    for i in values:
        bigrams.append(LETTERS[i // n_letters] + LETTERS[i % n_letters])
    return bigrams


def encrypt_bigram(bigrams: list[str], key: tuple) -> list:
    n_letters = len(LETTERS)
    encoded_bigrams = []
    values = bigrams_to_values(bigrams)
    for v in values:
        encoded_bigrams.append((key[0] * v + key[1]) % n_letters ** 2)
    return values_to_bigrams(encoded_bigrams)


def decrypt_bigram(encoded_bigrams: list[str], key: tuple) -> str:
    n_letters = len(LETTERS)
    decrypted_bigram = []
    encoded_bigrams = bigrams_to_values(encoded_bigrams)
    for bigram in encoded_bigrams:
        a = ((n_letters ** 2 + bigram - key[1]) * (reverse_element(key[0], n_letters ** 2))) % (
                n_letters ** 2)
        decrypted_bigram.append(LETTERS[a // n_letters] + LETTERS[a % n_letters])
    return decrypted_bigram


def decrypt_text(text: str, key: tuple) -> str:
    list_of_bigrams = my_lib.make_list_of_bigram(text, 2)
    decrypted_list = decrypt_bigram(list_of_bigrams, key)
    return ''.join(decrypted_list)


def encrypt_text(text: str, key: tuple) -> str:
    list_of_bigrams = my_lib.make_list_of_bigram(text, 2)
    encrypted_list = encrypt_bigram(list_of_bigrams, key)
    return ''.join(encrypted_list)


def reverse_element(a: int, b: int):
    return euclid_ext(a, b)[1]


def euclid_ext(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = euclid_ext(b, a % b)
        return d, y, x - y * (a // b)


def get_key_by_two_bigrams(original: tuple, encrypted: tuple) -> list[tuple[int]]:
    n_letters_sq = len(LETTERS) ** 2
    original = tuple(bigrams_to_values(original))
    encrypted = tuple(bigrams_to_values(encrypted))
    q = (original[1] - original[0]) % n_letters_sq
    t = (encrypted[1] - encrypted[0]) % n_letters_sq
    a = first_part_of_key(q, t)
    b1 = second_part_of_key(original[0], encrypted[1], a)
    b2 = second_part_of_key(original[1], encrypted[1], a)
    return [(a, b1)] if b1 == b2 else [(a, b1), (a, b2)]


def first_part_of_key(x: int, y: int) -> int:
    n_letters_sq = len(LETTERS) ** 2
    return (y * (reverse_element(x, n_letters_sq) % n_letters_sq)) % n_letters_sq


def second_part_of_key(x: int, y: int, a) -> int:
    n_letters_sq = len(LETTERS) ** 2
    return (y - x * a) % n_letters_sq


def combine(original_list: list) -> list[tuple]:
    combined_list = []
    for i in original_list[:-1]:
        for j in original_list[original_list.index(i) + 1:]:
            if i[0]!=j[0] and i[0]!=j[0]:
                combined_list.append(((i[0], j[0]),(i[1],j[1])))
    return combined_list


def combine1(list1:list, list2:list) -> list[tuple]:
    combined_list = []
    for i in list1:
        for j in list2:
            combined_list.append((i,j))
    return combined_list


def attack_on_cypher(text: str) -> list[tuple[int]]:
    bigrams_stats = my_lib.make_dict_of_stats_of_bigram(text, 2).items()
    sorted_by_frequency_bigrams = [i[0] for i in sorted(bigrams_stats, key=lambda a: a[1],
                                                    reverse=True)][:len(MOST_FREQUENT_BIGRAM)]
    print(f'Most frequent bigrams:\n{sorted_by_frequency_bigrams}')
    pairs_orgn_encr = combine1(MOST_FREQUENT_BIGRAM,sorted_by_frequency_bigrams)
    supposable_keys = []
    pairs_orgn_encr=combine(pairs_orgn_encr)
    for i in pairs_orgn_encr:
        for j in get_key_by_two_bigrams(*i):
            supposable_keys.append(j)
    return list(set(supposable_keys))

def validation(text):
    allowed_2g=['ст', 'но', 'ен', 'то', 'на', 'ов', 'ни', 'ра', 'по', 'ко']
    allowed_3g=['сто', 'ено', 'нов', 'тов', 'ово', 'ова']
    bigrams_stats = my_lib.make_dict_of_stats_of_bigram(text, 2).items()
    sorted_by_frequency_bigrams = [i[0] for i in sorted(bigrams_stats, key=lambda a: a[1],
                                                        reverse=True)][:len(allowed_2g)*2]
    threegrams_stats = Counter([text[i]+text[i+1]+text[i+2] for i in range(0,len(text)-len(text)%3,3)])
    sorted_by_frequency_threegrams = [i[0] for i in sorted(threegrams_stats, key=lambda a: a[1],
                                                        reverse=True)][:len(allowed_3g)*2]
    count_of_valid_ngrams=0
    for i in allowed_2g:
        if i  in sorted_by_frequency_bigrams:
            count_of_valid_ngrams+=1
    for i in allowed_3g:
        if i  in sorted_by_frequency_threegrams:
            count_of_valid_ngrams+=1
    forbiden = ['аь', 'аъ', 'бй', 'бф', 'гщ', 'гъ', 'еъ', 'жй', 'жц', 'жщ', 'жъ', 'жы', 'йъ', 'къ', 'лъ', 'мъ',
    'оъ', 'пъ', 'ръ', 'уъ', 'уь', 'фщ', 'фъ', 'хы', 'цщ', 'цъ', 'цю', 'чф', 'цщ', 'чъ',
    'чю', 'шщ', 'шъ', 'шы', 'шю', 'щж', 'щл', 'щх', 'щц', 'щш', 'щъ', 'щы', 'щю', 'щя', 'ъа',
    'ъб', 'ъг', 'ъд', 'ъз', 'ъй', 'ък', 'ъл', 'ън', 'ъо', 'ъп', 'ър', 'ъс', 'ът', 'ъу', 'ъф', 'ъх', 'ъц',
    'ъч', 'ъш', 'ъщ', 'ъъ', 'ъы', 'ъы', 'ъь', 'ъэ', 'ыъ',  'ьъ', 'ьы', 'эа', 'эж',   'эу',
    'эщ', 'эъ',  'эь', 'эю',  'юъ', 'юы', 'юь', 'яъ', 'яь', 'ьь']
    count=0
    for i in forbiden:
        if i in text:
            count+=1
    return count<len(forbiden)*0.30 and len(allowed_2g+allowed_3g)*0.40<count_of_valid_ngrams

