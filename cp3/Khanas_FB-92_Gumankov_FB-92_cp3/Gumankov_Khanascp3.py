from typing import Union
from itertools import islice
import itertools

ru_alph = [chr(x) for x in range(ord('а'), ord('а') + 32)]
ru_alph.remove('ъ')
ru_alph[26], ru_alph[27] = ru_alph[27], ru_alph[26]
most_frequent_bs = ['ст', 'но', 'то', 'на', 'ен']

def iterative_egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a; m, n = x - u  *q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return b, x, y

def modinv(a, m):
    g, x, y = iterative_egcd(a, m) 
    if g != 1:
        return None
    else:
        return x % m

def solve_linear_comparison(a, b, n):
    g, x, y = iterative_egcd(a, n)
    if g != 1:
        if b % g == 0:
            a1, b1, n1 = a / g, b / g, n / g
            g0, x0, y0 = iterative_egcd(a1, n1)
            x0 = (b1 * x0) % n1
            all_results = [x0 + d * n1 for d in range(0, x)]
            return all_results

        else:
            return []
    else:
        return [(x * b) % n]

def take(n, iterable):
    return dict(islice(iterable, n))

def count_bigram_frequency(alphabet, text_to_read):
    bigram_frequency_counted = {}
   
    iter1 = 0
    for i in alphabet:
        iter1 = iter1 + 1
        iter2 = 0
        
        for j in alphabet:
            iter2 = iter2 + 1
            count_the_bigram = text_to_read.count(str(i + j))
            bigram_frequency_counted[str(i + j)] = count_the_bigram / len(text_to_read)
            
    return take(5, sorted(bigram_frequency_counted.items(), key=lambda x: x[1], reverse=True))


def b_tonum(b):
    return ru_alph.index(b[0]) * len(ru_alph) + ru_alph.index(b[1])

def get_pairs(most_frequent_bs, most_frequent_enc_bs):
    l = list(itertools.product(most_frequent_bs, most_frequent_enc_bs))
    l = list(itertools.product(l, l))
    filtered = filter(lambda pairs: pairs[0][0] != pairs[1][0] and pairs[0][1] != pairs[1][0] and pairs[0][0] != pairs[1][1] and pairs[0][1] != pairs[1][1], l)
    return list(filtered)

forbidden_lst = ["аь", "еь", "иь", "оь", "уь", "юь", "яь", "эь", "ыь", "жы", "шы", "яы", "ьь", "яь", "эы", "эь"]


def decryptor(a, b, text):
  plaintext = ''
  n = len(ru_alph)
  g, x, y = iterative_egcd(a, n**2)

  for bi in [text[idx: idx + 2] for idx in range(0, (len(text)), 2)]:
    bi_idx = b_tonum(bi)
    deciph_bi = ((bi_idx - b) * x) % (n**2)

    x2_idx = deciph_bi % n
    x1_idx = (deciph_bi - x2_idx) / n

    x1 = ru_alph[int(x1_idx)]
    x2 = ru_alph[int(x2_idx)]
    if x1+x2 not in forbidden_lst:
      plaintext += x1 + x2
    else:
      return False

  return plaintext


with open('08.txt', encoding='utf-8') as f:
    text = ''
    for line in f:
        text += line.replace("\n", "")
    freq = count_bigram_frequency(ru_alph, text)
    print(freq.keys())
    pairs = get_pairs(most_frequent_bs, freq.keys())
    for (pair1, pair2) in pairs:
        y1 = b_tonum(pair1[0])
        x1 = b_tonum(pair1[1])

        y2 = b_tonum(pair2[0])
        x2 = b_tonum(pair2[1])

        a = y1 - y2
        b = x1 - x2
        n = len(ru_alph)**2

        a_k = solve_linear_comparison(a, b, n);

        for a in a_k:
            b = (x1 - y1 * a) % n
            text_d = decryptor(a, b, text)

            if text_d != False:
                print(f"a: {a}, b: {b}")
                print(text_d)
                exit(0)