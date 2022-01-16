#include "Mathematic.h"
////////////////////
//переводим число из десятичной в двоичную систему исчисления
string DEC_TO_BIN(big_integer chislo)//работает не коректно юзай другое
{
    int k = 0, n = 0;
    string ReverseBin = "", Bin = "";
    big_integer t, lchislo = chislo;
    while (lchislo > 0)
    {
        t = lchislo % 2;
        //cout << lchislo << endl;
        k = n;
        string c = t;
        ReverseBin = ReverseBin + c;
        n += 1;
        lchislo = lchislo / 2;
    }
    for (int lIndex = ReverseBin.length() - 1; lIndex != -1; lIndex--)
    {
        Bin = Bin + ReverseBin[lIndex];
    }
    return Bin;
}
//переводим число из шестнадцитиричнои в десятичную систему исчисления
big_integer HEX_TO_DEC(string st)
{
    int i;
    big_integer s = 0, k, Sixten = 16, p_1 = st.length() - 1;
    for (i = 0; st[i] != '\0'; i++)
    {
        switch (toupper(st[i]))
        {
        case 'A': k = 10; break;
        case 'B': k = 11; break;
        case 'C': k = 12; break;
        case 'D': k = 13; break;
        case 'E': k = 14; break;
        case 'F': k = 15; break;
        case '1': k = 1; break;
        case '2': k = 2; break;
        case '3': k = 3; break;
        case '4': k = 4; break;
        case '5': k = 5; break;
        case '6': k = 6; break;
        case '7': k = 7; break;
        case '8': k = 8; break;
        case '9': k = 9; break;
        case '0': k = 0; break;
        }
        s = s + k * (Sixten.pow(p_1));
        p_1 = st.length() - 2 - i;
    }
    big_integer Otvet(s);
    return Otvet;
}
//переводим число из десятичной в шестнадцитиричную систему исчисления
string DEC_TO_HEX(big_integer Dec)
{
    char Elem;
    string OtvetString = "";
    big_integer  Sixten = 16;
    map<big_integer, char> lMap;
    for (big_integer i = 0; Dec > 0; i++)
    {
        big_integer Ostacha = Dec % Sixten;
        Dec = Dec / Sixten;
        if (Ostacha == 0) { Elem = '0'; }
        else if (Ostacha == 1) { Elem = '1'; }
        else if (Ostacha == 2) { Elem = '2'; }
        else if (Ostacha == 3) { Elem = '3'; }
        else if (Ostacha == 4) { Elem = '4'; }
        else if (Ostacha == 5) { Elem = '5'; }
        else if (Ostacha == 6) { Elem = '6'; }
        else if (Ostacha == 7) { Elem = '7'; }
        else if (Ostacha == 8) { Elem = '8'; }
        else if (Ostacha == 9) { Elem = '9'; }
        else if (Ostacha == 10) { Elem = 'A'; }
        else if (Ostacha == 11) { Elem = 'B'; }
        else if (Ostacha == 12) { Elem = 'C'; }
        else if (Ostacha == 13) { Elem = 'D'; }
        else if (Ostacha == 14) { Elem = 'E'; }
        else if (Ostacha == 15) { Elem = 'F'; }
        lMap.insert(make_pair(i, Elem));
    }
    for (map<big_integer, char>::iterator lIt = prev(lMap.end()); lIt != lMap.end(); lIt = prev(lIt))
    {
        OtvetString = OtvetString + lIt->second;
    }
    return OtvetString;

}
//Самый большой общий делитель
map<map<int, big_integer>, big_integer> GCD(big_integer pFirstValue, big_integer pSecondValue)
{
    map <int, big_integer> lValuesOfGcd;
    map<map<int, big_integer>, big_integer> lResultForGcd;
    int lCounter = 1;
    while (pFirstValue > 0 && pSecondValue > 0)
    {
        if (pFirstValue > pSecondValue)
        {
            lValuesOfGcd.insert(make_pair(lCounter, pFirstValue / pSecondValue));
            pFirstValue %= pSecondValue;
        }

        else
        {
            lValuesOfGcd.insert(make_pair(lCounter, pSecondValue / pFirstValue));
            pSecondValue %= pFirstValue;
        }
        lCounter++;
    }
    lResultForGcd.insert(make_pair(lValuesOfGcd, pSecondValue + pFirstValue));
    return lResultForGcd;
}
//Функция нахождения обратного значения нашего числа
big_integer ReverseNumber(big_integer pValue, big_integer pMod, map<map<int, big_integer>, big_integer> lResultForGcd)
{
    map<big_integer, big_integer> result;
    result.insert(make_pair(0, 0));
    result.insert(make_pair(1, 1));
    big_integer lValue = pMod;
    for (int begin = 0; begin < lResultForGcd.begin()->first.size(); begin++)
    {
        result.insert(make_pair(prev(result.end())->first + 1, (((lValue - lResultForGcd.begin()->first.find(begin + 1)->second) * result.find(begin + 1)->second) + result.find(begin)->second) % pMod));
    }
    return prev(prev(result.end()))->second;
}
