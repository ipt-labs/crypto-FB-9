import re
import collections
from collections import Counter
from math import log2

f = open('text.txt', encoding='UTF-8')
out = open('output.txt', 'w', encoding='UTF-8')
file_txt = f.read().lower()

file_txt = re.sub('ъ', 'ь', file_txt)
file_txt = re.sub('ё', 'е', file_txt)
file_txt_no_spaces = re.sub(' ', '', file_txt)




def freq_letters(str):
    freq_l = collections.Counter(str)
    for v in freq_l.keys():
        freq_l[v] /= len(file_txt_no_spaces)
    return freq_l

def entropy(freq_l):
    entropy = 0
    for val in freq_l.values():
        entropy += -val * log2(val)
    return entropy

def freq_bigrams(str):
    frequency = Counter(str[bi: bi + 2] for bi in range(len(str) - 1))
    for key in frequency.keys():
        frequency[key] /= len(str)
    return frequency

def freq_bigram_wo_croses(str):
    frequency = Counter(str[bi: bi + 2] for bi in range(0, len(str) - 1, 2))
    for key in frequency.keys():
        frequency[key] /= len(str)
    return frequency

def out_put(v):
    for letter in v:
        out.write(f'{letter} -- {str(v[letter])}\n')
    out.write(f'\n\n')

letters_w_spaces = freq_letters(file_txt)
letters_wo_spaces = freq_letters(file_txt_no_spaces)

bigrams_w_spaces_frequency = freq_bigrams(file_txt)
bigrams_wo_spaces_frequency = freq_bigrams(file_txt_no_spaces)

bigrams_w_spaces_wo_intersections_frequency = freq_bigram_wo_croses(file_txt)
bigrams_wo_spaces_wo_intersections_frequency = freq_bigram_wo_croses(file_txt_no_spaces)

letters_w_spaces_entropy = entropy(letters_w_spaces)
letters_wo_spaces_entropy = entropy(letters_wo_spaces)

bigrams_w_spaces_entropy = entropy(bigrams_w_spaces_frequency) / 2
bigrams_wo_spaces_entropy = entropy(bigrams_wo_spaces_frequency) / 2

bigrams_w_spaces_wo_intersections_entropy = entropy(bigrams_w_spaces_wo_intersections_frequency) / 2
bigrams_wo_spaces_wo_intersections_entropy = entropy(bigrams_wo_spaces_wo_intersections_frequency) / 2

out.write(f'Entropy:\n'
             f'Letters with spaces:\n{letters_w_spaces_entropy}\n'
             f'Letters without spaces:\n{letters_wo_spaces_entropy}\n'
             f'Bigrams with spaces:\n{bigrams_w_spaces_entropy}\n'
             f'Bigrams without spaces:\n{bigrams_wo_spaces_entropy}\n'
             f'Bigrams with spaces, without intersections:\n{bigrams_w_spaces_wo_intersections_entropy}\n'
             f'Bigrams without spaces, without intersections:\n{bigrams_wo_spaces_wo_intersections_entropy}\n\n')
out.write(f'Letters with spaces frequency:\n')
out_put(letters_w_spaces)
out.write(f'Letters without spaces frequency:\n')
out_put(letters_wo_spaces)
out.write(f'Bigrams with spaces frequency:\n')
out_put(bigrams_w_spaces_frequency)
out.write(f'Bigrams without spaces frequency:\n')
out_put(bigrams_wo_spaces_frequency)
out.write(f'Bigrams with spaces, without intersections frequency:\n')
out_put(bigrams_w_spaces_wo_intersections_frequency)
out.write(f'Bigrams without spaces, without intersections frequency:\n')
out_put(bigrams_wo_spaces_wo_intersections_frequency)
print(letters_w_spaces)
print(letters_wo_spaces)
print(bigrams_w_spaces_frequency)
print(bigrams_wo_spaces_frequency)
print(bigrams_w_spaces_wo_intersections_frequency)
print(bigrams_wo_spaces_wo_intersections_frequency)
print(letters_w_spaces_entropy)
print(letters_wo_spaces_entropy)
print(bigrams_w_spaces_entropy)
print(bigrams_wo_spaces_entropy)
print(bigrams_w_spaces_wo_intersections_entropy)
print(bigrams_wo_spaces_wo_intersections_entropy)




