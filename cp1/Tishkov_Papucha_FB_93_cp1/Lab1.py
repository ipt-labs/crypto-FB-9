#coding=UTF-8
import math
from contextlib import contextmanager
import pandas as pd

rus_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']


def calc_symbol_freq(symbol, text):
    symbol_counter = 0
    for text_symbol in text:
        if symbol == text_symbol:
            symbol_counter = symbol_counter + 1
    return symbol_counter / len(text)


def calc_all_symbols_freq(alphabet, text, is_space_allowed = False, log_file_name = None):
    symbol_num_dict = {}
    symbol_freq_dict = {}
    if is_space_allowed:
        alphabet.append(' ')
    for letter in alphabet:
        symbol_num_dict.update({letter: 0})
        symbol_freq_dict.update({letter: 0})
    for symbol in text:
        symbol_num_dict[symbol] = symbol_num_dict[symbol] + 1
    for symbol in alphabet:
        symbol_freq_dict[symbol] = symbol_num_dict[symbol] / len(text)
    
    if log_file_name != None:
        sorted_symbol_freq_dict = dict(sorted(symbol_freq_dict.items(), key=lambda item: item[1], reverse=True))
        out_df = pd.DataFrame.from_dict(sorted_symbol_freq_dict, orient='index', columns=['Frequency'])
        out_df.to_excel(log_file_name + '.xlsx')

    return symbol_freq_dict
    

def calc_monogramm_entropy(alphabet, text, is_space_allowed = False):
    entropy = 0
    monogramm_freq_dict = calc_all_symbols_freq(alphabet, text, is_space_allowed)
    for monogramm_freq in monogramm_freq_dict.values():
        entropy = entropy + (monogramm_freq * math.log(monogramm_freq, 2))
    entropy = entropy * -1
    return entropy


def calc_bigramm_freq(bigramm, text, is_intersec_allowed = False):
    text_len = 0
    bigramm_counter = 0
    if not is_intersec_allowed and len(text) % 2 > 0:
        text_len = len(text - 1)
    else:
        text_len = len(text)

    index = 0
    while index < text_len - 1:
        if bigramm == text[index] + text[index + 1]:
            bigramm_counter = bigramm_counter + 1
        if is_intersec_allowed:
            index = index + 1
        else:
            index = index + 1

    frequency = bigramm_counter / (text_len / 2)
    return frequency


def calc_all_bigramm_freq(alphabet, text, is_space_allowed = False, is_intersec_allowed = False, log_file_name = None):
    bigramm_freq_dict = {}
    bigramm_num_dict = {}

    # Reduce text size if its length is odd
    if is_space_allowed:
        alphabet.append(' ')
    text_len = 0
    if len(text) % 2 == 0:
        text_len = len(text)
    else:
        text_len = len(text) - 1

    # Combine all letters for creating bigramms
    for sym1 in alphabet:
        for sym2 in alphabet:
            new_bigramm = sym1 + sym2
            bigramm_freq_dict.update({new_bigramm: 0})
            bigramm_num_dict.update({new_bigramm: 0})

    # Counting bigramm frequency
    index = 0
    while index < text_len - 1:
        sym1 = text[index]
        sym2 = text[index + 1]
        cur_bigramm = sym1 + sym2
        bigramm_num_dict[cur_bigramm] = bigramm_num_dict[cur_bigramm] + 1
        if is_intersec_allowed:
            index = index + 1
        else:
            index = index + 2
    for bigramm in bigramm_num_dict:
        divider = 0
        if is_intersec_allowed:
            divider = text_len - 1
        else:
            divider = text_len / 2
        bigramm_freq_dict.update({bigramm: bigramm_num_dict[bigramm]/divider})

    sorted_bigramm_freq_dict = dict(sorted(bigramm_freq_dict.items(), key=lambda item: item[1], reverse=True))
    if log_file_name is not None:
        out_df = pd.DataFrame.from_dict(sorted_bigramm_freq_dict, orient='index', columns=['Frequency'])
        out_df.to_excel(log_file_name + '.xlsx')
    return sorted_bigramm_freq_dict

def calc_bigramm_entropy(alphabet, text, is_space_allowed = False, is_intersec_allowed = False):
    bigramm_freq_dict = calc_all_bigramm_freq(alphabet, text, is_space_allowed, is_intersec_allowed)

    # Calculating entropy
    bigramm_entropy = 0
    for bigramm_freq in bigramm_freq_dict.values():
        if bigramm_freq == 0:
            continue
        bigramm_entropy = bigramm_entropy + bigramm_freq * math.log(bigramm_freq, 2)
    bigramm_entropy = bigramm_entropy / (-2)
    return bigramm_entropy
    

