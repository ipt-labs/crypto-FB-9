from itertools import permutations

def gcdExtended(a, b):
    if a == 0 :
        return b, 0, 1
    gcd, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b//a) * x1
    y = x1
    return gcd, x, y

def inverted(a, m):
    g, x, _ = gcdExtended(a, m)
    if g == 1:
        return x % m

def linearcomparison(a, b, m):
    gcd, x, y = gcdExtended(a, m)
    if gcd == 1:
        x = ((inverted(a, m))*b) % m
        return x
    elif b % gcd != 0:
        return -1
    else:
        a, b, m = a//gcd, b//gcd, m//gcd
        x0 = linearcomparison(a, b, m)
        return x0

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

f = open('text.txt', 'r', encoding='utf-8')
opentext = f.read()
f.close()

bigram_freq = {}

for i in range(len(opentext)-1):
    bigram = (opentext[i], opentext[i+1])
    if bigram not in bigram_freq:
        bigram_freq[bigram] = 0
    bigram_freq[bigram] += 1

bigram_sorted = []

for i in sorted(bigram_freq, key=bigram_freq.get, reverse=True):
    bigram_sorted.append(i)

bigram_5 = [bigram_sorted[i] for i in range(len(bigram_sorted)) if i < 5]

bigrams_text = []
for i in bigram_5:
    bigrams_text.append(''.join(i))

bigrams_lang = ['ст', 'но', 'ен', 'то', 'на']

def bigram_to_number(bigram, m):
    return alphabet.find(bigram[0]) * m + alphabet.find(bigram[1])

def number_to_bigram(number, m):
    return alphabet[number//m] + alphabet[number % m]

def create_key(x1, x2, y1, y2, m):
    Y = bigram_to_number(y1, m) - bigram_to_number(y2, m)
    X = bigram_to_number(x1, m) - bigram_to_number(x2, m)
    a = linearcomparison(X, Y, m**2)
    b = (bigram_to_number(y1, m) - a * bigram_to_number(x1, m)) % m**2
    return [a, b]

def create_keys(bigram_lang, bigram_text):
    perm_lang = list(permutations(bigram_lang, 2))
    perm_text = list(permutations(bigram_text, 2))

    perm = []
    for i in range(len(perm_lang)):
        perm.append(perm_lang[i] + perm_text[i])
    
    keys = []
    for i in range(20):
        keys.append(create_key(perm[i][0], perm[i][1], perm[i][2], perm[i][3], 31))
    return keys

keys = create_keys(bigrams_lang, bigrams_text)

def dec_bigram(a, b, m, bigram):
    Y = bigram_to_number(bigram, m)
    X = (inverted(a, m**2) * (Y - b)) % m**2
    return number_to_bigram(X, m)

def decrypt(a, b, m, text):
    dec_text = []
    text = [text[i:i + 2] for i in range(0, len(text), 2)]

    for i in range(len(text)):
        dec_text.append(dec_bigram(a, b, m, text[i]))

    dec_text = ''.join(dec_text)

    if dec_text.count('е')/len(dec_text) < 0.05 or dec_text.count('а')/len(dec_text) < 0.05:
        return -1
    else:
        return dec_text

def finally_decrypt_text(text, m, keys):
    for i in range(len(keys)):
        dec_text = decrypt(keys[i][0], keys[1][1], m, text)
        if dec_text == -1:
            continue
        else:
            f = open('c.txt', 'a', encoding='utf-8')
            f.write(dec_text)
            f.write('\n\n\n')
            f.close()

finally_decrypt_text(opentext, 31, keys)