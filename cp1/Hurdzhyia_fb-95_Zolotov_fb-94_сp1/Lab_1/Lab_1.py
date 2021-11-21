from array import *
from math import*
 
 
file_source = "..\\file1.txt"
file_noSpace = "..\\file2_noSpace.txt"
file_Space = "..\\file3_Space.txt"
file_probability_noSpace = "..\\file4_probability_noSpace.txt"
file_probability_Space = "..\\file5_probability_Space.txt"
file_bigramms_Space_1 = "..\\file6_bigramms_Space_1.txt"
file_bigramms_Space_2 = "..\\file7_bigramms_Space_2.txt"
file_bigramms_noSpace_1 = "..\\file8_bigramms_noSpace_1.txt"
file_bigramms_noSpace_2 = "..\\file9_bigramms_noSpace_2.txt"
 
 
Alphabet1=['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ы','ь','э','ю','я']
Alphabet2=['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ы','ь','э','ю','я', ' ']
 
 
file1 = open(file_source, "r")
cont_source = file1.read()
 
###################################################################################
###############################   Открываем файл 2     ############################
 
file2 = open(file_noSpace, "w")
file2.write(cont_source.lower())  # с помощью функции lower() мы меняем пpописные буквы на строчные
file2.close()
 
 
###########  тут стираются буквы, которых нет в алфавите ##################
file2 = open(file_noSpace, "r")
cont_noSpace = file2.read()
file2.close()
 
file2 = open(file_noSpace, "w")

########  убираем буквы, которых нет в алфавите #########
def alph(s):
    arr = []
    for char in string:
        if char not in Alphabet1:
           char = ''
        else:
            arr.append(char)
    return ''.join(arr)

string = cont_noSpace.replace('ё', 'е')
string = string.replace('ъ', 'ь')
file2.write(alph(string))

file2.close()
 
 
#####################    Частота букв в файле 4     ###############################
 
file2 = open(file_noSpace, "r")
cont_noSpace = file2.read()
 
arr = []
thisset = set()
for char in cont_noSpace:
    thisset.add(char) 
for c in thisset:
    arr.append(c)
 
arr.sort()

for i in range(0,len(arr)):
    probability = (cont_noSpace.count(arr[i]))/len(cont_noSpace)
    strochka1 = arr[i] + "\t " +str(cont_noSpace.count(arr[i])) + "\t " +  str(probability)
    file4 = open(file_probability_noSpace, "a")
    file4.write(strochka1 + '\n')
    file4.close()
file2.close()
 
 
 
####################################################################################
############################   Открываем файл 3     ################################
 
file3 = open(file_Space, "w")
file3.write(cont_source.lower())
file3.close()
 
###########  тут стираются буквы, которых нет в алфавите ##################
file3 = open(file_Space, "r")
cont_Space = file3.read()
file3.close()
 
file3 = open(file_Space, "w")
 
########  убираем буквы, которых нет в алфавите
def alph(s):
    arr = []
    for char in string:
        if char not in Alphabet2:
           char = ''
        else:
            arr.append(char)
    return ''.join(arr)
####### тут стираются ненужные пробелы ######
def space(s):
    s = s.split()
    return ' '.join(s)

string = cont_Space.replace('ё', 'е')
string = string.replace('ъ', 'ь')
string = string.replace("\n", ' ')
string = alph(string)
file3.write(space(string))
file3.close()
 
 
#####################   Частота букв в файле 3     ###############################
 
file3 = open(file_Space, "r")
cont_Space = file3.read()
 
arr = []
thisset = set()
for char in cont_Space:
    thisset.add(char) 
for c in thisset:
    arr.append(c)
 
arr.sort()
for i in range(0,len(arr)):
    probability = (cont_Space.count(arr[i]))/len(cont_Space)
    strochka2 = arr[i] + "\t " +str(cont_Space.count(arr[i])) + "\t " +  str(probability)
    file5 = open(file_probability_Space, "a")
    file5.write(strochka2 + '\n')
    file5.close()
file3.close()
 
#######################################################################################
###############################     Биграммы    #######################################
 
 
#############################  Файл 2 (без пробелов) с шагом 1      ###################
 
