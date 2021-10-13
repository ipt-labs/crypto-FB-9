import math
from collections import Counter


alph = ["а","б","в","г","д","е","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ", "ы",
        "ь","э","ю","я", " "]

#text editing
text_spaces = []
text_nospaces = []

with open('text.txt', 'r', encoding = 'utf-8') as f:
    file = f.read()
    file = file.lower()
    length = len(file)

    space = False
    for i in range(length):
        if file[i] == "ё":
            file[i] == "e"
        if file[i] == "ъ":
             file[i] == "ь"
        if file[i] in alph:
            if file[i] == " ":
                if space == True:
                    continue
                else:
                    text_spaces.append(" ")
                    space = True
            else:
                text_spaces.append(file[i])
                text_nospaces.append(file[i])
                space = False
        else:
            if space == False:
                text_spaces.append(" ")
                space = True


def redundancy(n, m):
    return 1 - (n / math.log(m, 2))

def letters_entropy(text):
    length = len(text)
    freq = Counter(text)
    for i in freq:
        freq[i] /= length
    result = -1 * sum(freq[k] * math.log(freq[k], 2) for k in freq)

    freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)
    for key, value in freq:
        print(key, ':', value)

    return result, redundancy(result, len(freq))


def bigrams_entropy(text, intersection):
    length = len(text)
    if length % 2 == 1 and intersection == 0:
        length -= 1

    bigrams = []
    for i in range(0, length-1, 2-intersection):
        bigrams.append(text[i]+text[i+1])
    count = len(bigrams)

    freq = Counter(bigrams)
    for i in freq:
        freq[i] /= count
    result = sum(freq[k] * math.log(freq[k], 2) for k in freq) / (-2)

    freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)
    for key, value in freq:
        print(key, ':', value)

    return result, redundancy(result, len(''.join(set(text))))


print("H1 text with spaces", letters_entropy(text_spaces))
print("H1 text without spaces", letters_entropy(text_nospaces))
print("H2 text with spaces without intersections", bigrams_entropy(text_spaces, 0))
print("H2 text with spaces with intersections", bigrams_entropy(text_spaces, 1))
print("H2 text without spaces without intersections", bigrams_entropy(text_nospaces, 0))
print("H2 text without spaces without intersections", bigrams_entropy(text_nospaces, 1))

