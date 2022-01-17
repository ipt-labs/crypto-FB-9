from collections import Counter 
import math 

a = True
#if false then without spaces

alphabet = [chr(code) for code in range(ord("а"), ord("а") + 32)]
alphabet.remove ("ъ")


if a:
  with open("Spaces.txt", encoding="utf-8") as f:
    text = f.read()
  alphabet.append(" ")
else:
   with open("WithoutSpaces.txt", encoding="utf-8") as f:
    text = f.read()

length = len(text)

if (length % 2 == 1) :
  text += 'б'
  length += 1

def ArrOfBg(step):
  i = 0
  arr = []
  while i < (length-1):
    arr.append(text[i] + text[i+1])
    i += step
  return arr

bigramArr1 = ArrOfBg(1)
bigramArr2 = ArrOfBg(2)

letters = Counter(text)
bg1 = Counter(bigramArr1)
bg2 = Counter(bigramArr2)

def Entropiacounter(counter, len, n_gram):
    Entropia = 0
    for i in counter:
        p = counter[i] / (len)
        Entropia -= p*math.log(p,2)
    return Entropia / n_gram



print('Letter Entropia: ',Entropiacounter(letters, sum(letters.values()), 1))
print('Bigram 1-stepped: ', Entropiacounter(bg1, sum(bg1.values()),2))
print('Bigram 2-stepped: ', Entropiacounter(bg2, sum(bg2.values()),2))


def LetterFreqency():
  for i in alphabet:
     print(i," => " ,(letters[i]/length))


LetterFreqency()

file2 = open('CrossBigram.txt', 'w')
def FreqOfCrossBg(bigrams, len):
  for i in alphabet:
    for j in alphabet:
      bg = (i + j)
      p = bigrams[bg] / (len)
      file2.write(bg + "->" + (str('%.6f' % p) + " "))
    file2.write("\n")

FreqOfCrossBg(bg1, sum(bg1.values()))
file2.close()


file3 = open('NotCrossBigram.txt', 'w')
def FreqOfNotCrossBg(bigrams, len):
  for i in alphabet:
    for j in alphabet:
      bg = (i + j)
      p = bigrams[bg] / (len)
      file3.write(bg + "->" + (str('%.6f' % p) + " "))
    file3.write("\n")


FreqOfNotCrossBg(bg2, sum(bg2.values()))
file3.close()

def BgFreqConsole(bigrams):
  for bg in bigrams.most_common():
    print(bg[0] + " : " + str(('%.6f' % (bg[1]/sum(bigrams.values())))))

BgFreqConsole(bg2)
