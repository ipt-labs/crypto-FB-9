import math
import csv

with open("raw_text.txt", "r", encoding="utf-8") as reader:
    lis = reader.read()
    lis2 = lis.lower().replace(",","").replace("!","").replace("?","").replace(".","").replace(":","").replace(";","").replace("\n","").replace("ъ","ь").replace("ё","е").replace("-","").replace("—","").replace("\xa0","").replace("[","").replace("]","").replace("(","").replace(")","").replace("…","").replace("=","").replace("*","").replace("/","")
    lis2_nospaces = lis2.replace(" ","")


    length = len(lis)
    length1 = len(lis2)
    length2 = len(lis2_nospaces)

    #частота биграм учитывая пробелы (step 1)
    def bigram_freq_spaces_step1(): 
        bigram_freq1 = {}
        all_bigrams1 = 0
        h2_sp = 0
        res = {}
        for i in range(length1-1):
            bigram = (lis2[i], lis2[i+1])
            if bigram not in bigram_freq1:
                bigram_freq1[bigram] = 0
            bigram_freq1[bigram] += 1
            all_bigrams1 += 1    
        for key in bigram_freq1:
            res[key] = bigram_freq1[key]/all_bigrams1
        for value in bigram_freq1.values():
            op = -(value/all_bigrams1*math.log2(value/all_bigrams1))
            h2_sp += op
        a3 = 1 - (h2_sp/2)/math.log2(32)
        with open('H_and_R.txt', 'a') as f:
            f.write('-' * 9 + 'Bigrams' + '-' * 9 + '\n' + '-' * 25 + '\n' + 'With spaces (step1): ' + "\n" + "   H2=" + str(h2_sp/2) + "\n" + "   R=" + str(a3) + "\n" + "--------------" + "\n")
        with open('Bigrams_spaces_step1.csv', 'w', newline="") as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerow(["Біграма", "Частота"])
            list_res = list(res.items())
            list_res.sort(key=lambda i: i[1], reverse=True)
            for i in list_res:
                writer.writerow(i) 
            #for key, value in res.items():
                #writer.writerow([key, value])  

    #частота биграм учитывая пробелы (step 2)
    def bigram_freq_spaces_step2(): 
        bigram_freq1 = {}
        all_bigrams1 = 0
        h2_sp = 0
        res = {}
        for i in range(length1-1):
            if i % 2 == 0:
                bigram = (lis2[i], lis2[i+1])
                if bigram not in bigram_freq1:
                    bigram_freq1[bigram] = 0
                bigram_freq1[bigram] += 1
                all_bigrams1 += 1    
        for key in bigram_freq1:
            res[key] = bigram_freq1[key]/all_bigrams1
        for value in bigram_freq1.values():
            op = -(value/all_bigrams1*math.log2(value/all_bigrams1))
            h2_sp += op
        a3 = 1 - (h2_sp/2)/math.log2(32)
        with open('H_and_R.txt', 'a') as f:
            f.write('With spaces (step2): ' + "\n" + "   H2=" + str(h2_sp/2) + "\n" + "   R=" + str(a3) + "\n" + "--------------" + "\n")                          
        with open('Bigrams_spaces_step2.csv', 'w', newline="") as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerow(["Біграма", "Частота"])
            list_res = list(res.items())
            list_res.sort(key=lambda i: i[1], reverse=True)
            for i in list_res:
                writer.writerow(i) 


    #частота биграм БЕЗ пробелов (step 1)
    def bigram_freq_nospaces_step1(): 
        bigram_freq2 = {}
        all_bigrams2 = 0
        h2_no_sp = 0 
        res = {}
        for i in range(length2-1):
            bigram = (lis2_nospaces[i], lis2_nospaces[i+1])
            if bigram not in bigram_freq2:
                bigram_freq2[bigram] = 0
            bigram_freq2[bigram] += 1
            all_bigrams2 += 1
        for key in bigram_freq2:
            res[key] = bigram_freq2[key]/all_bigrams2
        for value in bigram_freq2.values():
            op = -(value/all_bigrams2*math.log2(value/all_bigrams2))
            h2_no_sp += op
        a4 = 1 - (h2_no_sp/2)/math.log2(31)
        with open('H_and_R.txt', 'a') as f:
            f.write('No spaces (step 1): ' + "\n" + "   H2=" + str(h2_no_sp/2) + "\n" + "   R=" + str(a4) + "\n" + "--------------" + "\n")
        with open('Bigrams_no_spaces_step1.csv', 'w', newline="") as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerow(["Біграма", "Частота"])
            list_res = list(res.items())
            list_res.sort(key=lambda i: i[1], reverse=True)
            for i in list_res:
                writer.writerow(i) 


    #частота биграм БЕЗ пробелов (step 2)
    def bigram_freq_nospaces_step2(): 
        bigram_freq2 = {}
        all_bigrams2 = 0
        h2_no_sp = 0 
        res = {}
        for i in range(length2-1):
            if i % 2 == 0:
                bigram = (lis2_nospaces[i], lis2_nospaces[i+1])
                if bigram not in bigram_freq2:
                    bigram_freq2[bigram] = 0
                bigram_freq2[bigram] += 1
                all_bigrams2 += 1
        for key in bigram_freq2:
            res[key] = bigram_freq2[key]/all_bigrams2
        for value in bigram_freq2.values():
            op = -(value/all_bigrams2*math.log2(value/all_bigrams2))
            h2_no_sp += op
        a4 = 1 - (h2_no_sp/2)/math.log2(31)
        with open('H_and_R.txt', 'a') as f:
            f.write('No spaces (step 2): ' + "\n" + "   H2=" + str(h2_no_sp/2) + "\n" + "   R=" + str(a4) + "\n" + "--------------" + "\n")
        with open('Bigrams_no_spaces_step2.csv', 'w', newline="") as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerow(["Біграма", "Частота"])
            list_res = list(res.items())
            list_res.sort(key=lambda i: i[1], reverse=True)
            for i in list_res:
                writer.writerow(i) 


    #частота букв включая пробелы
    def char_freq_spaces():
        ch_fr1 = {}
        h1_sp = 0
        res = {}
        for i in range(length1-1):
            ch = (lis2[i])
            if ch not in ch_fr1:
                ch_fr1[ch] = 0
            ch_fr1[ch] += 1
        for key in ch_fr1:
            res[key] = ch_fr1[key]/length1
        for value in ch_fr1.values():
            op = -(value/length1*math.log2(value/length1))
            h1_sp += op
        a1 = 1 - h1_sp/math.log2(32)
        with open('H_and_R.txt', 'w') as f:
            f.write('-' * 8 + 'Monograms' + '-' * 8 + '\n' + '-' * 25 + '\n' + 'With spaces: ' + "\n" + "   H1=" + str(h1_sp) + "\n" + "   R=" + str(a1) + "\n" + "--------------" + "\n")
        with open('Char_spaces.csv', 'w', newline="") as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerow(["Літера", "Частота"])
            list_res = list(res.items())
            list_res.sort(key=lambda i: i[1], reverse=True)
            for i in list_res:
                writer.writerow(i) 

    #частота букв БЕЗ пробелов
    def char_freq_nospaces():
        ch_fr2 = {}
        h1_no_sp = 0
        res = {}
        for i in range(length2-1):
            ch = (lis2_nospaces[i])
            if ch not in ch_fr2:
                ch_fr2[ch] = 0
            ch_fr2[ch] += 1
        for key in ch_fr2: 
            res[key] = ch_fr2[key]/length2
        for value in ch_fr2.values():
            op = -(value/length2*math.log2(value/length2))
            h1_no_sp += op
        a2 = 1 - h1_no_sp/math.log2(31)
        with open('H_and_R.txt', 'a') as f:
            f.write('No spaces: ' + "\n" + "   H1=" + str(h1_no_sp) + "\n" + "   R=" + str(a2) + "\n" + "--------------" + "\n" * 2)
        with open('Char_no_spaces.csv', 'w', newline="") as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerow(["Літера", "Частота"])
            list_res = list(res.items())
            list_res.sort(key=lambda i: i[1], reverse=True)
            for i in list_res:
                writer.writerow(i) 
           
    char_freq_spaces()
    char_freq_nospaces()
    bigram_freq_spaces_step1()
    bigram_freq_spaces_step2()
    bigram_freq_nospaces_step1()
    bigram_freq_nospaces_step2()



