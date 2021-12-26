import collections

from collections import Counter

text1 = open("nospaces.txt",).read()
text2 = open("spaces.txt",).read()
Alphabet1 = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
             'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']
Alphabet2 = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
             'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ']

let1 = Counter(text1)
let2 = Counter(text2)

def FreqLet(n):
    if n == 1:
        freq = [str(i + ": " + str(let1[i] / len(text1))) for i in Alphabet1]
        r = open("nosp1.txt", "w")
        r.write("Монограммы без пробелов\n=====================\n")
        for i in freq:
            r.write(i)
            r.write("\n")
        r.write("==================\nГотово!!!!")
        r.close()
    elif n == 2:
        freq = [str(i + ": " + str(let2[i] / len(text2))) for i in Alphabet2]
        r = open("sp1.txt", "w")
        r.write("Монограммы с пробелами\n=====================\n")
        for i in freq:
            r.write(i)
            r.write("\n")
        r.write("==================\nГотово!!!!")
        r.close()

def Bigram1(n):
    bigram1=[]
    if n == 0:
        for i in range(len(text1)-1):
            bigram1.append(text1[i]+text1[i+1])
        return bigram1
    elif n == 2:
        for i in range(0,len(text1)-1, 2):
            bigram1.append(text1[i]+text1[i+1])
        return bigram1

def Bigram2(n):
    bigram2=[]
    if n == 0:
        for i in range(len(text2)-1):
            bigram2.append(text2[i]+text2[i+1])
        return bigram2
    elif n == 2:
        for i in range(len(0, text2)-1, 2):
            bigram2.append(text2[i]+text2[i+1])
        return bigram2

def FreqBigram(n):
    arrbig = []
    if n == 1:
        arrbig = [str(i + ": " + str((Counter(Bigram1(0))[i] / len(Bigram1(0)))))for i in Counter(Bigram1(0))]
        res1 = open("resnospacecross.txt", "w")
        res1.write("Без пробелов, перехрестные\n=========================\n")
        for i in arrbig:
            res1.write(i)
            res1.write("\n")
        res1.write("================\nПодсчет окончен!")
        res1.close()
    elif n == 2:
        arrbig = [str(i + ": " + str((Counter(Bigram1(2))[i] / len(Bigram1(2)))))for i in Counter(Bigram1(2))]
        res2 = open("resnospacenocross.txt", "w")
        res2.write("Без пробелов, неперехрестные\n=========================\n")
        for i in arrbig:
            res2.write(i)
            res2.write("\n")
        res2.write("================\nПодсчет окончен!")
        res2.close()
    elif n == 3:
        arrbig = [str(i + ": " + str((Counter(Bigram2(0))[i] / len(Bigram2(0)))))for i in Counter(Bigram2(0))]
        res3 = open("resspacecross.txt", "w")
        res3.write("С пробелами, перехрестные\n=========================\n")
        for i in arrbig:
            res3.write(i)
            res3.write("\n")
        res3.write("================\nПодсчет окончен!")
        res3.close()
    elif n == 4:
        arrbig = [str(i + ": " + str((Counter(Bigram2(2))[i] / len(Bigram2(2)))))for i in Counter(Bigram2(2))]
        res4 = open("resspacenocross.txt", "w")
        res4.write("С пробелами, неперехрестные\n=========================\n")
        for i in arrbig:
            res4.write(i)
            res4.write("\n")
        res4.write("================\nПодсчет окончен!")
        res4.close()

if __name__ == "__main__":
    print("Вывод данных")
    print("Монограммы без пробелов")
    print(FreqLet(1))
    print("Готово!")
    print("Монограммы с пробелом")
    print(FreqLet(2))
    print("Готово!")
    print("Биграммы 1")
    print(FreqBigram(1))
    print("Готово!")
    print("Биграммы 2")
    print(FreqBigram(2))
    print("Готово!")
    print("Биграммы 3")
    print(FreqBigram(3))
    print("Готово!")
    print("Биграммы 4")
    print(FreqBigram(4))
    print("Готово!")