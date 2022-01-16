#!/usr/bin/env python
# coding: utf-8



# In[91]:


import re
import collections
from collections import Counter
from math import log2
import pandas as pd
f = open('mas.txt', encoding='UTF-8')
file_txt  = f.read()
file_txt = re.sub('ъ', 'ь', file_txt)
file_txt = re.sub('ё', 'е', file_txt)
file_txt_no_spaces = re.sub(' ', '', file_txt)
file_txt_no_spaces = re.sub('\n', '', file_txt_no_spaces)
file_txt_no_spaces = re.sub('Т', '', file_txt_no_spaces)

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


# In[92]:


abc = ['а', 'б', 'в', 'г', 'д', 'е', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']
abc_index = dict(zip(abc,[id for id, item in enumerate(abc)]))  


# In[93]:


def encode(cryptotext,key,abc_index, abc):
    encoded_text = abc[(abc_index[cryptotext[0]]+abc_index[key[0%len(key)]])%len(abc)][0]
    for i in range(1, len(cryptotext)):
        encoded_text = encoded_text+abc[(abc_index[cryptotext[i]]+abc_index[key[i%len(key)]])%len(abc)]
    return encoded_text


def decode(encoded_text,key,abc_index, abc):
    decoded_text = abc[(abc_index[encoded_text[0]]-abc_index[key[0%len(key)]])%len(abc)][0]
    for i in range(1, len(encoded_text)):
        decoded_text = decoded_text+abc[(abc_index[encoded_text[i]]-abc_index[key[i%len(key)]])%len(abc)]
    return decoded_text


# In[129]:


def div_text_on_ngram(text, number_of_letters):
    div = []
    for i in range(0,len(text),number_of_letters):
        div.append(text[i:i+number_of_letters])
    return div

def count_of_ngram(div):
    return dict(collections.Counter(div))
   

def Index_vidpovidnosty(div_on_ngram_text_count_dict):
    val = []
    for key in list(div_on_ngram_text_count_dict.keys()):
        val.append(div_on_ngram_text_count_dict[key]*(div_on_ngram_text_count_dict[key]-1))
    return 1/(sum(div_on_ngram_text_count_dict.values())*(sum(div_on_ngram_text_count_dict.values())-1))*sum(val)


# In[130]:


keys = ["ч","ле","ммм","марс","холод","янежмурика","авангардист","беспризорник","верхоглядство","высокотоварный","жизнедеятельный","коммуникабельный","нетрудноспособный","последовательность","коричневорубашечник","сельскохозяйственный"]


# In[131]:


test = 'Окончив газету, вторую чашку кофе и калач с маслом, он встал, стряхнул крошки калача с жилета и, расправив широкую грудь, радостно улыбнулся, не оттого, что у него на душе было чтото особенно приятное, радостную улыбку вызвало хорошее пищеварение.'


# In[132]:


test = test.lower().replace(' ','').replace(',','').replace('.','')


# In[133]:


encoded_text = encode(test,keys[2],abc_index, abc)


# In[134]:


decoded_text = decode(encoded_text ,keys[2],abc_index, abc)


# In[135]:


test == decoded_text 


# In[136]:


r = []  
for key in keys:
    r.append(Index_vidpovidnosty(count_of_ngram(div_text_on_ngram(encode(test,key,abc_index,abc),1))))
print(r) 


# In[137]:


import pandas as pd

my_table = pd.DataFrame()
my_table ['r'] = [len(key) for key in keys]
my_table ['Index_vidpovidnosty'] = r
my_table.to_excel("1.xlsx")


# In[138]:




def div_text_on_block(text, lenght):
    rez = []
    for j in range(0, lenght):
        col = ""
        for i in range(0, len(text)-j,lenght):
                col = col+text[i+j]
        if col!="":       
            rez.append(col)
        else:
            continue
    return rez    
    

col = []
for r in range(2,31):
    col.append(div_text_on_block(encoded_text,r))
    
    
  
    
I = []
for i in range(0, len(col)): 
    j_list = []
    for c in range(0, len(col[i])):
        j_list.append(Index_vidpovidnosty(count_of_ngram(col[i][c])))
    I.append(sum(j_list)/len(j_list))

indexes = dict(zip([r for r in range(2,31)],I))    
print(indexes)


# In[139]:


vr = open('lab2.txt', encoding= 'UTF-8')
var_5 = vr.read()
var_5 = var_5.replace('\n',"")
var_5  = var_5.replace("С","")


# In[140]:


var_5


# In[141]:


col = []
for r in range(2,31):
    col.append(div_text_on_block(var_5,r))
    
    
  
    
I = []
for i in range(0, len(col)): 
    j_list = []
    for c in range(0, len(col[i])):
        j_list.append(Index_vidpovidnosty(count_of_ngram(col[i][c])))
    I.append(sum(j_list)/len(j_list))

indexes = dict(zip([r for r in range(2,31)],I))    
print(indexes)

lenght = 16


# In[142]:


def answer(r,encoded_text,abc_index,abc):
    col = div_text_on_block(encoded_text,r)
    lst = [] 
    for i in range(0,len(col)):
        lst.append(count_of_ngram((col[i])))
 

    freq = []
    for i in range(0,len(col)):
        freq.append({k: lst[i][k] / len(col[i]) for k in lst[i]})  
    best = []
    for i in range(0,len(freq)):
        best.append(sorted(freq[i], key=lambda x : lst[i][x],reverse=1)[0])

    letters = ['о','а','е','и','н','т','л','с','р','в','к','у','м','п','д','г','я','з','ь','ы','ч','б','й','ж','ш','х','ю','щ','ц','э','ф','ъ']

    k = []
    for j in range (0, len(letters)):
        ans = ""
        for i in range(0,len(best)):
            ans = ans+abc[(abc_index[best[i]] - abc_index[letters[j]])%(len(abc))]
        k.append(ans) 
    return k


# In[143]:



answer(16,var_5,abc_index,abc)


# In[144]:


key = 'делолисоборотней'


# In[145]:


text = decode(var_5,key,abc_index,abc)


# In[146]:


print(text)


# In[ ]:





# In[ ]:




