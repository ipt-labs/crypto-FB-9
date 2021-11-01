import collections
import sys
import string
# .translate({ord(c): None for c in string.whitespace})
import xlwt
from xlwt import Workbook
from math import log2


# function that i used to filter all chars that interfere entropy counting
def prefilter_text(alphabet, filename):
    with open(filename, "r", encoding='utf-8') as f:
        my_text = f.read().lower()
        my_text = my_text.replace("\n", " ").replace("\r", "").replace("\t", " ").replace("ё", "е").replace("ъ", "ь")
        for char in my_text[:]:
            if char not in alphabet:
                my_text = my_text.replace(char, " ")
        my_text = " ".join(my_text.split())
        return my_text


def count_char_frequency(alphabet, text_to_read):
    char_frequency_counted = {}
    for char in alphabet:
        count_the_char = text_to_read.count(char)
        char_frequency_counted[char] = count_the_char / len(text_to_read)
    return sorted(char_frequency_counted.items(), key=lambda x: x[1], reverse=True)


def count_bigram_frequency(alphabet, text_to_read, outputfile):
    bigram_frequency_counted = {}
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    iter1 = 0
    for i in alphabet:
        iter1 = iter1 + 1
        iter2 = 0
        sheet1.write(0, iter1, str(i))
        sheet1.write(iter1, 0, str(i))
        for j in alphabet:
            iter2 = iter2 + 1
            count_the_bigram = text_to_read.count(str(i + j))
            bigram_frequency_counted[str(i + j)] = count_the_bigram / len(text_to_read)
            sheet1.write(iter1, iter2, str(bigram_frequency_counted[str(i + j)]))
    wb.save(outputfile)
    return sorted(bigram_frequency_counted.items(), key=lambda x: x[1], reverse=True)

def count_bigram_intersetion_frequency(alphabet, text_to_read, outputfile):
    bigram_frequency_counted = {}
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')

    size = len(text_to_read)
    counter = collections.Counter()
    for i in range(0, size, 2):
        bigram = text_to_read[i:i+2]
        counter[bigram] += 1

    for bigram, count_the_bigram in counter.items():
        bigram_frequency_counted[bigram] = count_the_bigram / sum(counter.values())

    iter1 = 0
    for i in alphabet:
        iter1 = iter1 + 1
        iter2 = 0
        sheet1.write(0, iter1, str(i))
        sheet1.write(iter1, 0, str(i))
        for j in alphabet:
            iter2 = iter2 + 1
            if str(i + j) in bigram_frequency_counted.keys():
                sheet1.write(iter1, iter2, str(bigram_frequency_counted[str(i + j)]))
            else:
                sheet1.write(iter1, iter2, '0')
            
    wb.save(outputfile)
    return sorted(bigram_frequency_counted.items(), key=lambda x: x[1], reverse=True)




def count_entropy(frequency, amount) -> float:
    entropy = 0
    for i in frequency:
        if i[1] != 0:
            entropy += i[1] * log2(i[1])
    entropy *= -1 / amount
    return entropy


