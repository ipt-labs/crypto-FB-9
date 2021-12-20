import math

letters = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у',
           'ф','х','ц','ч','ш','щ','ы','ь','э','ю','я']

file = open("text1.txt", encoding="utf-8")
fileread = file.read().lower().replace("ъ", "ь").replace("ё", "е").replace('\n'," ")
letters.append(" ")

d = []
def ddd(f):
    for j in range(len(letters)):
        for i in range(len(fileread)):
            if fileread[i] == letters[j]:
                f += 1
                i += 1
            else: i += 1
        d.append(f)
        f = 0
    j += 1
    print('col letters',d)

h = []
def FrequencyLetter():
    for j in range(len(d)):
        i = d[j]/len(fileread)
        h.append(i)
    print('Frequency Letters',h)

val = int(input('enter val(1,2)'))

def Bigram():
    if val == 1:
        for i in range((len(fileread) - 1)):
            bigram.append(fileread[i] + fileread[i + 1])
    else:
        for i in range(0,len(fileread) - 2,2):
            bigram.append(fileread[i] + fileread[i + 1])
        print(bigram)


def dell(bigram):
    for i in range(len(bigram)-1):
        for g in range(i+1 ,len(bigram)):
            if bigram[i] == bigram[g]:
                bigram[g] = 0

def del_0():
    k = -1
    f_0 = []
    for i in range(len(bigram)):
        if bigram[i] == 0:
            f_0.append(i)
    for i in range(len(f_0)):
        k +=1
        f_0[i] = f_0[i]-k
        bigram.pop(f_0[i])
        colbigram.pop(f_0[i])
    print('col bigram',colbigram)
    print('bigrams',bigram)

def Colb(bigram):
    colbigram = []
    k = 0
    for g in range(len(bigram)):
        if bigram[g] in colbigram :
            break
        else:
            for i in range(len(bigram)):
                if bigram[g] == bigram[i]:
                    k += 1
            colbigram .append(k)
            k = 0
    return colbigram

def FrequencyBigram():
    sumbigram = 0
    frequencybigram =[]
    for j in range(len(colbigram)):
        sumbigram = sumbigram + colbigram[j]
    for i in range(len(colbigram)):
        frequencybigram.append(colbigram[i]/sumbigram)
    return frequencybigram

def Entropy(h):
    entropy_letters = 0
    for i in range(len(h)):
        entropy_letters -= h[i]*math.log(h[i],2)
    return entropy_letters

def EntropyBigram(frequencybigram):
    entropy_bigram =0
    for i in range(len(frequencybigram)):
        entropy_bigram -= frequencybigram[i]*math.log(frequencybigram[i],2)
    return entropy_bigram/2

def Sort_letters(h):
    f = []
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(h) - 1):
            if h[i] < h[i + 1]:
                h[i], h[i + 1] = h[i + 1], h[i]
                letters[i], letters[i + 1] = letters[i + 1], letters[i]
                swapped = True
    print(h)
    print(letters)
    f = h
    return h

def Sort_bigr(frequencybigram):
    a =[]
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(frequencybigram) - 1):
            if frequencybigram[i] < frequencybigram[i + 1]:
                frequencybigram[i], frequencybigram[i + 1] = frequencybigram[i + 1], frequencybigram[i]
                bigram[i], bigram[i + 1] = bigram[i + 1], bigram[i]
                swapped = True
    print(frequencybigram)
    print(bigram)
    a = frequencybigram
    return a


myfile = open('output.txt','w')
def WriteFile(frequencybigram):
    i = 0
    for element in range(len(frequencybigram)):
        while i < 1:
            myfile.write(str(frequencybigram[element])),myfile.writelines(','),myfile.writelines('"')
            myfile.write(str(bigram[element])),myfile.writelines('"'), myfile.writelines(',')
            myfile.write('\n')
            i += 1
        i = 0


myfile1 = open('letters.txt','w')
def WriteFile1():
    i = 0
    for element in range(len(h)):
        while i < 1:
            myfile1.write(str(h[element])),myfile1.writelines(','),myfile1.writelines('"')
            myfile1.write(str(letters[element])),myfile1.writelines('"'), myfile1.writelines(',')
            myfile1.write('\n')
            i += 1
        i = 0



def Redundancy_letters():
    return  1 - (Entropy(h)/math.log(len(letters),2))
def Redundancy_bigram():
    return 1 - (EntropyBigram(FrequencyBigram()) / math.log(32,2))


ddd(0)
FrequencyLetter()
bigram = []
Bigram()
colbigram = Colb(list(bigram))
dell(bigram)
del_0()
print('Frequency bigram',FrequencyBigram())
print('entropy letters',Entropy(h))
print('entropy bigram',EntropyBigram(FrequencyBigram()))
print("Redundancy_letters",Redundancy_letters())
print("Redundancy_bigram",Redundancy_bigram())
print('sort')
sorted_bigr = Sort_bigr(FrequencyBigram())
sorted_letters = Sort_letters(h)
WriteFile(sorted_bigr)
WriteFile1()
del fileread
del colbigram
del d
del h
del sorted_letters
d = []
h = []
print("whith out spaces")
myfile.writelines('////////whith out spaces////////'),myfile.writelines('\n')
myfile1.writelines('////////whith out spaces////////'),myfile1.writelines('\n')
letters = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у',
           'ф','х','ц','ч','ш','щ','ы','ь','э','ю','я']
file = open("text1.txt", encoding="utf-8")
fileread = file.read().lower().replace("ъ", "ь").replace("ё", "е").replace(" ", "").replace('\n',"")
letters.pop(-1)
ddd(0)
FrequencyLetter()
bigram = []
Bigram()
colbigram = Colb(list(bigram))
dell(bigram)
del_0()
print('entropy letters',Entropy(h))
print('entropy bigram',EntropyBigram(FrequencyBigram()))
print("Redundancy_letters",Redundancy_letters())
print("Redundancy_bigram",Redundancy_bigram())
print('sort')
sorted_letters = Sort_letters(h)
sorted_bigr = Sort_bigr(FrequencyBigram())
WriteFile(sorted_bigr)
WriteFile1()


# print(len(fileread))