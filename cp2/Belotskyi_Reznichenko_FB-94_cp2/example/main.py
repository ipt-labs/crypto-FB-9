from additional_functions import *

alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"

most_common_bigramms_RU = ["ст", "но", "то", "на", "ен"]
combinations_that_never_occur = ["аъ", "аы", "аь", "оъ", "оы", "оь", "уъ", "уы", "уь"]

def read_file(filename):
    f = open(filename, "r", encoding="utf-8")
    text = f.read()
    text = text.replace('\n', "")
    f.close()

    return text

def bigram_freq_in_cipher_text(text):
    i = 0
    big_count_dict = {}
    big_freq_dict = {}

    if len(text) % 2 == 1:
        text += "ъ"

    bidram_amount = len(text)/2

    while(i < len(text)-1):
        bigram = text[i] + text[i+1]
        if bigram in big_count_dict.keys():
            big_count_dict[bigram] += 1
        else:
            big_count_dict[bigram] = 1
        i += 2

    for key in big_count_dict.keys():
        big_freq_dict[key] = big_count_dict[key] / bidram_amount

    five_popular_in_cipher_text = sorted(big_freq_dict, key=big_freq_dict.get, reverse=True)[:5]

    return five_popular_in_cipher_text

def make_pairs(popular_list):
    output_pairs_list = []
    for i in popular_list:
        for j in popular_list:
            if i==j:
                continue
            else:
                pair = (i, j)
                if (j, i) in output_pairs_list:
                    continue
                else:
                    output_pairs_list.append(pair)
    return output_pairs_list

def convert_pairs_to_numbers(pair_list):
    pair_list_in_numbers = []
    for i in pair_list:
        str1 = ""
        str2 = ""
        X1 = alphabet.index(str1.join([i[0][0]])) * 31 + alphabet.index(str2.join([i[0][1]]))
        str1 = ""
        str2 = ""
        X2 = alphabet.index(str1.join([i[1][0]])) * 31 + alphabet.index(str2.join([i[1][1]]))
        new_pair = (X1, X2)
        pair_list_in_numbers.append(new_pair)
    return pair_list_in_numbers

def make_keys_list(Ru_popular_numbers, text_popular_numbers):
    keys_list = []
    for key_RU in Ru_popular_numbers:
        for key_text in text_popular_numbers:
            delta_x = int(key_RU[0]) - int(key_RU[1])
            delta_y = int(key_text[0]) - int(key_text[1])
            a = modular_solution(delta_x, delta_y, 31 ** 2)
            if a == 0:
                continue
            else:
                b = (int(key_text[0]) - a * int(key_RU[0]))%31**2
                keys_list.append((a, b))
    return keys_list

def decrypt_cipher_text(keys, text):
    made_plain_text = ""
    cipher_bg=[]
    plain_text_dict = {}
    i = 0
    while i < len(text)-1:
        y = alphabet.index(text[i]) * 31 + alphabet.index(text[i+1])
        cipher_bg.append(y)
        i += 2

    for k in keys:
        made_plain_text = ""
        for Y in cipher_bg:
            a_1 = reverse_element(k[0], 31**2)
            if (a_1 != 0):
                X = a_1 * (Y - k[1]) % 31**2
                x1 = X // 31
                x2 = X % 31
                made_plain_text += alphabet[x1] + alphabet[x2]
                plain_text_dict[k] = made_plain_text

    return plain_text_dict

def analyze_made_texts(text_dict):
    text_dict_filter = {}
    keys_not_fit = []
    for k in text_dict.keys():
        for pair in combinations_that_never_occur:
            temp_text = text_dict[k]
            if pair in temp_text:
                keys_not_fit.append(k)
                break

    for k1 in keys_not_fit:
        del text_dict[k1]

    return list(text_dict.keys())[0]


if __name__ == '__main__':
    my_var_text = read_file("05.txt")
    five_popular_list = bigram_freq_in_cipher_text(my_var_text)
    print(f"5 popular bigrams in text\n{five_popular_list}")
    five_popular_pairs_in_pt = make_pairs(most_common_bigramms_RU)
    print(f"Pairs of the most popular five bigrams\n{five_popular_pairs_in_pt}")
    five_popular_pairs_in_ct = make_pairs(five_popular_list)
    print(f"Pairs of the most popular five bigrams in ciphertext\n{five_popular_pairs_in_ct}")
    five_popular_pairs_in_pt_numbers = convert_pairs_to_numbers(five_popular_pairs_in_pt)
    print(f"Pairs of the most popular five bigrams(numbers)\n{five_popular_pairs_in_pt_numbers}")
    five_popular_pairs_in_ct_numbers = convert_pairs_to_numbers(five_popular_pairs_in_ct)
    print(f"Pairs of the most popular five bigrams in ciphertext (numbers)\n{five_popular_pairs_in_ct_numbers}")
    keys = make_keys_list(five_popular_pairs_in_pt_numbers, five_popular_pairs_in_ct_numbers)
    print(f"All possible keys\n{keys}")
    made_texts = decrypt_cipher_text(keys, my_var_text)
    print(f"Keys that can be true\n{made_texts.keys()}")
    key = analyze_made_texts(made_texts)
    print(f"Key was found\n{key}")
    print(f"Decrypt text is\n{made_texts[key]}")