file2 = open(file_noSpace, "r")
cont_noSpace = file2.read()
 
arr1 = []
for i in range(0,len(cont_noSpace)-1):
    char = cont_noSpace[i] + cont_noSpace[i+1]
    arr1.append(char)

arr = []
thisset = set()
for char in arr1:
    thisset.add(char) 
for c in thisset:
    arr.append(c)
arr.sort()

sumOfCountOfBigrams = 0
for i in range(0, len(arr)):    # тут мы считаем сумму количества каждой биграммы
    sumOfCountOfBigrams+=cont_noSpace.count(arr[i])

for i in range(0, len(arr)):
    
    probability = (cont_noSpace.count(arr[i]))/sumOfCountOfBigrams
    strochka3 = arr[i] + "\t " +str(cont_noSpace.count(arr[i])) + "\t " +  str(probability)
    file6 = open(file_bigramms_noSpace_1, "a")
    file6.write(strochka3 + '\n')
    file6.close()
file2.close()
 
 
 
 
##########################   Файл 2 (без пробелов) с шагом 2      ####################
 
file2 = open(file_noSpace, "r")
cont_noSpace = file2.read()
 
arr1 = []
 
i = 0
while i < len(cont_noSpace)-1:
    char = cont_noSpace[i] + cont_noSpace[i+1] 
    arr1.append(char)
    i+=2

arr = []
thisset = set()
for char in arr1:
    thisset.add(char) 
for c in thisset:
    arr.append(c)

arr.sort()

sumOfCountOfBigrams = 0
for i in range(0, len(arr)):    # тут мы считаем сумму количества каждой биграммы
    sumOfCountOfBigrams+=cont_noSpace.count(arr[i])

for i in range(0, len(arr)):
    probability = (cont_noSpace.count(arr[i]))/sumOfCountOfBigrams  # вероятность
    strochka3 = arr[i] + "\t " +str(cont_noSpace.count(arr[i])) + "\t " +  str(probability)
    file7 = open(file_bigramms_noSpace_2, "a")
    file7.write(strochka3 + '\n')
    file7.close()
file2.close()
 
 
 
 
 
##########################   Файл 3 (с пробелами) с шагом 1      #####################
 
file3 = open(file_Space, "r")
cont_Space = file3.read()
 
arr1 = []
for i in range(0,len(cont_Space)-1):
    char = cont_Space[i] + cont_Space[i+1]
    arr1.append(char)

arr = []
thisset = set()
for char in arr1:
    thisset.add(char) 
for c in thisset:
    arr.append(c)
 
arr.sort()


sumOfCountOfBigrams = 0
for i in range(0, len(arr)):    # тут мы считаем сумму количества каждой биграммы
    sumOfCountOfBigrams+=cont_Space.count(arr[i])

for i in range(0, len(arr)):
    
    probability = (cont_Space.count(arr[i]))/sumOfCountOfBigrams
    strochka3 = arr[i] + "\t " +str(cont_Space.count(arr[i])) + "\t " +  str(probability)
    file8 = open(file_bigramms_Space_1, "a")
    file8.write(strochka3 + '\n')
    file8.close()
file3.close()
 
 
 
 
########################   Файл 3 (с пробелами) с шагом 2      #######################
 
file3 = open(file_Space, "r")
cont_Space = file3.read()
 
arr1 = []
 
i = 0
while i < len(cont_Space)-1:
    char = cont_Space[i] + cont_Space[i+1]
    arr1.append(char)
    i+=2
 
arr = []
thisset = set()
for char in arr1:
    thisset.add(char)
for c in thisset:
    arr.append(c)
 
arr.sort()
sumOfCountOfBigrams = 0
for i in range(0, len(arr)):    # тут мы считаем сумму количества каждой биграммы
    sumOfCountOfBigrams += cont_Space.count(arr[i])

for i in range(0, len(arr)):
    probability = (cont_Space.count(arr[i]))/sumOfCountOfBigrams  # вероятность
    strochka3 = arr[i] + "\t " +str(cont_Space.count(arr[i])) + "\t " +  str(probability)
    file9 = open(file_bigramms_Space_2, "a")
    file9.write(strochka3 + '\n')
    file9.close()
file3.close()