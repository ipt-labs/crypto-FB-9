import math
import re
import numpy as np
file = open("1.txt", "r")

# m=32 - кількість букв алфавіту
alphabet = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ы','ь','э','ю','я',' ']

save = []
save1 = []
save2 = []

print("\n 1. First task\n 2. Second task\n 3. Third task\n")
ans = input()

def func():
    for i in alphabet:
        letter = one.count(i)
        if letter == 0:
            y = 0
        else:
            y = -math.log2(letter/length)
        H = (letter/length) * y
        save.append(H)
        save1.append(i)
        save2.append(round(H,4))
        a = np.column_stack([save1,save2])
        b = sorted(a, key = lambda x: x[1])
        c = "\n".join(map(str,b))
    print (c)
    print("H1: ", sum(save))

def bigram(a):
    for i in alphabet:
        r = [alphabet[a] + i]
        for j in r:
            letter = one.count(j)
            if letter == 0:
                y1 = 0
            else:
                y1 = -math.log2(letter/length)
            H1 = (letter/length) * y1

            save.append(round(H1,1))
            save1.append(H1)
            #save2.append(i)
    print(alphabet[a], "  ".join(map(str, save)))
    save.clear()


if ans == "1":
    data = file.read().replace("ъ","ь")
    one = re.sub(r"[^а-я]+", " ", data.lower())
    #print(one)
    length = len(one)
    func()
elif ans == "2":
    data = file.read()
    one = re.sub(r"[^а-я]+", " ", data.lower().replace(" ", "").replace("ъ","ь"))
    length = len(one)
    #print(one)
    func()
elif ans == "3":
    data = file.read().replace("ъ","ь")
    one = re.sub(r"[^а-я]+", " ", data.lower().replace("ъ","ь"))
    #print(one)
    length = len(one)
    arr = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,24,26,27,28,29,30,31]
    print("   ", "  ".join(alphabet))
    for item in arr:
        bigram(item)
    print("H2: ", sum(save1))

else:
    print("Wrong input")

#print(sorted(save))
#a = np.reshape(np.dstack((save1,save)), [-1,2])
#print(sorted(a, key = lambda  x: x[0]))
#a = np.sort(a, axis=0)
#print (a)
#print(sorted(a, key = lambda  x: x[1]))