def make_text_only_alphabet_symbols(text, is_space_allowed):
    context = text
    new_context = str()
    is_prev_space = False
    for text_symbol in context:
        for rus_symbol in rus_alphabet:
            if text_symbol.lower() == rus_symbol:
                is_prev_space = False
                new_context = new_context + text_symbol.lower()
                break
            elif text_symbol == 'ъ':
                is_prev_space = False
                new_context = new_context + 'ь'
                break
            elif text_symbol == 'Ъ':
                is_prev_space = False
                new_context = new_context + 'Ь'
                break
            elif text_symbol == 'ё':
                is_prev_space = False
                new_context = new_context + 'е'
                break
            elif text_symbol == 'Ё':
                is_prev_space = False
                new_context = new_context + 'Е'
                break
            elif is_space_allowed and text_symbol == ' ':
                if is_prev_space:
                    break
                else:
                    is_prev_space = True
                    new_context = new_context + ' '
                
    return new_context


def redundant(entropy, alphabet, is_spaces_allowed = False, in_percents = False):
    multiplicator = 1
    if in_percents:
        multiplicator = 100
    if is_spaces_allowed:
        return (1 - (entropy/math.log2(len(alphabet) + 1))) * multiplicator
    else:
        return (1 - (entropy/math.log2(len(alphabet)))) * multiplicator


@contextmanager
def open_text(path, is_space_allowed):
    try:
        text_file = open(path, 'r')
        text_in = text_file.read()
        text_out = make_text_only_alphabet_symbols(text_in, is_space_allowed)
    except OSError:
        print("There is a problem with text file!")
    yield text_out
    text_file.close()


def main():

    is_space_allowed = False
    with open_text('dyuma.txt', is_space_allowed) as context:
        # Export monogramm freq
        calc_all_symbols_freq(rus_alphabet, context, is_space_allowed, 'monogramms')
        calc_all_bigramm_freq(rus_alphabet, context, is_space_allowed, False, 'bigramms')
        calc_all_bigramm_freq(rus_alphabet, context, is_space_allowed, True, 'bigramms_with_intersec')
        print("Monogramm entropy:")
        h1 = calc_monogramm_entropy(rus_alphabet, context, is_space_allowed)
        print(h1)
        print("Redundant:")
        print(redundant(h1, rus_alphabet, is_space_allowed, True))
        print("Bigramm entropy:")
        h2_without_intersec = calc_bigramm_entropy(rus_alphabet, context, is_space_allowed, False)
        print(h2_without_intersec)
        print("Redundant:")
        print(redundant(h2_without_intersec, rus_alphabet, is_space_allowed, True))
        print("Bigramm entropy with intersection:")
        h2_with_intersec = calc_bigramm_entropy(rus_alphabet, context, is_space_allowed, True)
        print(h2_with_intersec)
        print("Redundant:")
        print(redundant(h2_with_intersec, rus_alphabet, is_space_allowed, True))

    is_space_allowed = True
    with open_text('dyuma.txt', is_space_allowed) as context:
        # Export monogramm freq
        calc_all_symbols_freq(rus_alphabet, context, is_space_allowed, 'monogramms_with_spaces')
        calc_all_bigramm_freq(rus_alphabet, context, is_space_allowed, False, 'bigramms_with_spaces')
        calc_all_bigramm_freq(rus_alphabet, context, is_space_allowed, True, 'bigramms_with_spaces_and_intersec')
        print("Monogramm entropy with spaces:")
        h1 = calc_monogramm_entropy(rus_alphabet, context, is_space_allowed)
        print(h1)
        print("Redundant:")
        print(redundant(h1, rus_alphabet, is_space_allowed, True))
        print("Bigramm entropy with spaces:")
        h2_without_intersec = calc_bigramm_entropy(rus_alphabet, context, is_space_allowed, False)
        print(h2_without_intersec)
        print("Redundant:")
        print(redundant(h2_without_intersec, rus_alphabet, is_space_allowed, True))
        print("Bigramm entropy with spaces and intersection:")
        h2_with_intersec = calc_bigramm_entropy(rus_alphabet, context, is_space_allowed, True)
        print(h2_with_intersec)
        print("Redundant:")
        print(redundant(h2_with_intersec, rus_alphabet, is_space_allowed, True))

def Lab2():
    new_context = ''
    with open_text('dyuma.txt', False) as context:
        new_context = context
    new_text = open('dyuma2.txt', 'w')
    new_text.write(new_context)
    new_text.close()

if __name__ == '__main__':
    #main()
    Lab2()
    