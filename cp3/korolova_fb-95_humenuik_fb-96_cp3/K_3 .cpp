\ufeff#include <string>
#include <fstream>
#include <streambuf>
#include<iostream>
#include<cmath>
#include <vector>
#include <locale>
#include <string>
#include <algorithm>
#include <conio.h>
#include <windows.h>
#include <string.h>
#include <stdlib.h>
#include <memory>
#include <map>
#include <unordered_map>
#include <iterator>
#include <regex>
#include <sstream>
#include <cmath>
#include <list>
#include <iomanip>
#include "AllBigrams.h"
using namespace std;
int gModule = 961;
bool DeleteExtraLetters(char c)
{
    switch (c)
    {
    case '\u0430':
    case '\u0431':
    case '\u0432':
    case '\u0433':
    case '\u0434':
    case '\u0435':
    case '\u0436':
    case '\u0437':
    case '\u0438':
    case '\u0439':
    case '\u043a':
    case '\u043b':
    case '\u043c':
    case '\u043d':
    case '\u043e':
    case '\u043f':
    case '\u0440':
    case '\u0441':
    case '\u0442':
    case '\u0443':
    case '\u0444':
    case '\u0445':
    case '\u0446':
    case '\u0447':
    case '\u0448':
    case '\u0449':
    case '\u044a':
    case '\u044b':
    case '\u044c':
    case '\u044d':
    case '\u044e':
    case '\u044f':
        return false;
    default:
        return true;
    }
}
map< char, int> Alphabet_Rus = { {'\u0430', 0 },
                                {'\u0431', 1 },
                                {'\u0432', 2 },
                                {'\u0433', 3 },
                                {'\u0434', 4 },
                                {'\u0435', 5 },
                                {'\u0436', 6 },
                                {'\u0437', 7 },
                                {'\u0438', 8 },
                                {'\u0439', 9 },
                                {'\u043a', 10},
                                {'\u043b', 11},
                                {'\u043c', 12},
                                {'\u043d', 13},
                                {'\u043e', 14},
                                {'\u043f', 15},
                                {'\u0440', 16},
                                {'\u0441', 17},
                                {'\u0442', 18},
                                {'\u0443', 19},
                                {'\u0444', 20},
                                {'\u0445', 21},
                                {'\u0446', 22},
                                {'\u0447', 23},
                                {'\u0448', 24},
                                {'\u0449', 25},
                                {'\u044b', 26},
                                {'\u044c', 27},
                                {'\u044d', 28},
                                {'\u044e', 29},
                                {'\u044f', 30} };

map< int, string> Alphabet_Rus_2{ {0 , "\u0430" },
                                { 1, "\u0431"},
                                { 2, "\u0432"},
                                { 3, "\u0433"},
                                { 4, "\u0434"},
                                { 5, "\u0435"},
                                { 6, "\u0436"},
                                { 7, "\u0437"},
                                { 8, "\u0438"},
                                { 9, "\u0439"},
                                {10, "\u043a"},
                                {11, "\u043b"},
                                {12, "\u043c"},
                                {13, "\u043d"},
                                {14, "\u043e"},
                                {15, "\u043f"},
                                {16, "\u0440"},
                                {17, "\u0441"},
                                {18, "\u0442"},
                                {19, "\u0443"},
                                {20, "\u0444"},
                                {21, "\u0445"},
                                {22, "\u0446"},
                                {23, "\u0447"},
                                {24, "\u0448"},
                                {25, "\u0449"},
                                {26, "\u044a"},
                                {27, "\u044b"},
                                {28, "\u044c"},
                                {29, "\u044d"},
                                {30, "\u044e"},
                                {31, "\u044f"} };
