import math
from collections import Counter
import re


# відкриваємо файл
def openfile(t):
    with open(t, 'r', encoding='utf-8') as file:
        text = file.read().lower()

    return text
# редагуємо текст- заміняємо всі знаки(, замінюємо великі букви на маленькі

def edit_text(t):
    with open(t, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    # openfile(t)

    text = re.sub("[^А-Яа-я]", " ", text)
    text = text.replace("ъ", "ь").replace("ё", "е")
    with open('withspaces.txt', 'w', encoding='utf-8') as file:
        file.write(text)
    # return text
# видаляємо пробіли та записуємо в окремий файл текст без пробілів
def deleteSpaces(t):
    with open(t, 'r', encoding='utf-8') as file:
        text1 = file.read()

    text1 = text1.replace(' ', '')  # for t in text1]

    with open('withoutspaces.txt', 'w', encoding='utf-8') as file:
        file.writelines(text1)


edit_text('unedited.txt')
text_with_spaces = openfile('withspaces.txt')
deleteSpaces('withspaces.txt')
text_without_spaces = openfile('withoutspaces.txt')


def count_letters(t):
    d = {}
    # рахуємо частоту букв(монограм)
    d = Counter(t)
    for i in d.keys():
        d[i] = d[i] / len(t)
    sorted_d = {}
    # сортуємо значення у спадному порядку
    sorted_values = sorted(d.values(), reverse=True)
    for i in sorted_values:
        for k in d.keys():
            if d[k] == i:
                sorted_d[k] = d[k]
                break
    print(sorted_d)
    # рахуємо ентропію для монограм
    entropyMono = 0
    for i in d.keys():
        entropy = (-d[i] * math.log2(d[i]))
        entropyMono += entropy
    entropyMono = round(entropyMono, 8)
    print("Entropy for monogram:\n")
    print(entropyMono)
    return (entropyMono)


def count_bigrams(t, intersection):
    bigram = []
    if intersection == True:  # для перехресної
        bigram = [t[i:i + 2] for i in range(len(t))]  # розділяємо на біграми (масив з біграм)
        count = Counter(bigram)  # рахує кількість кожної біграми (біграма це ключ, а значення це кількість)
    else:
        length = len(t)
        if len(t) % 2 == 1:
            length = len(t) - 1
        bigram = [t[i:i + 2] for i in range(0, length, 2)]
        count = Counter(bigram)
    lengthbigram = len(bigram)
    ans = {}
    ans = {i: round(count[i] / lengthbigram, 10) for i in count}
    sorted_ans = {}
    sorted_values = sorted(ans.values(), reverse=True)
    for i in sorted_values:
        for k in ans.keys():
            if ans[k] == i:
                sorted_ans[k] = ans[k]
                break
    print(sorted_ans)
    entropyBigram = 0
    for i in count.values():
        entropyBigram += - (i / len(bigram)) * math.log2(i / len(bigram))
    entropyBigram = entropyBigram / 2
    print("Entropy for bigram")
    print(entropyBigram)
    return entropyBigram


print("Monograms for text_with_spaces: \n")
entropy = count_letters(text_with_spaces)
print("Redundant: \n")
redundant = 1 - (entropy / math.log2(32))
print(redundant)
print("Monograms for text_without_spaces: \n")
entropy = count_letters(text_without_spaces)
print("Redundant: \n")
redundant = 1 - (entropy / math.log2(31))
print(redundant)

print("Bigrams for text_with_spaces and with intersection: \n")
entropy = count_bigrams(text_with_spaces, True)
print("Redundant: \n")
redundant = 1 - (entropy / math.log2(32))
print(redundant)
print("Bigrams for text_with_spaces and without intersection: \n")
entropy = count_bigrams(text_with_spaces, False)
print("Redundant: \n")
redundant = 1 - (entropy / math.log2(32))
print(redundant)
print("Bigrams for text_without_spaces and with intersection: \n")
entropy = count_bigrams(text_without_spaces, True)
print("Redundant: \n")
redundant = 1 - (entropy / math.log2(31))
print(redundant)
print("Bigrams for text_without_spaces and without intersection: \n")
entropy = count_bigrams(text_without_spaces, False)
print("Redundant: \n")
redundant = 1 - (entropy / math.log2(31))
print(redundant)