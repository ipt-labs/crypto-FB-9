#pragma once
#include "BigNumbers.h"
#include <map>
#include <iterator>
/////
string DEC_TO_BIN(big_integer chislo);
big_integer HEX_TO_DEC(string st);
string DEC_TO_HEX(big_integer Dec);
map<map<int, big_integer>, big_integer> GCD(big_integer pFirstValue, big_integer pSecondValue);
big_integer ReverseNumber(big_integer pValue, big_integer pMod, map<map<int, big_integer>, big_integer> lResultForGcd);
///////////