//\u043f\u043e\u0438\u0441\u043a \u043f\u043e \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044e \u0432 \u043c\u0430\u043f\u0435 \u0438 \u0432\u0441\u0442\u0432\u043a\u0430 \u043d\u0443\u0436\u043d\u043e\u0433\u043e \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f
void MapFindValueStringInt(int pValue, map<string, int> pMap, map < int, string>* pMapIn)
{
    map < string, int> ::iterator lMapIterator;
    for (lMapIterator = pMap.begin(); lMapIterator != pMap.end(); lMapIterator = next(lMapIterator))
    {
        if (lMapIterator->second == pValue)
        {
            pMapIn->insert(make_pair(lMapIterator->second, lMapIterator->first)); ;
            break;
        }
    }
}
//\u043f\u043e\u043b\u0435\u0447\u0430\u0435\u043c \u0442\u0435\u043a\u0441\u0442 \u0441 \u0444\u0430\u0439\u043b\u0430 \u0438 \u0437\u0430\u043f\u0438\u0441\u044b\u0432\u0430\u0435\u043c \u0432 vector<char>
/////////////////////////////////////////////////////////////////////////////////////////
void RetrievingInformationFromAFile(std::vector<char>* pText, string pPath)
{
    std::ifstream inBigramka(pPath);
    std::vector<char> lText{
        std::istreambuf_iterator<char>(inBigramka),
        std::istreambuf_iterator<char>() };
    *pText = lText;
}
//\u043f\u0435\u0440\u0435\u0432\u043e\u0434\u0438\u043c \u0442\u0435\u043a\u0441\u0442 \u0432 \u043c\u0430\u0441\u0441\u0438\u0432 char
void ConvertVectorToChar(std::vector<char> pText, char* pCharElement)
{
    for (int a = 0; a < pText.size(); a++)
    {
        pCharElement[a] = pText[a];
    }
    int a = pText.size();
    pCharElement[a] = '\0';
}
//\u041f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u044f \u0441 \u0412\u0435\u0442\u043e\u0440\u043e\u0432 \u0447\u0430\u0440\u0430 \u043f\u0440\u043e\u0441\u0442\u043e \u043c\u0430\u0441\u0441\u0438\u0432 \u0447\u0430\u0440\u043e\u0432
char* VectorCharToChar(string pPath, int* lSizeText)
{
    ////////////////////////////////////// \u041b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435
    std::vector<char> lText;
    //////////////////////////////////////
    RetrievingInformationFromAFile(&lText, pPath);//\u0441\u0447\u0438\u0442\u044b\u0432\u0430\u0435\u043c \u0444\u0430\u0439\u043b\u044b \u043f\u043e \u043f\u0443\u0442\u0438 \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0443 \u043d\u0430\u0441 \u044d\u0441\u0442\u044c
    lText.erase(std::remove_if(lText.begin(), lText.end(), &DeleteExtraLetters), lText.end());//\u0443\u0434\u0430\u043b\u044f\u0435\u043c \u043b\u0438\u0448\u043d\u0438\u0435 \u0441\u0438\u043c\u0432\u043e\u043b\u044b
    char* lTextInChar = new char[lText.size()];
    *lSizeText = lText.size();
    //////////////////////////////////////
    ConvertVectorToChar(lText, lTextInChar);//\u043f\u0440\u0435\u0432\u0440\u0430\u0449\u0430\u0435\u043c \u0432\u0435\u043a\u0442\u043e\u0440 \u0447\u0430\u0440\u043e\u0432 \u0432 \u043c\u0430\u0441\u0441\u0438\u0432 \u0447\u0430\u0440\u043e\u0432
    return lTextInChar;
}
///////////////////////////////////////////////////////////////////////////////////////////
//\u0432\u044b\u0432\u043e\u0434\u0438\u043c \u0447\u0430\u0441\u0442\u043e \u0432\u0441\u0442\u0440\u0435\u0447\u0430\u0435\u043c\u044b\u0435 \u0431\u0438\u0433\u0440\u0430\u043c\u043a\u0438
void PrintoutBigramki(map < string, int>* pMaxBigramki)
{
    for (auto lMaxBigramki : *pMaxBigramki)
    {
        cout << lMaxBigramki.first << "\t:" << lMaxBigramki.second << "\t" << endl;
    }
}
//\u041f\u043e\u0438\u0441\u043a \u0432\u0441\u0435\u0445 \u0431\u0438\u0433\u0440\u0430\u043c\u043e\u043a \u0432 \u0442\u0435\u043a\u0441\u0442\u0435
void FindBigramka(map < string, int>* pAllBigrams, char* pTextInChar, int  lSizeText, int* lQuontityBigrams)
{
    int kabachok = 0;
    map < string, int> ::iterator it_1, it_2;
    for (int h = 0; h <= lSizeText; h = h + 2)//for each char in string/////
    {
        if (h <= lSizeText - 1)
        {
            char BigramkaChar[3] = { pTextInChar[h],pTextInChar[h + 1],0 };
            std::string BigramkaString(BigramkaChar);

            it_2 = it_1 = pAllBigrams->find(BigramkaString);
            if (it_2 == pAllBigrams->end())
            {
                pAllBigrams->insert(make_pair(BigramkaString, 1));
                (*lQuontityBigrams)++;
            }
            else if (it_2 != pAllBigrams->end())
            {
                it_2->second++;
                (*lQuontityBigrams)++;
            }
        }
    }
}
//\u043f\u043e\u0438\u0441\u043a 5 \u0441\u0430\u043c\u044b\u0445 \u0432\u0441\u0442\u0440\u0435\u0447\u0430\u0435\u043c\u044b\u0445 \u0431\u0438\u0433\u0440\u0430\u043c\u043e\u043a \u0432 \u0442\u0435\u043a\u0441\u0442\u0430\u0445
void Max5Bigrams(map < string, int> pAllBigrams, map < string, int>* pMaxBigramki, int pQuontityBigrams)
{
    for (int i = 1; i <= 5; i++)
    {
        auto x = std::max_element(pAllBigrams.begin(), pAllBigrams.end(), [](const pair<string, int>& p1, const pair<string, int>& p2) {return p1.second < p2.second; });
        cout << x->first << " : " << x->second << endl;
        pMaxBigramki->insert(make_pair(x->first, i));
        pAllBigrams.erase(x->first);
    }
}
//\u043f\u043e\u0438\u0441\u043a \u0441\u0430\u043c\u044b\u0445 \u0432\u0441\u0442\u0440\u0435\u0447\u0430\u0435\u043c\u044b\u0445 \u0431\u0438\u0433\u0440\u0430\u043c\u043e\u043a
void MostUsed(string pPath, map < string, int>* pMaxBigramki)
{
    ////////////////////////////////////// \u041b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435
    map < string, int> lAllBigrams;
    int  lSizeText = 0;
    //////////////////////////////////////
    char* lTextInChar = VectorCharToChar(pPath, &lSizeText);
    int lQuontityBigrams = 0;
    FindBigramka(&lAllBigrams, lTextInChar, lSizeText, &lQuontityBigrams);

    Max5Bigrams(lAllBigrams, pMaxBigramki, lQuontityBigrams);
    cout << "\u0412\u044b\u0432\u043e\u0434 \u0434\u043b\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438!" << endl;
    for (auto lMaxBigramki : *pMaxBigramki)
    {
        cout << lMaxBigramki.first << "\t:" << lMaxBigramki.second << "\t" << endl;
    }
    cout << endl;   return;
}
//\u041f\u0440\u0435\u0432\u0440\u0430\u0449\u0435\u043d\u0438\u0435 \u0431\u0438\u0433\u0440\u0430\u043c\u043a\u0438 \u0432 \u0447\u0438\u0441\u043b\u043e
void BigramkaToValue(char *lDecipherBigram1, int* pIntValue)
{
    *pIntValue = Alphabet_Rus.find(lDecipherBigram1[0])->second * 31 + Alphabet_Rus.find(lDecipherBigram1[1])->second;
}
void gcd(int pfirstValue, int pMod, map<map<int, int>, int> *pResultForGcd)
{
    map <int, int> lValuesOfGcd;
    int lCounter = 1;
    while (pfirstValue > 0 && pMod > 0)
    {
        if (pfirstValue > pMod)
        {
            lValuesOfGcd.insert(make_pair(lCounter,pfirstValue / pMod));

            pfirstValue %= pMod;
        }

        else
        {
            lValuesOfGcd.insert(make_pair(lCounter, pMod / pfirstValue));
            pMod %= pfirstValue;
        }
        lCounter++;
    }
    pResultForGcd->insert(make_pair(lValuesOfGcd, pMod + pfirstValue));
}
void ReverseNumber(int pValue, int pMod, int* pReversFirstValue)
{
    map<map<int, int>, int> lResultForGcd;
    //map<int, int> ::iterator lIterator233;
    map<map<int, int>, int> ::iterator asdsf;
    if (pValue<0)
    {
        double lIDK = -pValue/ gModule;
        pValue = pValue + (lIDK+1)*gModule;
    }
    gcd(pValue, pMod, &lResultForGcd);

    if (lResultForGcd.begin()->second != 1)
    {
        cout << "Gcd not equal to 1" << endl;
        return;
    }
    map<int, int> result;
    map<int, int> :: iterator lResultIterator;
    result.insert(make_pair(0, 0));
    result.insert(make_pair(1, 1));

    int lValue = gModule;
    int lCounter = 2;
    for (int begin = 0; begin < lResultForGcd.begin()->first.size(); begin++)
    {
        int lChecker1 = lResultForGcd.begin()->first.find(begin+1)->second;
        int lChecker2 = result.find(begin + 1)->second;
        int lChecker3 = result.find(begin)->second;
        int lChecker4 = (lValue - lChecker1) * lChecker2;
        int lChecker5 = lChecker4 + lChecker3;
        int lChecker6 = lChecker5%961;

        result.insert(make_pair(lCounter,(((lValue - lResultForGcd.begin()->first.find(begin+1)->second) * result.find(begin+1)->second) + result.find(begin)->second) % 961));
        lCounter++;
    }
    lResultIterator = prev(prev(result.end()));
    *pReversFirstValue= lResultIterator->second;
}
void LinearEquation(int pFirstValue, int pSecondValue, int pMod, map <int, int>*pAllA)
{
    map<map<int,int>,int> lResultForGcd;
    gcd(pFirstValue, pMod, &lResultForGcd);

    if (lResultForGcd.begin()->second == 1)
    {
        int lReversFirstValue = 0; int lA = 0;
        ReverseNumber(pFirstValue, pMod,&lReversFirstValue);
        lA = lReversFirstValue * pSecondValue;
        if (lA < 0)
        {
            double lIDK = -lA / gModule;
            lA = lA + (lIDK + 1) * gModule;
        }
        pAllA->insert(make_pair(1, lA));
        return;
    }
    if (pSecondValue % lResultForGcd.begin()->second > 0){return ;}
    int lValue = lResultForGcd.begin()->second, lX0 = 0;

    ReverseNumber((pFirstValue / lValue) *(pSecondValue / lValue), pMod / lValue, &lX0);

    map<int, int> lRresult;
    map<int, int> ::iterator lResultIterator;
    int lCounter = 2;
    for (int begin = 0; begin < lResultForGcd.begin()->first.size(); begin++)
    {
        lRresult.insert(make_pair(lX0 + begin* pMod, pMod));
        lCounter++;
    }
    *pAllA = lRresult;
}
//\u0424\u0443\u043d\u043a\u0446\u0438\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438 \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u0447\u0438\u0441\u043b\u0430
int Proverka(int lValue)
{
    if (lValue < 0)
    {
        double lIDK = -lValue / gModule;
        return lValue + (lIDK + 1) * gModule;
    }
    else if (lValue > gModule)
    {
        double lIDK = lValue / gModule;
        return lValue - lIDK * gModule;
    }
    else { return lValue; }
}
//\u0424\u0443\u043d\u043a\u0446\u0438\u044f \u043f\u043e\u0434\u0441\u0447\u0435\u0442\u0430 \u0431\u0443\u043a\u0432\u044b \u0430 \u0438 \u0431
void AandB(map < int, string> ::iterator pDecipherBigram1, map < int, string> ::iterator pDecipherBigram2, map < map< int, int>, string> ::iterator pCipherBigram1, map < map< int, int>, string> ::iterator pCipherBigram2, double* a, double* b)
{
    double Module = 961;
    char* lDecipherBigram1 = &pDecipherBigram1->second[0];
    char* lDecipherBigram2 = &pDecipherBigram2->second[0];
    char* lCipherBigram1 = &pCipherBigram1->second[0];
    char* lCipherBigram2 = &pCipherBigram2->second[0];
    char alkjla = pDecipherBigram1->second[0];
    int x1 = 0, x2 = 0, y1 = 0, y2 = 0;
    BigramkaToValue(lDecipherBigram1, &x1);
    BigramkaToValue(lDecipherBigram2, &x2);
    BigramkaToValue(lCipherBigram1, &y1);
    BigramkaToValue(lCipherBigram2, &y2);
    
    int lB = 0,lA = 0;
    map <int, int> lAllA;
    LinearEquation(x1- x2, y1- y2, gModule,&lAllA);
    if (lAllA.size() == 1)
    {
        lB = y1 - lAllA.begin()->second * x1;
        *b = Proverka(lB);
        lA = lAllA.begin()->second;
        *a = Proverka(lA);
        return;
    }
}
//\u043f\u043e\u0438\u0441\u043a \u043f\u043e \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044e \u0432 \u043c\u0430\u043f\u0435 \u0438 \u0432\u0441\u0442\u0432\u043a\u0430 \u043d\u0443\u0436\u043d\u043e\u0433\u043e \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f
void MapFindValue(map < int, int> ::iterator pIterator, map<string, int> pMap, map < map< int, int>, string>* pMapIn)
{
    map < string, int> ::iterator lMapIterator;
    map< int, int> lMapForValue;
    lMapForValue.insert(make_pair(pIterator->first, pIterator->second));
    for (lMapIterator = pMap.begin(); lMapIterator != pMap.end(); lMapIterator = next(lMapIterator))
    {
        if (lMapIterator->second == pIterator->second)
        {
            pMapIn->insert(make_pair(lMapForValue, lMapIterator->first)); ;
            break;
        }
    }
}
//\u0421\u0447\u0438\u0442\u0430\u0435\u043c \u0431\u0443\u043a\u0432\u044b \u0430 \u0438 \u0431 \u0434\u043b\u044f \u043d\u0430\u0448\u0435\u0439 \u0434\u0435\u0448\u0438\u0444\u0440\u043e\u0432\u043a\u0443 \u0430\u0444\u0438\u043d\u043d\u043e\u0433\u043e \u0448\u0438\u0444\u0440\u0430
void AllAandB(map < string, int>pMaxBigramkiForDeciphertext, map < string, int> pMaxBigramkiForCiphertext, map<int, map<int, int>> pAllKeys, map<int, map<double, double>>* pAllKeysAandB)
{
    map < map< int, int>, string> lMBFCTITRO;//pMax bigramki for cipher text in the right order
    map < map< int, int>, string> ::iterator lMBFCTITROIterator;
    map < int, string> ::iterator lMBFDTConstIterator;// 1 2 3 4 5 
    map < int, int> ::iterator lAllKeysIterator;
    map < int, string>  lMBFDTConst;// 1 2 3 4 5 

    for (int lCounter = 1; lCounter <= 5; lCounter++)
    {
        MapFindValueStringInt(lCounter, pMaxBigramkiForDeciphertext, &lMBFDTConst);
    }
    int lCounter = 1;
    map<double, double> lValueForAAndB;
    for (auto lAllKeys : pAllKeys)
    {
        lAllKeysIterator = lAllKeys.second.begin();
        for (lAllKeysIterator; lAllKeysIterator != lAllKeys.second.end(); lAllKeysIterator = next(lAllKeysIterator))
        {
            MapFindValue(lAllKeysIterator, pMaxBigramkiForCiphertext, &lMBFCTITRO);
        }
        double a = 0, b = 0;
        lMBFCTITROIterator = lMBFCTITRO.begin();
        lMBFDTConstIterator = lMBFDTConst.begin();
        map<double, double> lValueForAAndBTemporary;

        for (lMBFCTITROIterator; lMBFCTITROIterator != prev(lMBFCTITRO.end()); lMBFCTITROIterator = next(lMBFCTITROIterator))
        {
            AandB(lMBFDTConstIterator, next(lMBFDTConstIterator), lMBFCTITROIterator, next(lMBFCTITROIterator), &a, &b);
            if ((a != 0 && b != 0) && (lValueForAAndB.find(a) == lValueForAAndB.end()))
            {
                lValueForAAndB.insert(make_pair(a, b));
                lValueForAAndBTemporary.insert(make_pair(a, b));
                pAllKeysAandB->insert(make_pair(lCounter, lValueForAAndBTemporary));
                lCounter++; lValueForAAndBTemporary.clear();
            }
            a = 0, b = 0;
            lMBFDTConstIterator = next(lMBFDTConstIterator);
        }
        cout << lAllKeys.first<<endl;
        lMBFCTITRO.clear();
    }
}
string FindingLetterByNumber(int n)
{
    if (n < 26) 
    { 
        int lValue = n - 32;
        if (lValue < 0) { lValue = 32 + lValue; }
        return Alphabet_Rus_2.find(lValue)->second;
    }
    else 
    {
        int lValue = n + 1 - 32;
        if (lValue < 0) { lValue = 32 + lValue; }
        return Alphabet_Rus_2.find(lValue)->second;
    }
}
string GettingBigram(int n)
{
    return FindingLetterByNumber(n / 31) + FindingLetterByNumber(n % 31);
}
string DecipheringBigramka(string BigramkaString, double pA, double pB)
{
    char* lDBigram = &BigramkaString[0];
    string DecipherBigramkaString = "";
    int y1 = 0, lReversFirstValue=0;
    BigramkaToValue(lDBigram, &y1);

    ReverseNumber(pA, gModule, &lReversFirstValue);
    
    int lXProverka = (y1 - pB) * lReversFirstValue, lX = 0;
    lX = Proverka(lXProverka);
    DecipherBigramkaString = DecipherBigramkaString + GettingBigram(lX);
    return DecipherBigramkaString;
}
//\u0414\u0435\u0448\u0438\u0444\u0440\u043e\u0432\u043a\u0430 \u0432\u0441\u0435\u0445 \u0442\u0435\u043a\u0441\u0442\u043e\u0432
string DecipheringText(char* lTextInChar, int lSizeText, map<double, double> lMapWithKey)
{
    string DecipheringNeededText = "";
    for (int h = 0; h <= lSizeText; h = h + 2)//for each char in string/////
    {
        if (h <= lSizeText - 1)
        {
            char BigramkaChar[3] = { lTextInChar[h],lTextInChar[h + 1],0 };
            std::string BigramkaString(BigramkaChar);
            map<double, double>   ::iterator lIteratorWithKey = lMapWithKey.begin();
            DecipheringNeededText = DecipheringNeededText + DecipheringBigramka(BigramkaString, lIteratorWithKey->first, lIteratorWithKey->second);
        }
    }
    return DecipheringNeededText;
}
//\u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0442\u0435\u043a\u0441\u0442\u043e\u0432 \u0441 \u043f\u043b\u043e\u0445\u0438\u043c\u0438 \u0431\u0438\u0433\u0440\u0430\u043c\u0430\u043c\u0438
void DeletingBannedBigrams(map < int, map < string, int>>* pAllBigramsForAllTextes, map < int, string>* pAllTexts, int lQuontityBigram)
{
    map < int, string> BannedBigrams {  { 0, "\u0430\u044c" },
                                        { 1, "\u0443\u044c" },
                                        { 2, "\u043e\u044c" },
                                        { 3, "\u0435\u044c" },
                                        { 4, "\u0438\u044c" },
                                        { 5, "\u044b\u044c" },
                                        { 6, "\u044d\u044c" },
                                        { 7, "\u044e\u044c" },
                                        { 8, "\u044f\u044c" },
                                        { 9, "\u0439\u044c" },
                                        {10, "\u043a\u044c" },
                                        {11, "\u0445\u044c" },
                                        {12, "\u0446\u044c" },
                                        {13, "\u044c\u0430" },
                                        {14, "\u044c\u0439" },
                                        {15, "\u044c\u0443" },
                                        {16, "\u044c\u044b" },
                                        {17, "\u044c\u043b" },
                                        {18, "\u044c\u044c" },
                                        {19, "\u0439\u0439" },
                                        {20, "\u0448\u0448" },
                                        {21, "\u0449\u0449" },
                                        {22, "\u044b\u044b" },
                                        {23, "\u044d\u044d" } };
    map < int, map < string, int>>::iterator lIterator;
    int lValue = 0;
    for (lIterator = pAllBigramsForAllTextes->begin(); lIterator != pAllBigramsForAllTextes->end(); lIterator = next(lIterator))
    {
        map < string, int> lMap = lIterator->second;
        map < string, int> ::iterator lMapIterator = lMap.begin();
        map < int, string>::iterator BannedBigramsIterator = BannedBigrams.begin();
        for (BannedBigramsIterator = BannedBigrams.begin(); BannedBigramsIterator != BannedBigrams.end(); BannedBigramsIterator=next(BannedBigramsIterator))
        {
            lValue = lIterator->first;
            if ((lMap.find(BannedBigramsIterator->second) != lMap.end()) && (lMap.find(BannedBigramsIterator->second)->second > lQuontityBigram/100))
            {
                pAllTexts->erase(lIterator->first);
                break;
            }
        }
    }
}
double ConformityIndexTexs(string pTextInChar,int pSizeText)
{
    map< string, int> ArrayLetters;
    map< string, int> ::iterator it_1;
    double lMatchIndex = 0; int pSizeAlphabet = 1;
    for (int h = 0; h <= pSizeText; h++)//\u043f\u043e\u0438\u0441\u043a \u0442\u043e\u0433\u043e \u0441\u043a\u043e\u043b\u044c\u043a\u043e \u0440\u0430\u0437 \u0432\u0441\u0442\u0440\u0435\u0447\u0430\u0435\u0442\u0441\u044f \u043a\u0430\u0436\u0434\u0430\u044f \u0431\u0443\u043a\u0432\u0430
    {
        if (h <= pSizeText - 1)
        {
            char BigramkaChar[2] = { pTextInChar[h],0 };
            std::string BigramkaString(BigramkaChar);

            it_1 = ArrayLetters.find(BigramkaString);
            if (it_1 == ArrayLetters.end())
            {
                ArrayLetters.insert(make_pair(BigramkaString, 1));
            }
            else if (it_1 != ArrayLetters.end()){it_1->second++;}
        }
    }
    //////////////////////////////////////////////////////////////////////////////////////////////////////////\u0420\u0430\u0445\u0443\u0454\u043c\u043e \u0438\u043d\u0434\u0435\u043a\u0441
    for (auto& pArrayLetters : ArrayLetters)  //for each unique char in map
    {
        lMatchIndex = lMatchIndex + ((pArrayLetters.second) * (pArrayLetters.second - 1.0)) / (pSizeText * (pSizeText - 1));
        if (pSizeAlphabet == 31){return  lMatchIndex;}
        pSizeAlphabet++;
    }
}
//\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0438\u043d\u0434\u0435\u043a\u0441
bool CheckerIndex(double pIndex)
{
    if (pIndex > 0.05 && pIndex < 0.06) { return 1; }
    if (pIndex > 0.06) { return 0; }
}
//\u0414\u0435\u0448\u0438\u0444\u0440\u043e\u0432\u043a\u0430 \u0442\u0435\u043a\u0441\u0442\u0430 \u043f\u043e \u043e \u0438 \u0431 \u0438 \u043a\u0430\u043d\u0435\u0448 \u043f\u043e \u0441\u0430\u043c\u043e\u043c\u0443 \u0442\u0435\u043a\u0441\u0442\u0443
string FindingText(map<int, map<double, double>> lAllKeysAandB, string pPath)
{
    ////////////////////////////////////// \u041b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435
    map < int, string> lAllTexts;
    map < string, int> lAllBigrams;
    map < int, map < string, int>> lAllBigramsForAllTextes;
    map<int, map<double, double>> ::iterator lKeyIterator;
    lKeyIterator = lAllKeysAandB.begin();
    int lSizeText = 0;
    //////////////////////////////////////
    char* lTextInChar = VectorCharToChar(pPath,&lSizeText);
    cout << "\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432 " << (lSizeText - 1) << endl;
    string DecipheringNeededText = "";

    for (lKeyIterator = lAllKeysAandB.begin(); lKeyIterator != lAllKeysAandB.end(); lKeyIterator = next(lKeyIterator))
    {
        map<double, double> lMapWithKey = lKeyIterator->second;
        int lReversFirstValue = 0;
        ReverseNumber(lMapWithKey.begin()->first, gModule, &lReversFirstValue);
        if (lReversFirstValue == 0) {  }
        else 
        {
            DecipheringNeededText = DecipheringText(lTextInChar, lSizeText, lMapWithKey);
            lAllTexts.insert(make_pair(lKeyIterator->first, DecipheringNeededText));
            DecipheringNeededText.clear();
        }
    }
    int lQuontityBigram = 0;
    for (auto pAllTexts : lAllTexts)
    {
        int lQuontityBigrams = 0;
        char* DecipheringNeededTextInChar = &pAllTexts.second[0];
        int lSizeDecipherText = strlen(DecipheringNeededTextInChar);
        FindBigramka(&lAllBigrams, DecipheringNeededTextInChar, lSizeDecipherText, &lQuontityBigrams);
        lAllBigramsForAllTextes.insert(make_pair(pAllTexts.first, lAllBigrams));
        lQuontityBigram = lQuontityBigrams;
        lQuontityBigrams = 0; lAllBigrams.clear();
    }
    DeletingBannedBigrams(&lAllBigramsForAllTextes,&lAllTexts, lQuontityBigram);
    for (auto pAllTexts : lAllTexts)
    {
        double lIndex = ConformityIndexTexs(pAllTexts.second, lSizeText);
        bool lValue = CheckerIndex(lIndex);
        if (lValue == 1) 
        { 
            map<double, double> lMap = lAllKeysAandB.find(pAllTexts.first)->second;
            cout << lIndex << endl<< lMap.begin()->first << "\t" << lMap.begin()->second << endl << pAllTexts.second << endl;
        return pAllTexts.second; 
        }
    }
    cout << endl;
}
//\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u0438\u0435 \u043f\u043e \u0444\u043e\u0440\u043c\u0443\u043b\u0435
void LAKFJLAJF(string *SearchedText)
{
    string lPath = "\u0428\u0422.txt";
    map<int, map<double, double>> lAllKeysAandB;
    map<int, map<int, int>> lAllKeys;
    map< string, int> MaxBigramkiForDeciphertext{   { "\u0442\u043e"  , 1},
                                                    { "\u0435\u043d"  , 2},
                                                    { "\u043d\u043e"  , 3},
                                                    { "\u043d\u0430"  , 4},
                                                    { "\u0441\u0442"  , 5} };
    map< string, int> MaxBigramkiForCiphertext  {   { "\u0439\u0430"  , 1},
                                                    { "\u044e\u0430"  , 2},
                                                    { "\u0447\u0448"  , 3},
                                                    { "\u044e\u0434"  , 4},
                                                    { "\u0440\u0449"  , 5} };

    GettingKeys(&lAllKeys);//\u043f\u043e\u043b\u0443\u0447\u0430\u0435\u043c \u0432\u0441\u0435 \u0432\u0430\u0440\u0438\u043d\u0430\u0442\u044b \u0447\u0438\u0441\u0435\u043b \u0441 1 2 3 4 5 \u0434\u043e 5 4 3 2 1
    AllAandB(MaxBigramkiForDeciphertext, MaxBigramkiForCiphertext, lAllKeys, &lAllKeysAandB);
    *SearchedText = FindingText(lAllKeysAandB, lPath);
    cout << endl;
}
int main()
{
    setlocale(LC_ALL, "ru");
    system("color 0A");
    SetConsoleCP(1251);// \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u043a\u043e\u0434\u043e\u0432\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b win-cp 1251 \u0432 \u043f\u043e\u0442\u043e\u043a \u0432\u0432\u043e\u0434\u0430
    SetConsoleOutputCP(1251); // \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u043a\u043e\u0434\u043e\u0432\u043e\u0439 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b win-cp 1251 \u0432 \u043f\u043e\u0442\u043e\u043a \u0432\u044b\u0432\u043e\u0434
    string lText = "";
    LAKFJLAJF(&lText);

    system("pause");
    return 0;
}

