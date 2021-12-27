#include <string>
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

using namespace std;

//ñîçäàíèÿ íà÷àëüíîãî map
void StartMap(map<int, int>* pKey);
//ðàñïîëîæåíèå åëåìåíòîâ â ïîðÿäêå ñïàäàíèÿ è çàïèñü â êëþ÷
void ArrangeNumbersInAscendingOrder(map<int, int>* pConstKey, map<int, int>* pKey);
//ðàñïîëîæåíèå åëåìåíòîâ â ïîðÿäêå ñïàäàíèÿ è çàïèñü â êëþ÷
void ArrangeNumbersInDescendingOrder(map<int, int>* pConstKey, map<int, int>* pKey);
//âûâîäèò êëþ÷è
void OutKey(map<int, int> pKey);
//çàïèñü â ìàï ñ îïðåäåëåííîãî åëåìåíòà äî êîíöà
void WriteTo(map<int, int>::iterator pIterator, map<int, int>* pMap, map<int, int>* pNSymphols);
//ïåðåçàïèñü êëþ÷à â ïîðÿäêå ñïàäàíèÿ
void ReWriting(map<int, int>::iterator pKeyForGame, map<int, int>* pKey, map<int, int>* pNSymphols);
//ïåðåçàïèñü êëþ÷à â ïîðÿäêå âîçðàñòàíèÿ
void ReWriting_Max(map<int, int>::iterator pKeyForGame, map<int, int>* pKey, map<int, int>* pNSymphols);
//ïîèñê ïî çíà÷åíèþ â ìàïå
void MapFindValue(int pValue, map<int, int> pMap, int* pLocation);
//ïðîâåðêà íà èñïîëüçûâàíûé åëåìåíòè ïîèñê ìèíèìàëüíîãî
void UsedMinElements(map<int, int> pUsedNumbers, map<int, int> pNSymphols, int* pMinElement);
//ïðîâåðêà íà èñïîëüçûâàíûé åëåìåíò è ïîèñê ìàêñèìàëüíîãî
void UsedMaxElements(map<int, int> pUsedNumbers, map<int, int> pNSymphols, int* pMaxElement);
//Ïåðåçàïèñàü â map lNSymphols  
void WriteToNumberSympholsMap(map<int, int>::iterator pKeyForGame, map<int, int>::iterator pIteratorForMinElement, map<int, int>* pKey, int lMinElement, map<int, int>* pNSymphols);
//äåëàåì êëþ÷ âî âòîðîì ñëó÷àå 
void ChangerMap(map<int, int>* pUsedNumbers1Element, map<int, int>* pUsedNumbers2Element, map<int, int>* pUsedNumbers3Element, map<int, int>* pKey, map<int, int>::iterator pIteratorForCheckMap, int* pCounterFor1Element, int* pCounterFor2Element, int* pCounterFor3Element);
//ïîëó÷åíèå âñåõ êëþ÷åé ÷òî ó íàñ ýñòü âîçìîæíû
void GettingKeys(map<int, map<int, int>>* pAllKeys);
