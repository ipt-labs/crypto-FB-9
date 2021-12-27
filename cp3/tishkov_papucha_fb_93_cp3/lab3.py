from itertools import permutations
from cp1.Tishkov_Papucha_FB_93_cp1.Lab1 import calc_all_bigramm_freq

rus_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

rus_most_freq_bigramms = ['ст', 'но', 'то', 'ен', 'на']

control_bigramms_rus = ['аы', 'аь', 'йь', 'оы', 'уы', 'уь', 'ьы', 'ыь']


def insert_line_breaks(text, period):
    new_text = list()
    i = 1
    while i <= len(text):
        new_text.append(text[i - 1])
        if i % period == 0:
            new_text.append('\n')
        i += 1
    return ''.join(new_text)


def gcd_ext(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_ext(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def calc_reverse_by_mod(a, mod):
    gcd, x, y = gcd_ext(a, mod)
    if gcd == 1:
        return (x % mod + mod) % mod
    else:
        return -1


def calc_linear_comparison(a, b, mod):
    gcd, x, y = gcd_ext(a, mod)
    if gcd == 1:
        x = (calc_reverse_by_mod(a, mod) * b) % mod
        return x
    elif b % gcd != 0:
        return -1
    else:
        a1 = int(a / gcd)
        b1 = int(b / gcd)
        n1 = int(mod / gcd)
        x = calc_linear_comparison(a1, b1, n1)
        return x


def get_most_freq_bigramms(bigramm_freq_dict, size):
    most_freq_dict = dict(list(bigramm_freq_dict.items())[:size])
    return most_freq_dict


def get_bigramm_num(bigramm, alphabet):
    bigramm_num = alphabet.index(bigramm[0]) * len(alphabet) + alphabet.index(bigramm[1])
    return bigramm_num


def get_bigramm_by_num(bigramm_num, alphabet):
    return alphabet[bigramm_num//len(alphabet)] + alphabet[bigramm_num % len(alphabet)]


class AphineCypher:
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def encrypt_bigramm(self, sym1, sym2, a, b):
        x = get_bigramm_num(sym1 + sym2, self.alphabet)
        m = len(self.alphabet)
        y = (a*x + b) % (m*m)
        enc_bigramm = get_bigramm_by_num(y, self.alphabet)
        return enc_bigramm

    def decrypt_bigramm(self, sym1, sym2, a, b):
        y = get_bigramm_num(sym1 + sym2, self.alphabet)
        m = len(self.alphabet)
        x = (calc_reverse_by_mod(a, m * m) * (y-b)) % (m * m)
        dec_bigramm = get_bigramm_by_num(x, self.alphabet)
        return dec_bigramm

    def encrypt(self, text, a, b):
        enc_text = list()
        i = 1
        while i < len(text):
            enc_text.append(self.encrypt_bigramm(text[i - 1], text[i], a, b))
            i = i + 2
        return ''.join(enc_text)

    def decrypt(self, enc_text, a, b):
        text = list()
        i = 1
        while i < len(enc_text):
            text.append(self.decrypt_bigramm(enc_text[i - 1], enc_text[i], a, b))
            i = i + 2
        return ''.join(text)


class HackTheKey:
    def __init__(self, alphabet, control_bigramms):
        self.alphabet = alphabet
        self.control_bigramms = control_bigramms
        self.aphine = AphineCypher(self.alphabet)

    def find_key(self, enc_bigramm_num1, enc_bigramm_num2, dec_bigramm_num1, dec_bigramm_num2):
        x = dec_bigramm_num1 - dec_bigramm_num2
        y = enc_bigramm_num1 - enc_bigramm_num2
        m = len(self.alphabet)
        a = calc_linear_comparison(x, y, m*m)
        b = (enc_bigramm_num1 - a*dec_bigramm_num1) % (m*m)
        return a, b

    def generate_suitable_keys(self, most_freq_bigramms, most_freq_bigramms_enc):
        enc_bigramm_pairs = list(permutations(most_freq_bigramms_enc, 2))
        dec_bigramm_pairs = list(permutations(most_freq_bigramms, 2))
        suitable_keys = list()
        for i in enc_bigramm_pairs:
            for j in dec_bigramm_pairs:
                suitable_keys.append(self.find_key(get_bigramm_num(i[0], self.alphabet),
                                                   get_bigramm_num(i[1], self.alphabet),
                                                   get_bigramm_num(j[0], self.alphabet),
                                                   get_bigramm_num(j[1], self.alphabet)
                                                   )
                                     )
        return list(dict.fromkeys(suitable_keys))

    def check_text_readability(self, text):
        for bigramm in self.control_bigramms:
            if bigramm in text:
                return False
        if text.count('о')/len(text) < 0.10 or text.count('а')/len(text) < 0.07:
            return False
        return True

    def filter_keys(self, key_pairs, enc_text):
        most_suitable_keys = list()
        for key_pair in key_pairs:
            text = self.aphine.decrypt(enc_text, key_pair[0], key_pair[1])
            if self.check_text_readability(text):
                most_suitable_keys.append(key_pair)
        return most_suitable_keys


def main():
    aphine = AphineCypher(rus_alphabet)
    hack_the_key = HackTheKey(rus_alphabet, control_bigramms_rus)
    with open('encrypted.txt', 'r') as enc_text_file:
        enc_text = enc_text_file.read()
        enc_text_list = list()
        for i in enc_text:
            if i != '\n' and i != ' ':
                enc_text_list.append(i)
        enc_text = ''.join(enc_text_list)
        most_freq_bigramms = get_most_freq_bigramms(calc_all_bigramm_freq(rus_alphabet, enc_text), 5)
        key_pairs = hack_the_key.generate_suitable_keys(rus_most_freq_bigramms, most_freq_bigramms.keys())
        print('Amount of suitable keys: ' + str(len(key_pairs)))

        key_pairs = hack_the_key.filter_keys(key_pairs, enc_text)
        len_of_filtered_keys = len(key_pairs)
        print('Amount of filtered keys: ' + str(len_of_filtered_keys))

        if len(key_pairs) == 0:
            print("There is no suitable keys!")
        elif len(key_pairs) == 1:
            print("Target key is: " + str(key_pairs))
            target_key_pair = key_pairs[0]
            open_text = aphine.decrypt(enc_text, target_key_pair[0], target_key_pair[1])
            open_text_with_breaks = insert_line_breaks(open_text, 200)
            print("Open text: \n")
            print(open_text_with_breaks)
            with open('decrypted.txt', 'w') as decrypted_text_file:
                decrypted_text_file.write(open_text_with_breaks)
        else:
            print("There are too much keys - try to filter it manually!")
            print("Keys: " + str(key_pairs))


if __name__ == '__main__':
    main()
