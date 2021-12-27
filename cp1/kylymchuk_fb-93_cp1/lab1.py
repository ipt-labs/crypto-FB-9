from collections  import Counter 
import math

#name=input("Введите название файла:")
name="text.txt"
with open(name) as file:
    f=file.read()

#letters
entr=0
for i in Counter(f):
    print(i+":",Counter(f)[i]/len(f))
    p = Counter(f)[i] / len(f)
    entr -= p*math.log(p,2)
print("Энтропия: ",entr)
print("Избыточность:", 1-(entr/len(Counter(f))))

#bigrams
bigram1=[]
bigram2=[]
f2=f
for i in range(0, len(f)-1):
    bigram1.append(f[i]+f[i+1])
if (len(f)%2==1):
    f2+="о"
for i in range(0, len(f2)-1, 2):
    bigram2.append(f2[i]+f2[i+1])
entr1=0
entr2=0
for i in Counter(bigram1):
    print(i+":", Counter(bigram1)[i]/len(bigram1))
    p = Counter(bigram1)[i]/len(bigram1)
    entr1 -=p*math.log(p,2)
print("Энтропия биграм с пересечение:", entr1/2)
print("Избыточность:", 1-(entr1/len(Counter(f))))
for i in Counter(bigram2):
    print(i+":", Counter(bigram2)[i]/len(bigram2))
    p = Counter(bigram2)[i]/len(bigram2)
    entr2 -=p*math.log(p,2)
print("Энтропия биграм без пересечения:", entr2/2)
print("Избыточность:", 1-(entr2/len(Counter(f2))))