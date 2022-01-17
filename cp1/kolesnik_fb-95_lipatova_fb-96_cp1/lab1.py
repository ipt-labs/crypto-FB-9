import math
import csv
from io import open

f = open('text.txt', encoding='utf-8')
text = f.read()
f.close()
text = text.lower()
text = ' '.join(text.split())

alphabet = 'а#б#в#г#д#е#ё#ж#з#и#й#к#л#м#н#о#п#р#с#т#у#ф#х#ц#ч#щ#ъ#ы#ь#э#ю#я# '.split('#')

preptext = ''

for i in text:
    if i in alphabet:
        preptext = preptext + i

char_freq = {}

for i in preptext:
    keys = char_freq.keys()
    if i in keys:
        char_freq[i] += 1
    else:
        char_freq[i] = 1

bigram_freq = {}

for i in range(len(preptext)-1):
    bigram = (preptext[i], preptext[i+1])
    if bigram not in bigram_freq:
        bigram_freq[bigram] = 0
    bigram_freq[bigram] += 1

char_prob = {key: char_freq[key] / len(preptext) for key in char_freq.keys()}
bigram_prob = {key: bigram_freq[key] / sum(bigram_freq.values()) for key in bigram_freq.keys()}

h1s = sum(list(map(lambda x: -x * math.log2(x), char_prob.values())))
h2s = 1/2 * sum(list(map(lambda x: -x * math.log2(x), bigram_prob.values())))

alphabetnospace = 'а#б#в#г#д#е#ё#ж#з#и#й#к#л#м#н#о#п#р#с#т#у#ф#х#ц#ч#щ#ъ#ы#ь#э#ю#я'.split('#')

preptexts = ''

for i in text:
    if i in alphabetnospace:
        preptexts = preptexts + i

char_freqs = {}

for i in preptexts:
    keys = char_freqs.keys()
    if i in keys:
        char_freqs[i] += 1
    else:
        char_freqs[i] = 1

bigram_freqs = {}

for i in range(len(preptexts)-1):
    bigram = (preptexts[i], preptexts[i+1])
    if bigram not in bigram_freqs:
        bigram_freqs[bigram] = 0
    bigram_freqs[bigram] += 1

char_probs = {key: char_freqs[key] / len(preptexts) for key in char_freqs.keys()}
bigram_probs = {key: bigram_freqs[key] / sum(bigram_freqs.values()) for key in bigram_freqs.keys()}

h1ns = sum(list(map(lambda x: -x * math.log2(x), char_probs.values())))
h2ns = 1/2 * sum(list(map(lambda x: -x * math.log2(x), bigram_probs.values())))

print('H1 with spaces:', h1s, '\nH2 with spaces:', h2s, '\nH1 without spaces:', h1ns, '\nH2 without spaces:', h2ns)

f = open('char prob whitespaces.txt', 'w', encoding='utf-8')
writer = csv.writer(f)
for key, value in char_prob.items():
    writer.writerow([key, value])

f = open('char prob no whitespaces.txt', 'w', encoding='utf-8')
writer = csv.writer(f)
for key, value in char_probs.items():
    writer.writerow([key, value])

f = open('bigram prob whitespaces.txt', 'w', encoding='utf-8')
writer = csv.writer(f)
for key, value in bigram_prob.items():
    writer.writerow([key, value])

f = open('bigram prob no whitespaces.txt', 'w', encoding='utf-8')
writer = csv.writer(f)
for key, value in bigram_probs.items():
    writer.writerow([key, value])