def owerflow(entropy, amount):
    return 1 - (entropy / log2(amount))


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit("No arguments")
    a = ord('а')
    russ_alphabet = [chr(i) for i in range(a, a + 32)]
    # print (russ_alphabet)
    russ_alphabet.remove('ъ')
    russ_alphabet_without_whitespace = russ_alphabet
    russ_alphabet.append(' ')

    filtered_text_with_whitespaces = prefilter_text(russ_alphabet, sys.argv[1])
    new_filename = 'filtered_text_with_whitespaces' + str(sys.argv[1])
    with open(new_filename, 'w', encoding='utf-8') as f:
        f.write(filtered_text_with_whitespaces)
        f.close()

    filtered_text_without_whitespaces = filtered_text_with_whitespaces.translate(
        {ord(c): None for c in string.whitespace})
    new_filename = 'filtered_text_without_whitespaces' + str(sys.argv[1])
    with open(new_filename, 'w', encoding='utf-8') as f:
        f.write(filtered_text_without_whitespaces)
        f.close()

    char_frec_with_whitespace = count_char_frequency(russ_alphabet, filtered_text_with_whitespaces)
    print("char_frec_with_whitespace:\n-------")
    for i in char_frec_with_whitespace:
        print(i[0], i[1])

    char_frec_without_whitespace = count_char_frequency(russ_alphabet_without_whitespace,
                                                        filtered_text_without_whitespaces)
    print("char_frec_without_whitespace:\n-------")
    for i in char_frec_without_whitespace:
        print(i[0], i[1])

    bigram_frec_with_whitespace = count_bigram_frequency(russ_alphabet, filtered_text_with_whitespaces,
                                                         'bigram_frec_with_whitespace.xls')
    print("bigram_frec_with_whitespace:\n-------")
    for i in bigram_frec_with_whitespace:
        print(i[0], i[1])

    bigram_frec_without_whitespace = count_bigram_frequency(russ_alphabet_without_whitespace,
                                                            filtered_text_without_whitespaces,
                                                            'bigram_frec_without_whitespace.xls')
    print("bigram_frec_without_whitespace:\n-------")
    for i in bigram_frec_without_whitespace:
        print(i[0], i[1])

    bigram_frec_with_whitespace_not_shifted = count_bigram_intersetion_frequency(russ_alphabet,
                                                                           filtered_text_with_whitespaces,
                                                                           'bigram_frec_with_whitespace_insertion.xls')
    print("bigram_frec_with_whitespace_not_shifted:\n-------")
    for i in bigram_frec_with_whitespace_not_shifted:
        print(i[0], i[1])

    bigram_frec_without_whitespace_not_shifted = count_bigram_intersetion_frequency(russ_alphabet_without_whitespace,
                                                                              filtered_text_without_whitespaces,
                                                                              'bigram_frec_without_whitespace_insertion.xls')
    print("bigram_frec_without_whitespace_not_shifted:\n-------")
    for i in bigram_frec_without_whitespace_not_shifted:
        print(i[0], i[1])

    print('-------------------------------------------------------\n----------------------------------------------')
    h1_withspaces = count_entropy(char_frec_with_whitespace, 1)
    print('H1 with ' + str(h1_withspaces))
    h1_withoutspaces = count_entropy(char_frec_without_whitespace, 1)
    print('H1 without ' + str(h1_withoutspaces))
    h2_withspaces = count_entropy(bigram_frec_with_whitespace, 2)
    print('H2 with ' + str(h2_withspaces))
    h2_withoutspaces = count_entropy(bigram_frec_without_whitespace, 2)
    print('H2 without ' + str(h2_withoutspaces))

    h2_withspaces_not_shifted = count_entropy(bigram_frec_with_whitespace_not_shifted, 2)
    print('H2 not shifted with ' + str(h2_withspaces_not_shifted))
    h2_withoutspaces_not_shifted = count_entropy(bigram_frec_without_whitespace_not_shifted, 2)
    print('H2 not shifted without ' + str(h2_withoutspaces_not_shifted))

    h1_withspaces_ower = owerflow(h1_withspaces, len(russ_alphabet))
    print('H1 with spaces owerflow ' + str(h1_withspaces_ower))
    h1_withoutspaces_ower = owerflow(h1_withoutspaces, len(russ_alphabet_without_whitespace))
    print('H1 without spaces owerflow ' + str(h1_withoutspaces_ower))
    h2_withspaces_ower = owerflow(h2_withspaces, len(russ_alphabet))
    print('H2 with spaces owerflow ' + str(h2_withspaces_ower))
    h2_withoutspaces_ower = owerflow(h2_withoutspaces, len(russ_alphabet_without_whitespace))
    print('H2 without spaces owerflow ' + str(h2_withoutspaces_ower))
