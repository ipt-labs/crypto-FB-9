import unicodedata
import math
import pandas as pd
import collections
import numpy as np
import regex 

harry = open(r'C:\Users\Julia\KPI 5\крипта лабы\гитхаб\crypto-FB-9\cp1\Borodai_fb-96_cp1\garri_potter.txt', encoding='utf-8').read()
harry = harry.lower() # cменили регистр всех символов на нижний
harry = harry.replace("\n"," ") #сменили переход на новую строку на пробел
harry = ' '.join(harry.split()) #разбили строку на список и объединили обратно в строку с разделителем в виде " " 

Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']
Alphabet_with_space = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']

 # наш отформатир текст без пробела
text = ''.join(c for c in harry if unicodedata.category(c).startswith('L'))

# с пробелом
text_withspace = regex.sub(r'[^\w\s]+|[\d]+', r'',harry).strip()


print(text_withspace)

words = []  
words_and_space = []
for i in range(0,len(text)):
    words.append(text[i])
for i in range(0,len(text_withspace)):
    words_and_space.append(text_withspace[i])
    
words_count = dict(collections.Counter(words))
words_and_space_count = dict(collections.Counter(words_and_space))

f_words = {k: words_count[k] / len(words) for k in words_count}
f_words_and_space = {k: words_and_space_count[k] / len(words_and_space) for k in words_and_space_count}
print(f_words_and_space)

for_index_temp= sorted(f_words, key=lambda x : words_count[x],reverse=1)     
for_index_temp2= sorted(f_words_and_space, key=lambda x : words_and_space_count[x],reverse=1) 

tempdict1 = []
tempdict2 = []
for i in range(0,len(for_index_temp)):
    tempdict1.append(f_words[for_index_temp[i]])

for i in range(0,len(for_index_temp2)):
    tempdict2.append(f_words_and_space[for_index_temp2[i]])  
    
dataframe = pd.DataFrame(index = for_index_temp)
dataframe_with_space = pd.DataFrame(index = for_index_temp2)
dataframe['Частота'] = tempdict1
dataframe_with_space['Частота'] = tempdict2
print(dataframe.head(33))
print(dataframe_with_space.head(34))

#біграми
bigramma_step_1 = []
bigramma_step_2 = []
for j in range(0, len(text)-1):
    bigramma_step_1.append(text[j]+text[j+1])
    
for j in range(0, len(text)-2,2):
    bigramma_step_2.append(text[j]+text[j+1])


bigramma_step_1_count = dict(collections.Counter(bigramma_step_1))
bigramma_step_2_count = dict(collections.Counter(bigramma_step_2))

s_bigramma_step_1_count= {k: bigramma_step_1_count[k] / len(bigramma_step_1) for k in bigramma_step_1_count}
s_bigramma_step_2_count= {k: bigramma_step_2_count[k] / len(bigramma_step_2) for k in bigramma_step_2_count}


#біграми с пробілом
bigramma_step_1_space = [] 
bigramma_step_2_space = []
for j in range(0, len(text_withspace)-1):
    bigramma_step_1_space.append(text_withspace[j]+text_withspace[j+1])
    
for j in range(0, len(text_withspace)-2,2):
    bigramma_step_2_space.append(text_withspace[j]+text_withspace[j+1])


bigramma_step_1_space_count = dict(collections.Counter(bigramma_step_1_space))
bigramma_step_2_space_count = dict(collections.Counter(bigramma_step_2_space))

s_bigramma_step_1_count_with_space= {k: bigramma_step_1_space_count[k] / len(bigramma_step_1_space) for k in bigramma_step_1_space_count}
s_bigramma_step_2_count_with_space= {k: bigramma_step_2_space_count[k] / len(bigramma_step_2_space) for k in bigramma_step_2_space_count}


def matrix_for_bigram( Alphabet, freq):
    matrix = pd.DataFrame(index = Alphabet, columns=Alphabet)

    mask = []

    for i in Alphabet:
        for j in Alphabet:
            mask.append(i+j) 
    n = 0

    for i in range(0,len(Alphabet)):
        matrix [Alphabet[i]] = mask[n:len(Alphabet)+n]
        n = len(Alphabet)+n
    matrix = matrix.T

    for key in list(s_bigramma_step_1_count.keys()):
        a,c = np.where(matrix == key)
        matrix.iloc[a,c] = s_bigramma_step_1_count[key]

    for m in mask:
        a,c = np.where(matrix == m)
        matrix.iloc[a,c] = 0
    return matrix



bigramma_step_1_matrix = matrix_for_bigram(Alphabet, s_bigramma_step_1_count)
bigramma_step_2_matrix = matrix_for_bigram(Alphabet, s_bigramma_step_2_count)
bigramma_step_1_matrix_space = matrix_for_bigram(Alphabet_with_space, s_bigramma_step_1_count_with_space)
bigramma_step_2_matrix_space = matrix_for_bigram(Alphabet_with_space, s_bigramma_step_2_count_with_space)

print('частоти появ біграм з кроком 1 без пробілу')
print(bigramma_step_1_matrix)
print('частоти появ біграм з кроком 2 без пробілу')
print(bigramma_step_2_matrix)
print('частоти появ біграм з кроком 1 з пробілом')
print(bigramma_step_1_matrix_space)
print('частоти появ біграм з кроком 2 з пробілом')
print(bigramma_step_2_matrix_space)


#ентропии
def H(frequency,n):
    a = []
    for i in frequency.values():
        a.append(i*math.log(i,2))
    a = sorted(a)
    H = -sum(a)/n
    return H

H1 = H(f_words,1)
H1_with_space = H(f_words_and_space,1)
H2_bigramma = H(s_bigramma_step_1_count,2) 
H2_bigramma_2 = H(s_bigramma_step_2_count,2) 
H2_bigramma_space = H(s_bigramma_step_1_count_with_space,2) 
H2_bigramma_2_space = H(s_bigramma_step_2_count_with_space,2) 
print("ентропія Н1 без пробілу", H1)
print("ентропія Н1 з пробілом", H1_with_space)
print("ентропія Н2 біграм без пробілу", H2_bigramma)
print("ентропія Н2 біграм з кроком 2 без пробілу",H2_bigramma_2)
print("ентропія Н2 біграм з пробілом", H2_bigramma_space)
print("ентропія Н2 біграм з кроком 2 з пробілом", H2_bigramma_2_space )



#надлишковість
H00=H1/33
print('ентропія мови', H00)

def R(H_language):
    H0 = math.log(33,2)
    r = 1-H_language/H0
    print("H0 ",H0)
    print("надлишковість", r)
    return (r)

R(H00)