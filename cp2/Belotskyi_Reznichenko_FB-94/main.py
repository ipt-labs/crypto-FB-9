#!/usr/bin/env python
# coding: utf-8

# In[94]:


import regex 
import re
import unicodedata
import collections
import math
import pandas as pd
import numpy as np

Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']
Alphabet_and_space = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']
Alphabet_num = []
for id, item in enumerate(Alphabet ):
    Alphabet_num.append(id)
Alphabet_dict = dict(zip(Alphabet,Alphabet_num))


def clear(text):
    text = text.lower()
    text = text.replace("\n"," ")
    
    text = ' '.join(text.split())
    text = regex.sub(r'[^\w\s]+|[\d]+', r'',text).strip()
    return text
def merge(text):
    return ''.join(t for t in text if unicodedata.category(t).startswith('L'))

                 
def separator(text, n):
    res = []
    for i in range(0,len(text),n):
        res.append(text[i:i+n])
    return res

def count(text):
    return dict(collections.Counter(text))

def frequrence(text,n):
    letters = separator(text,n)  
    count_ = count(letters)
    f = {k: count_[k] / len(letters) for k in count_}
    return f
                 
def encode(text,key,Alphabet_dict,Alphabet):
    encoded_letters = []
    for var in range(0, len(text)):
         encoded_letters.append((Alphabet_dict[text[var]]+Alphabet_dict [key[var%len(key)]])%len(Alphabet))
    encoded_text = Alphabet[ encoded_letters[0]]
    for i in range(1, len(encoded_letters)):
        encoded_text =  encoded_text+Alphabet[encoded_letters[i]]
    return encoded_text
                 
def decode(encoded_text,key,Alphabet_dict, Alphabet):
    decoded_letters = []
    for i in range(0, len(encoded_text)):
         decoded_letters.append((Alphabet_dict[ encoded_text[i]]-Alphabet_dict[key[i%len(key)]])%len(Alphabet))
    decoded_text = Alphabet[decoded_letters[0]]
    for i in range(1, len( decoded_letters)):
         decoded_text  =  decoded_text +Alphabet[decoded_letters[i]]
    return  decoded_text 
     

def I(count_):
    i = []
    for key in list(count_.keys()):
        i.append(count_[key]*(count_[key]-1))
    return 1/(sum(count_.values())*(sum(count_.values())-1))*sum(i)

def bloc(text, length):
    b = []
    for j in range(0, length):
        bb = ""
        for i in range(0, len(text)-j,length):
                bb = bb+text[i+j]
        if bb!="":       
            b.append(bb)
        else:
            continue
    return b

def I_r(encoded_text,r_list):
    blocs = []
    I_list = []
    for r in r_list:
        blocs.append(bloc(encoded_text,r))
    for i in range(0, len(blocs)): 
        I_value= []
        for b in range(0, len(blocs[i])):
             I_value.append(I(count(blocs[i][b])))
        I_list.append(sum(I_value)/len( I_value))  

    return dict(zip([r for r in r_list],I_list)) 
def save(r,I_,name):
    df = pd.DataFrame()
    df['r'] = r
    df['I'] = I_
    df.to_excel(name+".xlsx")


# In[103]:


def search_key(length, encoded_text,Alphabet_dict,Alphabet):
    b = bloc(encoded_text,length)
    l_number = [] 
    for i in range(0,len(b)):
        l_number.append(count(b[i]))
    fr = []
    for i in range(0,len(b)):
        fr.append({k: l_number[i][k] / len(b[i]) for k in l_number[i]} )  
    lst = []
    for i in range(0,len(fr)):
        lst.append(sorted(fr[i], key=lambda x : l_number[i][x],reverse=1)[0])
    top_rus = ['о','а','е','и','н','т','л','с','р','в','к','у','м','п','д','г','я','з','ь','ы','ч','б','й','ж','ш','х','ю','щ','ц','э','ф','ъ']
    keys = []
    for j in range (0, len(top_rus)):
        key = ""
        for i in range(0,len(lst)):
            key = key+Alphabet[(Alphabet_dict[lst[i]] - Alphabet_dict[top_rus[j]])%(len(Alphabet))]
        keys.append(key) 
    return keys  


# In[106]:


text = open("1.txt", encoding="utf-8").read()
text = clear(text)
text_merged = merge(text)
text_merged


# In[16]:


fr_1 = frequrence(text,1)
fr_2 = frequrence(text_merged ,1)


# In[21]:


print(fr_1,'\n\n',fr_2)


# In[64]:


keys = ["м","ма","луч","зной","топаю","всесложноо","уменятожеса","попадаетонао","ситечкеилипро","чаятравяногохо","спроситчтосказа","помочьтакзайтивд","явключустримиесли","помочьскриптойустя","интерпретированиедоп"]


# In[27]:


text = text.replace("n","")
text_merged = text_merged.replace("n","")


# In[65]:


encoded = []
decoded  = []
for key in keys:
    encoded.append(encode(text_merged,key,Alphabet_dict,Alphabet))
for i in range(0, len(encoded)):
    decoded.append(decode(encoded[i],keys[i],Alphabet_dict,Alphabet))
    
r = []  
length = []
for i in range(0, len(encoded)):
    length.append(len(keys[i]))
    r.append(I(count(separator(encoded[i],1))))
print(r) 
save(length,r,'r')


# In[66]:


r_list = list([r for r in range(2,31)])


# In[85]:


I_ = I_r(encoded[6],r_list)
print(len(keys[6]))


# In[86]:


print(I_)
save(r_list,list(I_.values()),'r_I')


# In[119]:


Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж','з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ','ы', 'ь', 'э', 'ю', 'я']
Alphabet_dict = dict(zip(Alphabet,Alphabet_num))   


# In[107]:


encoded_text = open("2.txt", encoding="utf-8").read().replace('\n',"")
# encoded_text 


# In[108]:


I_encoded_text = I_r(encoded_text,r_list)


# In[109]:


print(I_encoded_text)


# In[136]:


keys = search_key(16,encoded_text,Alphabet_dict,Alphabet)


# In[138]:


print(keys[0])
key = 'делолисоборотней'
print(key)
bad_bloc = [2,3,12,13]


# In[121]:


decoded_text = decode(encoded_text,key,Alphabet_dict,Alphabet)


# In[122]:


print(decoded_text)


# In[130]:




b = []
b = bloc(decoded_text, 16)

for i in bad_bloc:
    c = dict(collections.Counter(b[i]))
    f = {k: c[k] / len(decoded_text) for k in c}
    df = pd.DataFrame.from_dict(f,'index').stack().reset_index(level=0).sort_values(by=0, ascending=0).rename(columns = {'level_0': 'letter', 0: 'freq'}).reset_index(inplace=False).drop(columns= ['index'])  
    top_f = list(df['letter'].head())
    #df.to_csv(str(i)+'.txt')


# In[127]:


df


# In[ ]:




