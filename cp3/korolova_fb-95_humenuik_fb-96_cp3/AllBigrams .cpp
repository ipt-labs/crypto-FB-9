#include "AllBigrams.h"

//создания начального map
void StartMap(map<int, int>* pKey)
{
    for (int i = 1; i <= 5; i++)
    {
        pKey->insert(make_pair(i, i));
        std::cout << i << " ";
    }
    std::cout << endl;
}
//расположение елементов в порядке спадания и запись в ключ
void ArrangeNumbersInAscendingOrder(map<int, int>* pConstKey, map<int, int>* pKey)
{
    map<int, int> ::iterator lEnd;
    map<int, int> ::iterator lBegin;
    map<int, int> ::iterator lpKey;

    int lValue;
    for (lEnd = prev(pConstKey->end()); lEnd != pConstKey->begin(); lEnd = prev(lEnd))
    {
        for (lBegin = pConstKey->begin(); lBegin != prev(pConstKey->end()); lBegin = next(lBegin))
        {
            if (lBegin->second > next(lBegin)->second)
            {
                lValue = lBegin->second;
                lBegin->second = next(lBegin)->second;
                next(lBegin)->second = lValue;
            }
        }
    }
    for (auto lConstKey : *pConstKey)
    {
        lpKey = pKey->find(lConstKey.first);
        lpKey->second = lConstKey.second;
    }
}
//расположение елементов в порядке спадания и запись в ключ
void ArrangeNumbersInDescendingOrder(map<int, int>* pConstKey, map<int, int>* pKey)
{
    map<int, int> ::iterator lEnd;
    map<int, int> ::iterator lBegin;
    map<int, int> ::iterator lpKey;

    int lValue;
    for (lEnd = prev(pConstKey->end()); lEnd != pConstKey->begin(); lEnd = prev(lEnd))
    {
        for (lBegin = pConstKey->begin(); lBegin != prev(pConstKey->end()); lBegin = next(lBegin))
        {
            if (lBegin->second < next(lBegin)->second)
            {
                lValue = lBegin->second;
                lBegin->second = next(lBegin)->second;
                next(lBegin)->second = lValue;
            }
        }
    }
    for (auto lConstKey : *pConstKey)
    {
        lpKey = pKey->find(lConstKey.first);
        lpKey->second = lConstKey.second;
    }
}
//выводит ключи
void OutKey(map<int, int> pKey)
{
    for (auto lKey : pKey)
    {
        std::cout << lKey.second << " ";
    }
    std::cout << endl;
}
//запись в мап с определенного елемента до конца
void WriteTo(map<int, int>::iterator pIterator, map<int, int>* pMap, map<int, int>* pNSymphols)
{
    map<int, int>::iterator lValuesWhichWeChange;
    for (lValuesWhichWeChange = pMap->find(std::next(pIterator)->first); lValuesWhichWeChange != pMap->end(); lValuesWhichWeChange = next(lValuesWhichWeChange))
    {
        pNSymphols->insert(make_pair(lValuesWhichWeChange->first, lValuesWhichWeChange->second));
    }
}
//перезапись ключа в порядке спадания
void ReWriting(map<int, int>::iterator pKeyForGame, map<int, int>* pKey, map<int, int>* pNSymphols)
{
    WriteTo(pKeyForGame, pKey, pNSymphols);
    ArrangeNumbersInAscendingOrder(pNSymphols, pKey);
}
//перезапись ключа в порядке возрастания
void ReWriting_Max(map<int, int>::iterator pKeyForGame, map<int, int>* pKey, map<int, int>* pNSymphols)
{
    WriteTo(pKeyForGame, pKey, pNSymphols);
    ArrangeNumbersInDescendingOrder(pNSymphols, pKey);
}
//поиск по значению в мапе
void MapFindValue(int pValue, map<int, int> pMap, int* pLocation)
{
    int lValue = 0;
    for (auto lMap : pMap)
    {
        if (lMap.second == pValue)
        {
            lValue = lMap.first;
            *pLocation = lValue;
            break;
        }
    }
}
//проверка на использываный елементи поиск минимального
void UsedMinElements(map<int, int> pUsedNumbers, map<int, int> pNSymphols, int* pMinElement)
{
    map<int, int> lNSymphols = pNSymphols;
    map<int, int> ::iterator lIterator;
    int pLocation = 0;
    if (pUsedNumbers.size() == 0)
    {
        *pMinElement = min_element(lNSymphols.begin(), lNSymphols.end(), [](const pair<int, int>& p1, const pair<int, int>& p2) {return p1.second < p2.second; })->second;
    }
    for (auto lUsedNumbers : pUsedNumbers)
    {
        int pValue = lUsedNumbers.second;
        *pMinElement = min_element(lNSymphols.begin(), lNSymphols.end(), [](const pair<int, int>& p1, const pair<int, int>& p2) {return p1.second < p2.second; })->second;
        if (*pMinElement == pValue)
        {
            MapFindValue(pValue, pNSymphols, &pLocation);
            lNSymphols.erase(pLocation);
        }
    }
}
//проверка на использываный елемент и поиск максимального
void UsedMaxElements(map<int, int> pUsedNumbers, map<int, int> pNSymphols, int* pMaxElement)
{
    map<int, int> lNSymphols = pNSymphols;
    map<int, int> ::iterator lIterator;
    int pLocation = 0;
    if (pUsedNumbers.size() == 0)
    {
        *pMaxElement = max_element(lNSymphols.begin(), lNSymphols.end(), [](const pair<int, int>& p1, const pair<int, int>& p2) {return p1.second < p2.second; })->second;
    }
    for (auto lUsedNumbers : pUsedNumbers)
    {
        int pValue = lUsedNumbers.second;
        *pMaxElement = max_element(lNSymphols.begin(), lNSymphols.end(), [](const pair<int, int>& p1, const pair<int, int>& p2) {return p1.second < p2.second; })->second;
        if (*pMaxElement == pValue)
        {
            MapFindValue(pValue, pNSymphols, &pLocation);
            lNSymphols.erase(pLocation);
        }
    }
}
//Перезаписаь в map lNSymphols  
void WriteToNumberSympholsMap(map<int, int>::iterator pKeyForGame, map<int, int>::iterator pIteratorForMinElement, map<int, int>* pKey, int lMinElement, map<int, int>* pNSymphols)
{
    int lElementForSwap = pKeyForGame->second;
    pKeyForGame->second = lMinElement;
    pIteratorForMinElement->second = lElementForSwap;
    WriteTo(pKeyForGame, pKey, pNSymphols);
    ReWriting(pKeyForGame, pKey, pNSymphols);
}
//делаем ключ во втором случае 
void ChangerMap(map<int, int>* pUsedNumbers1Element, map<int, int>* pUsedNumbers2Element, map<int, int>* pUsedNumbers3Element, map<int, int>* pKey, map<int, int>::iterator pIteratorForCheckMap, int* pCounterFor1Element, int* pCounterFor2Element, int* pCounterFor3Element)
{
    map<int, int> lNSymphols;
    map<int, int> lNSympholsChecker;
    map<int, int> lNSympholsChecker_2;
    map<int, int> lKey = *pKey;
    map<int, int> lKeyForCheck;
    int lMinElement = 0;
    int lNotMinButMinValue = 0;
    int lElementForSwap = 0;
    map<int, int>::iterator lIteratorForMinElement;
    map<int, int>::iterator lKeyForGame;
    map<int, int>::iterator lKeyForGame2 = pKey->find(2);
    //////////////////////////////////////////////////////////////////////////////////////
    int lMaxElement = 0;
    WriteTo(prev(prev(pIteratorForCheckMap)), pKey, &lNSymphols);
    UsedMaxElements(*pUsedNumbers3Element, lNSymphols, &lMaxElement);
    lKeyForCheck = *pKey;
    ReWriting_Max(next(lKeyForCheck.begin()), &lKeyForCheck, &lNSympholsChecker_2);
    bool lValue_2 = ((pKey->find(3)->second == lNSympholsChecker_2.find(3)->second) && (pKey->find(4)->second == lNSympholsChecker_2.find(4)->second) && (pKey->find(5)->second == lNSympholsChecker_2.find(5)->second));
    lNSymphols.clear();
    if ((pKey->find(3)->second == lMaxElement) && lValue_2)
    {
        pUsedNumbers3Element->clear();
        *pCounterFor3Element = 1;
    }
    //////////////////////////////////////////////////////////////////////////////////////
    WriteTo(prev(pIteratorForCheckMap), pKey, &lNSymphols);
    WriteTo(pKey->begin(), pKey, &lNSympholsChecker);
    ReWriting_Max(pKey->begin(), &lKey, &lNSympholsChecker);
    bool lValue = ((lKeyForGame2->second == lNSympholsChecker.find(lKeyForGame2->first)->second) && (pKey->find(3)->second == lNSympholsChecker.find(3)->second) && (pKey->find(4)->second == lNSympholsChecker.find(4)->second) && (pKey->find(5)->second == lNSympholsChecker.find(5)->second));
    if (lKeyForGame2->second <= 5 && lValue == 0)
    {
        UsedMinElements(*pUsedNumbers3Element, lNSymphols, &lMinElement);
        MapFindValue(lMinElement, *pKey, &lNotMinButMinValue);
        lIteratorForMinElement = pKey->find(lNotMinButMinValue);
        lKeyForGame = prev(pKey->find(lNSymphols.begin()->first));
        lNSymphols.clear();
    }
    else if (lValue)
    {
        if (pKey->find(1)->second == 5)
        {
            pUsedNumbers1Element->clear();
            pUsedNumbers2Element->clear();
            pUsedNumbers3Element->clear();
            lValue = 0;
            return;
        }
        pUsedNumbers3Element->clear();
        *pCounterFor3Element = 1;
        lKeyForGame = next(pKey->begin());
        pUsedNumbers2Element->clear();
        *pCounterFor2Element = 0;
        pUsedNumbers1Element->insert(make_pair(*pCounterFor1Element, pKey->find(1)->second));
        (*pCounterFor1Element)++;
        lNSymphols.clear();
        WriteTo(prev(lKeyForGame), pKey, &lNSymphols);
        UsedMinElements(*pUsedNumbers1Element, lNSymphols, &lMinElement);
        MapFindValue(lMinElement, *pKey, &lNotMinButMinValue);
        lIteratorForMinElement = pKey->find(lNotMinButMinValue);
        lNSymphols.clear();
        WriteToNumberSympholsMap(prev(lKeyForGame), lIteratorForMinElement, pKey, lMinElement, &lNSymphols);
        std::cout << endl;
        OutKey(*pKey);
        lMinElement = 0;
        lValue = 0;
        return;
    }
    if (lKeyForGame->second == lMaxElement)
    {
        pUsedNumbers2Element->insert(make_pair(*pCounterFor2Element, pKey->find(2)->second));
        (*pCounterFor2Element)++;
        WriteTo(prev(prev(pIteratorForCheckMap)), pKey, &lNSymphols);
        UsedMinElements(*pUsedNumbers2Element, lNSymphols, &lMinElement);
        MapFindValue(lMinElement, *pKey, &lNotMinButMinValue);
        lIteratorForMinElement = pKey->find(lNotMinButMinValue);
        lNSymphols.clear();
        WriteToNumberSympholsMap(prev(lKeyForGame), lIteratorForMinElement, pKey, lMinElement, &lNSymphols);
    }
    else
    {
        WriteToNumberSympholsMap(lKeyForGame, lIteratorForMinElement, pKey, lMinElement, &lNSymphols);
        if (lKeyForGame->second == lMaxElement)
        {
            pUsedNumbers2Element->insert(make_pair(*pCounterFor2Element, pKey->find(2)->second));
            (*pCounterFor2Element)++;
        }
    }
    lNSymphols.clear();
    OutKey(*pKey);
    lMinElement = 0;
}
//получение всех ключей что у нас эсть возможны
void GettingKeys(map<int, map<int, int>>* pAllKeys)
{
    map<int, int> lKey;
    map<int, int> lUsedNumbers1Element;
    map<int, int> lUsedNumbers2Element;
    map<int, int> lUsedNumbers3Element;
    StartMap(&lKey);
    pAllKeys->insert(make_pair(1, lKey));
    map<int, int>::iterator lKeyIterator = lKey.begin();
    map<int, int>::iterator lKeyIteratorEnd = prev(lKey.end());
    int lValue1 = 0, lValue2 = 0;
    int lCounterFor1Element = 0;
    int lCounterFor2Element = 1;
    int lCounterFor3Element = 1;
    for (int i = 2; i <= 120; i++)
    {
        if (lKeyIteratorEnd->second > std::prev(lKeyIteratorEnd)->second)
        {
            lValue1 = lKeyIteratorEnd->second;
            lValue2 = std::prev(lKeyIteratorEnd)->second;
            lKeyIteratorEnd->second = lValue2;
            std::prev(lKeyIteratorEnd)->second = lValue1;
            OutKey(lKey);
        }
        else if (lKeyIteratorEnd->second < std::prev(lKeyIteratorEnd)->second)
        {
            lUsedNumbers3Element.insert(make_pair(lCounterFor3Element, lKey.find(3)->second));
            lCounterFor3Element++;
            ChangerMap(&lUsedNumbers1Element, &lUsedNumbers2Element, &lUsedNumbers3Element, &lKey, prev(lKeyIteratorEnd), &lCounterFor1Element, &lCounterFor2Element, &lCounterFor3Element);
        }
        pAllKeys->insert(make_pair(i, lKey));
    }
}