import unicodedata
import collections
import codecs

harry = open(r'C:\Users\Julia\KPI 5\крипта лабы\гитхаб\crypto-FB-9\cp2\Borodai_fb-96_cp2\вт.txt', encoding='utf-8').read()
harry = harry.lower() # cменили регистр всех символов на нижний
harry = harry.replace("\n","") #сменили переход на новую строку на ybxtuj
harry = ' '.join(harry.split()) #разбили строку на список и объединили обратно в строку с разделителем в виде " " 

Alphabet_n = []
Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
for id, item in enumerate(Alphabet):
    Alphabet_n.append(id)
Alphabet_dict = dict(zip(Alphabet, Alphabet_n))

text = ''.join(c for c in harry if unicodedata.category(c).startswith('L'))
print(text)

k2="ра"
k3="кря"
k4="бубс"
k5="кошки"
k16="хочукушатьиспать"
def Encrypt(text,key):
    
    key*=len(text)//len(key)+1
    c=""
    for i,j in enumerate(text): 
        gg=(ord(j)+ord(key[i])) 
        c+=chr(gg%33+ord("а"))
        encrypt=str(c)
    return encrypt

encrypt2=Encrypt(text,k2)
encrypt3=Encrypt(text,k3)
encrypt4=Encrypt(text,k4)
encrypt5=Encrypt(text,k5)
encrypt16=Encrypt(text,k16)
print("Encrypted message:\n", Encrypt(text,k2))
print("Encrypted message:\n", Encrypt(text,k3))
print("Encrypted message:\n", Encrypt(text,k4))
print("Encrypted message:\n", Encrypt(text,k5))
print("Encrypted message:\n", Encrypt(text,k16))

# text
def periodicity(cipher_t):
    n = len(cipher_t)
        
    D = []
    for j in range(1, 30):
        Di = 0
        for i in range(n):
            Di += int(cipher_t[i] == cipher_t[(i + j) %n])
        D.append([Di, j])
        print (j, Di)
        
    print('Період шифру ', [i for j, i in sorted(D, key=lambda x:x[0])[-1:]
])

def block(data, r):
    bl = []
    for a in range(0, r):
        temp = ""
        for s in range(0, len(data) - a, r):
            temp = temp + data[s + a]
        if temp != "":
            bl.append(temp)
        else:
            continue
    return bl
    
    
with codecs.open("вар2.txt", "r+", "utf-8") as file:
    var2sht = file.readline()
    var2sht = var2sht.replace('\n', "")
    var2sht = var2sht.replace('\r', "")

print("індекси відповідності відкритий текст")
periodicity(text)
print("індекси відповідності шифр текст с ключем довжиною 2")
periodicity(encrypt2)
print("індекси відповідності шифр текст с ключем довжиною 3")
periodicity(encrypt3)
print("індекси відповідності шифр текст с ключем довжиною 4")
periodicity(encrypt4)
print("індекси відповідності шифр текст с ключем довжиною 5")
periodicity(encrypt5)
print("індекси відповідності шифр текст с ключем довжиною 16")
periodicity(encrypt16)
print("індекси відповідності шифр текст вар 2")
periodicity(var2sht)

print("індекс відповідності шифр текст варіанту №2 = 14")


def search_k(r, cipher, Alphabet_dict, Alphabet):
    blocks = block(cipher, r)
    l_count = []
    for i in range(0, len(blocks)):
        l_count.append(dict(collections.Counter(blocks[i])))

    freq = []
    for i in range(0, len(blocks)):
        temp = []
        temp = {k: l_count[i][k] / len(blocks[i]) for k in l_count[i]}
        freq.append(temp)
    top = []
    for i in range(0, len(freq)):
        temp = []
        temp = sorted(freq[i], key=lambda x: l_count[i][x], reverse=1)
        top.append(temp[0])

    help = ['о', 'е', 'а', 'и', 'н', 'т', 'с', 'р', 'в', 'л', 'к', 'м', 'д', 'п', 'у', 'я', 'ы', 'ь', 'г', 'з', 'б', 'ч', 'й', 'х', 'ж', 'ш', 'ю', 'ц', 'щ', 'э', 'ф', 'ъ']

    keys = []
    for j in range(0, len(help)):
        key = ""
        for i in range(0, len(top)):
            key = key + Alphabet[(Alphabet_dict[top[i]] - Alphabet_dict[help[j]]) % (len(Alphabet))]
        keys.append(key)
    return keys

def decode(cipher, key, Alphabet_dict, Alphabet):
    temp = []
    for i in range(0, len(cipher)):
        temp.append((Alphabet_dict[cipher[i]] - Alphabet_dict[key[i % len(key)]]) % len(Alphabet))
    vt = Alphabet[temp[0]]
    for i in range(1, len(cipher)):
        vt = vt + Alphabet[temp[i]]
    return vt


key=search_k(14, var2sht, Alphabet_dict, Alphabet)
print(key)
key[0]='последнийдозор'
key[0] = key[0].replace('\n', "")
key[0] = key[0].replace('\r', "")
vt=decode(var2sht, key[0], Alphabet_dict, Alphabet)
print(vt)
