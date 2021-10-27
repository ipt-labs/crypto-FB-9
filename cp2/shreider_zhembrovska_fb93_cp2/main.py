from collections import Counter

with open('text.txt', 'r', encoding = 'utf-8') as f:
    plaintext = f.read()

alph = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']
keys = ['ай','кот','мать','жесть','разложение','превращение','трагикомедия','недоразумение','нравственность',
        'амариллисцветок','мягенькаяподушка','пельменискетчупом','неспатьаделатьлабу','киберполицияукраины','женоненавистничесвто']


def encryption(text,key):
    ciphertext = []
    for i in range(len(text)):
        y = (alph.index(text[i])+alph.index(key[i%len(key)]))%32
        ciphertext.append(alph[y])
    return ''.join(i for i in ciphertext)


