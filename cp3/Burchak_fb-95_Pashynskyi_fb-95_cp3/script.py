import os   # для перезапису файлів
import itertools  # для отримання перестановок

chars = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
         'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

# зчитування шифротексту і його фільтрація
f = open(".\\05.txt", "r", encoding="utf-8")
e_text = f.read()
f.close()
A = []
for ch in e_text:
    if ch in chars:
        A.append(ch)
e_text = ''.join(A)


# ф-я отримання масиву біграм з заданого тексту
def Get_bigram_array(text):
    A = []
    for i in range(0, len(text) - 1, 2):
        b = text[i] + text[i + 1]
        A.append(b)
    return A


# ф-я знаходження найчастіших біграм в тексті
def Find_max_freq_bigrams(A):
    freq = []
    max_freq_bigrams = []

    A_u = sorted(set(A), key=A.index)
    for b in A_u:
        freq.append(A.count(b))

    for i in range(5):
        max_freq_bigrams.append(A_u[freq.index(max(freq))])
        A_u.remove(A_u[freq.index(max(freq))])
        freq.remove(max(freq))
    return max_freq_bigrams


# ф-я отримання значень біграм
def Get_bigram_values(bigram_arr):
    A = []
    index_arr = []
    for i in range(len(bigram_arr)):
        for char in bigram_arr[i]:
            A.append(char)
        index_arr.append(chars.index(A[0]) * len(chars) + chars.index(A[1]))
        A = []
    # print(index_arr)
    return index_arr


# найбільший спільний дільник
def nsd(a, m):
    if a == 0:
        return (m, 0, 1)
    else:
        d, y, x = nsd(m % a, a)
        return (d, x - (m // a) * y, y)


# ф-я знаходження оберненого до а
def re(a, m):
    d, x, y = nsd(a, m)
    if d != 1:
        return 0
    else:
        return x % m


# ф-я знаходження ключа а,
# методом розв'язку лінійних рівнянь
def Find_key_a(P, C, m):
    d, x, y = nsd(P, m)
    if d == 1:
        a = (re(P, m) * C) % m
        return a
    else:
        P, C, m = int(P / d), int(C / d), int(m / d)
        a = Find_key_a(P, C, m)
        return a


# ф-я знаходження ключа b, що повертає обидва ключа
def Find_keys(ru, sht):   # P-біграма ru | C-біграма sht
    K = []
    # формування списків перестановок найчастіших біграм
    perestanovki_P = list(itertools.permutations(ru, 2))
    perestanovki_C = list(itertools.permutations(sht, 2))

    # розв'язання рівнянь
    for i in range(len(perestanovki_P)):
        P = (perestanovki_P[i][0] - perestanovki_P[i][1]) % 961
        C = (perestanovki_C[i][0] - perestanovki_C[i][1]) % 961
        a = Find_key_a(P, C, 961)
        b = (perestanovki_C[i][0] - a * perestanovki_P[i][0]) % 961
        K.append((a, b))
    return K


# ф-я розшифровки
def decode(a, b, text):
    P = []
    b_sht = Get_bigram_values(Get_bigram_array(text))
    for val in b_sht:
        # формула дешифровки
        p = re(a, 961) * (val - b) % 961
        # отримання індексів літер з біграми
        p_1 = int(p / len(chars))   # перша літера
        P.append(chars[p_1])
        p_2 = p % len(chars)    # друга
        P.append(chars[p_2])
    return ''.join(P)


# найчастіші біграми в мові та шифротексті,
# а також їх числові значення
max_freq_ru = ['ст', 'но', 'ен', 'то', 'на']    # from gogle
max_freq_sht = Find_max_freq_bigrams(Get_bigram_array(e_text))
ind_ru = Get_bigram_values(max_freq_ru)
ind_sht = Get_bigram_values(max_freq_sht)
print("\nMost frequent bigrams in russian lang:")
print(max_freq_ru)
print(ind_ru)
print("\nMost frequent bigrams in cyphertext:")
print(max_freq_sht)
print(ind_sht)

keys = Find_keys(ind_ru, ind_sht)
print("\nAll keys:")
print(keys)

# формування списку можливих істинних відкритих текстів
text_variants = []
for key in keys:
    text_variants.append(decode(key[0], key[1], e_text))
    # print(str(key[0]) + ", " + str(key[1]))
    # print(text_variants[-1])


# знаходження коректного відкритого тексту
# методом знахдження індексів відповідності
# і порівняння їх з індексом мови ~ 0.0553
def index_f(text):    # ф-я знаходження індексів відповідності
    index = 0
    for i in range(0, len(chars)):
        N = text.count(chars[i])
        index += N * (N - 1)
    index /= (len(text) * (len(text) - 1))
    return index


# отримання результатів
indexes = []
for text in text_variants:
    indexes.append(index_f(text))
print("\nF_Indexes for texts decrypted with these keys:")
print(indexes)
for i in range(len(indexes)):
    if indexes[i] > 0.05 and indexes[i] < 0.06:
        # print(keys[i])
        # print(text_variants[i])
        str = "KEY => " + str(keys[i]) + "\n" + text_variants[i]
        f = open(".\\05_text.txt", "w")
        f.write(str)
        f.close()
        print("\nCorrect key and decrypted text were written to file!")
        break
