from collections import Counter

with open('text.txt', 'r', encoding = 'utf-8') as f:
    plaintext = f.read()

alph = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']

keys = {2:'ай',3:'кот',4:'мать',5:'жесть',10:'разложение',11:'превращение',12:'трагикомедия',13:'недоразумение',14:'нравственность',
        15:'амариллисцветок',16:'мягенькаяподушка',17:'пельменискетчупом',18:'неспатьаделатьлабу',19:'киберполицияукраины',20:'женоненавистничесвто'}


def encryption(r):
    ciphertext = []
    for i in range(len(plaintext)):
        y = (alph.index(plaintext[i]) + alph.index(keys[r][i%r]))%32
        ciphertext.append(alph[y])
    return ciphertext


