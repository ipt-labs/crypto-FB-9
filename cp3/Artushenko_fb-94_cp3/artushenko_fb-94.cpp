#include <iostream>
#include <fstream>
#include <Windows.h>
#include <algorithm>
#include <string>
#include <stdio.h>
#include <string.h>
#include <cstring>

using namespace std;

void print_menu() {
    system("cls"); 
    cout << "Що Ви хочете зробити?" << endl;
    cout << "1. Обернений елемент за допомогою алгоритма Евкліда " << endl;
    cout << "2. Вирішення лінійних рівнянь" << endl;
    cout << "3. Знаходження біграм в зашифрованому тексті" << endl;
    cout << "4. Пошук пари ключів" << endl;
    cout << "5. Пошук правильного ключа " << endl;
    cout << "6. Дешифровка Афінного шифру " << endl;
    cout << "7. Вихід" << endl;
    cout << ">";
}
int get_variant(int count) {
    int variant;
    string s; 
    getline(cin, s);
    while (sscanf_s(s.c_str(), "%d", &variant) != 1 || variant < 1 || variant > count) {
        cout << ">"; 
        getline(cin, s); 
    }

    return variant;
}
int gcd(int a, int n) {
    if (a == 0) {
        return n;
    }
    int d = gcd(n % a, a);
    return d;
}
int E_A(int a, int m)
{
    int  q;
    int i = 0, gcd = 0, c = 0;
    int mass[256];
    int mod = m;
    while (gcd != 1)
    {
        q = m / a;
        gcd = m % a;
        if (gcd == 0)
        {
            return 0;
        }
        m = a;
        a = gcd;
        mass[i] = q;
        i++;
        c++;
    }
    int zero = 0, one = 1, a_1 = 0;
    for (int i = 0; i < c; i++)
    {
        a_1 = ((mass[i] * -1) * one) + zero;
        zero = one;
        one = a_1;
    }
    if (a_1 < 0)
    {
        a_1 = a_1 + mod;
    }
    return a_1;
}
void Euclid_Algorithm()
{
    int a, m;
    cout << "Введіть елемент: ";
    cin >> a;
    cout << "Введіть модуль: ";
    cin >> m;
    cout << "Обернений елемент: " << E_A(a,m) << endl;
}
void Linear_Equations()
{
    int a, b, m, x, a_1;
    cout << "Введіть елемент 'a' і 'b' : ";
    cin >> a >> b;
    cout << "Введіть модуль : ";
    cin >> m;
    int d = gcd(a, m);
    if (d == 1)
    {
        a_1 = E_A(a, m);
        x = (a_1 * b) % m;
        cout << "Має один розв'язок : " << x << endl;
    }
    else if (d > 1)
    {
        if ((b % d) == 0)
        {
            if (E_A(a, m) == 0)
            {
                cout << " Немає розв'язка : gcd = 0" << endl;
            }
            else
            {
                cout << "Рівняння має " << d << " розв'язків :" << endl;
                a_1 = E_A(a, m);
                int x_0 = (b * a_1) % m;
                for (int i = 0; i < d; i++)
                {
                    cout << "x[" << i << "] = " << x_0 + (m * i) << endl;
                }
            }
        }
        else
        {
            cout << "Рівняння немає розв'язків" << endl;
        }
    }
}
void Bigram()
{
    ifstream fin;
    ofstream fout;
    char ch, arr[2], a, b;
    int count = 0, i = 0, j = 0;
    fout.open("D:\\Crypto3\\bigram2.txt");
    fin.open("D:\\Crypto3\\06.txt");
    while (fin.get() != EOF)
    {
        count++;
    }
    cout << count;
    char* mass = new char[count];
    int count1 = count / 2;
    string* str = new string[count1];
    fin.close();
    fin.open("D:\\Crypto3\\06.txt");
    while (fin.get(ch))
    {
        mass[i] = ch;
        i++;
    }
    fin.close();
    string a1, b1, c1;
    string* str2 = new string[count1];
    for (int i = 0; i < count; i = i + 2)
    {
        a1 = mass[i];
        b1 = mass[i + 1];
        c1 = a1 + b1;
        str[j] = c1;
        j++;
    }
    int length = 0, g = 0;
    bool bol;
    for (int i = 0; i < count1; i++)
    {
        for (int j = 0; j < count1; j++)
        {
            if (str[i] == str[j])
            {
                length++;
            }
        }

        for (int k = 0; k <= g; k++)
        {
            if (str2[k] != str[i])
            {
                bol = true;
            }
            else
            {
                bol = false;
                break;
            }
        }
        if (bol == true)
        {
            str2[g] = str[i];
            fout << str[i] << " : " << length << endl;
            g++;
        }
        length = 0;
    }
    fout.close();
}
void Find_Key()
{
    int a, b, c1 = 0, c2 = 0;
    const char alf[] = "абвгдежзийклмнопрстуфхцчшщьыэюя";
    const char bigram1[] = "стноентона";
    const char bigram2[] = "щехечвлецв";
    int bigramvar[5]; // { "ще", "хе", "чв", "ле", "цв" };
    int bigramrus[5]; // { "ст", "но", "ен", "то", "на" };
    for (int i = 0; i < 10; i = i + 2)
    {
        a = 0;
        b = 0;
        for (int j = 0; j < 31; j++)
        {
            if (bigram1[i] == alf[j])
            {
                a = j;
            }
            if (bigram1[i + 1] == alf[j])
            {
                b = j;
            }
        }
        bigramrus[c1] = a * 31 + b;
        c1++;
    }
    ofstream fout;
    fout.open("D:\\Crypto3\\key.txt");
    for (int i = 0; i < 10; i = i + 2)
    {
        a = 0;
        b = 0;
        for (int j = 0; j < 31; j++)
        {
            if (bigram2[i] == alf[j])
            {
                a = j;
            }
            if (bigram2[i + 1] == alf[j])
            {
                b = j;
            }
        }
        bigramvar[c2] = a * 31 + b;
        c2++;
    }
    int key_a, key_b, m = 961, ea_r, ea_v;
    for (int i = 0; i < 5; i++)
    {
        for (int j = 1; j <= 5; j++)
        {
            if (j == 5)
            {
                j = 0;
            }
            for (int g = 0; g < 5; g++)
            {
                for (int h = 1; h <= 5; h++)
                {
                    if (h == 5)
                    {
                        h = 0;
                    }
                    ea_r = bigramrus[i] - bigramrus[j];
                    if (ea_r < 0)
                    {
                        ea_r = (ea_r % m) + m;
                    }
                    else
                    {
                        ea_r %= m;
                    }
                    ea_v = bigramvar[g] - bigramvar[h];
                    if (ea_v < 0)
                    {
                        ea_v = (ea_v % m) + m;
                    }
                    else
                    {
                        ea_v %= m;
                    }
                    ea_r = E_A(ea_r, m);
                    if (ea_r != 0 && ea_v != 0)
                    {
                        key_a = ea_r * ea_v;
                        if (key_a < 0)
                        {
                            key_a = (key_a % m) + m;
                        }
                        else
                        {
                            key_a %= m;
                        }
                        if (key_a != 0)
                        {
                            key_b = bigramvar[g] - (key_a * bigramrus[i]);
                            if (key_b < 0)
                            {
                                key_b = (key_b % m) + m;
                            }
                            else
                            {
                                key_b %= m;
                            }
                            fout << key_a << "\n" << key_b << endl;
                        }
                    }
                    if (h == 0)
                    {
                        h = 5;
                    }
                }

            }
            if (j == 0)
            {
                j = 5;
            }
        }
    }
    fout.close();
}
int Affine_Сipher_VAR(int a, int b)
{
    const char alf[] = "абвгдежзийклмнопрстуфхцчшщьыэюя";
    int  a1, b1, a_1, count = 0, X, Y, w1, w2;
    a_1 = E_A(a, 961);
    if (a_1 != 0)
    {
        ifstream fin;
        ofstream fout;
        fin.open("D:\\Crypto3\\06.txt");
        fout.open("D:\\Crypto3\\decipher.txt");
        char ch;
        while (fin.get() != EOF)
        {
            count++;
        }
        fin.close();
        int c = 0;
        int bigram = 0, bigram_next = 2;
        for (int j = 0; j < count; j = j + 2)
        {
            Y = 0, X = 0, a1 = 0, b1 = 0, c = 0; w1 = 0, w2 = 0;
            fin.open("D:\\Crypto3\\06.txt");
            while (fin.get(ch))
            {
                if (c >= bigram && c < bigram_next)
                {
                    for (int i = 0; i < 31; i++)
                    {
                        if (c == bigram)
                        {
                            if (alf[i] == ch)
                            {
                                a1 = i;
                            }
                        }
                        if (c == (bigram + 1))
                        {
                            if (alf[i] == ch)
                            {
                                b1 = i;
                            }
                        }
                    }
                }
                c++;
                if (c == bigram_next)
                {
                    break;
                }
            }
            fin.close();
            bigram = bigram_next;
            bigram_next += 2;
            Y = (a1 * 31) + b1;
            X = a_1 * (Y - b);
            if (X < 0)
            {
                X = (X % 961) + 961;
            }
            else
            {
                X %= 961;
            }
            w1 = X / 31;
            w2 = X % 31;
            fout << alf[w1] << alf[w2];
        }
        fout.close();
        return 1;
    }
    else
    {
        return 0;
    }
}
double IndexText()
{
    double count = 0;
    double index = 0;
    char ch;
    double letter;
    double freque;
    const int SIZE = 32;
    const char alph[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
                          'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
                          'ц','ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я' };
    ifstream fin;
    fin.open("D:\\Crypto3\\decipher.txt");
    if (!fin.is_open())
    {
        cout << "Ошибка открытия файла!\n";
    }
    else
    {
        while (fin.get() != EOF)
        {
            count++;
        }
    }
    fin.close();
    for (int i = 0; i < SIZE; i++)
    {
        fin.open("D:\\Crypto3\\decipher.txt");
        if (!fin.is_open())
        {
            cout << "Ошибка открытия файла!\n";
        }
        else
        {
            letter = 0;
            freque = 0;
            while (fin.get(ch))
            {
                if (ch == alph[i])
                {
                    letter++;
                }
            }
            freque = (letter) / (count);
            index = index + (freque * freque);
        }
        fin.close();
    }
    return index;;
}
void Find_Key_Variant()
{
    ifstream fin;
    ofstream fout;
    fin.open("D:\\Crypto3\\key.txt");
    fout.open("D:\\Crypto3\\decipher.txt");
    string str;
    int c = 0, a, b;
    while (getline(fin, str))
    {
        int key = atoi(str.c_str());
        if (c == 0)
        {
            a = key;
            c++;
        }
        else
        {
            b = key;
            if (Affine_Сipher_VAR(a, b) == 1)
            {
                if (IndexText() > 0.05 && IndexText() < 0.06)
                {
                    cout << "Ключи : " << a << " " << b << " ПОДХОДИТ" << endl;
                }
                else
                {
                    cout << "Ключи : " << a << " " << b << " не подходят" << endl;
                }
            }
            c = 0;
        }

    }
}
void Affine_Сipher()
{
    const char alf[] = "абвгдежзийклмнопрстуфхцчшщьыэюя";
    int a, b, a1, b1, a_1, count = 0, X, Y, w1, w2;
    cout << "Введите пару ключей 'a' и 'b' через пробел : ";
    cin >> a >> b;
    a_1 = E_A(a, 961);
    ifstream fin;
    ofstream fout;
    fin.open("D:\\Crypto3\\06.txt");
    fout.open("D:\\Crypto3\\decipher.txt");
    char ch;
    while (fin.get() != EOF)
    {
        count++;
    }
    fin.close();
    int c = 0;
    int bigram = 0, bigram_next = 2;
    for (int j = 0; j < count; j = j + 2)
    {
        Y = 0, X = 0, a1 = 0, b1 = 0, c = 0, w1 = 0, w2 = 0;
        fin.open("D:\\Crypto3\\06.txt");
        while (fin.get(ch))
        {
            if (c >= bigram && c < bigram_next)
            {
                for (int i = 0; i < 31; i++)
                {
                    if (c == bigram)
                    {
                        if (alf[i] == ch)
                        {
                            a1 = i;
                        }
                    }
                    if (c == (bigram + 1))
                    {
                        if (alf[i] == ch)
                        {
                            b1 = i;
                        }
                    }
                }
            }
            c++;
            if (c == bigram_next)
            {
                break;
            }
        }
        fin.close();
        bigram = bigram_next;
        bigram_next += 2;
        Y = (a1 * 31) + b1;
        X = a_1 * (Y - b);
        if (X < 0)
        {
            X = (X % 961) + 961;
        }
        else
        {
            X %= 961;
        }
        w1 = X / 31;
        w2 = X % 31;
        fout << alf[w1] << alf[w2];
    }
    fout.close();
}
int main()
{
    setlocale(LC_ALL, "Russian");
    int variant = 0;
    do 
    {
        print_menu();

        variant = get_variant(6);

        switch (variant) {
        case 1:
            Euclid_Algorithm();
            break;
        case 2:
            Linear_Equations();
            break;
        case 3:
            Bigram();
            break;
        case 4:
            Find_Key();
            break;
        case 5:
            Find_Key_Variant();
            break;
        case 6:
            Affine_Сipher();
            break;
        }
        if (variant != 6)
            system("pause");
    } while (variant != 6);
}