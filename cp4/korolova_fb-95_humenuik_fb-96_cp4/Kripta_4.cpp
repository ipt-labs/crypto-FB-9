// Kripta_4.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include <chrono>
#include <windows.h>
#include "Mathematic.h"


//переводим число в двоичную систему исчисления
map<int, big_integer> DecBin(big_integer chislo, big_integer size)
{
	map<int, big_integer> bin;
	string Bin = "";
	int k = 0, n = 0;
	big_integer lCounter = 0, t, lchislo = chislo;
	while (lchislo > 0)
	{
		t = lchislo % 2;
		k = n;
		bin.insert(make_pair(k, t));
		n += 1;
		lchislo = lchislo / 2;
	}
	return bin;
}
//! Вычисляет a^k (mod n)
big_integer Horner(big_integer a, big_integer k, const big_integer& n)
{
	big_integer  res = 1, lSize(sizeof(k) * 8);
	map<int, big_integer> lBin = DecBin(k, lSize);
	for (map<int, big_integer>::iterator lIterator = prev(lBin.end()); lIterator != lBin.end(); lIterator = prev(lIterator))
	{
		big_integer ldegree = a.pow(lIterator->second);
		res = res * ldegree % n;
		if (prev(lIterator) != lBin.end()) { res = res.pow(2); }
		res = res % n;
	}
	return res;
}
//Производится k раундов проверки числа n на простоту
bool MillerRabinTest(big_integer p, int k)
{
	if (p % 2 == 0)return false;
	if (p % 3 == 0 || p % 5 == 0 || p % 7 == 0 || p % 13 == 0 || p % 17 == 0 || p % 19 == 0)
		return false;
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	big_integer d = p - 1, s = 0;
	while (d % 2 == 0)
	{
		d /= 2;
		s += 1;
	}
	///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	for (int i = 0; i < k; i++)// повторяем k раз
	{
		big_integer x = 1 + rand() % (p - 1);
		for (map<map<int, big_integer>, big_integer> lResultForGcd = GCD(x, p); lResultForGcd.begin()->second != 1; ++x)
			return false;
		bool isProstoe = false;
		//cout << x << endl;
		big_integer res = Horner(x, d, p);
		if (res == 1) isProstoe = true;

		for (int r = 0; r < s; r++)// повторить s − 1 раз
		{
			int lPow = pow(2, r);  // x ← x^2 mod n
			res = Horner(x, d * lPow, p);
			if (res == p - 1) isProstoe = true;
		}
		if (!isProstoe) return false;
		else return true;
	}
	return true;
}
//находим рандомное простое число
big_integer FindRandSimpleNumber(big_integer pLeftLimit, big_integer pRightLimit)
{
	//srand(time(NULL)); // это делается только ОДИН раз в начале работы
	big_integer random = 0;
	do
	{
		random = (rand() % pLeftLimit / 2 + pRightLimit / 2) * 2 + 1; // случайное число в диапазоне от 2^255 до 2^256-1
		cout << random << endl;
	} while (!MillerRabinTest(random, 4));
	cout << random << endl << "Prostoe" << endl;
	return random;
}
//Получаем P i Q для Аліси і Біба
map<string, map<string, big_integer>> PandQ(map<int, big_integer> RandSimpleValue)
{
	map<string, map<string, big_integer>> PandQ;
	if (RandSimpleValue.find(1)->second * RandSimpleValue.find(2)->second > RandSimpleValue.find(3)->second * RandSimpleValue.find(4)->second)
	{
		map<string, big_integer> lmap;
		lmap.insert(make_pair("p", RandSimpleValue.find(1)->second));
		lmap.insert(make_pair("q", RandSimpleValue.find(2)->second));
		PandQ.insert(make_pair("B", lmap)); lmap.clear();
		lmap.insert(make_pair("p", RandSimpleValue.find(3)->second));
		lmap.insert(make_pair("q", RandSimpleValue.find(4)->second));
		PandQ.insert(make_pair("A", lmap)); lmap.clear();
		return PandQ;
	}
	else
	{
		map<string, big_integer> lmap;
		lmap.insert(make_pair("p", RandSimpleValue.find(3)->second));
		lmap.insert(make_pair("q", RandSimpleValue.find(4)->second));
		PandQ.insert(make_pair("B", lmap)); lmap.clear();
		lmap.insert(make_pair("p", RandSimpleValue.find(1)->second));
		lmap.insert(make_pair("q", RandSimpleValue.find(2)->second));
		PandQ.insert(make_pair("A", lmap)); lmap.clear();
		return PandQ;
	}
}
//Находимо цифровий підпис за РСА - S = ((M^d)(mod(n))
big_integer DigitalSignatureRSA(big_integer DecipherText, big_integer D, big_integer N)
{
	big_integer S = Horner(DecipherText, D, N);
	return S;
}
//Шифруєм текст за РСА - C = ((M^e)(mod(n))
big_integer CipherTextRSA(big_integer DecipherText, big_integer E, big_integer N)
{
	big_integer C = Horner(DecipherText, E, N);
	return C;
}
//Дешифруєм текст за РСА - M = ((C^d)(mod(n)) 
big_integer GetM(big_integer CipherText, big_integer D, big_integer N)
{
	big_integer M = Horner(CipherText, D, N);
	return M;
}
bool Check_Signature(big_integer M, big_integer S, big_integer E, big_integer N)
{
	big_integer lM = Horner(S, E, N);
	cout << "Dec:"<<lM << endl;
	if (lM == M) return 1;
	else return 0;
}
//Находим д и е по алгоритму РСА
map<big_integer, big_integer> Find_D_And_E(big_integer p, big_integer q)
{
	big_integer Phi = (p - 1) * (q - 1);
	for (;;)
	{
		big_integer e("7849449506493312711129561415324524125992486842778339457741484350474842986835952529599938858691733011284688088033961594091469025745492687971667759715244529") /*= (rand() % 1 + (n-1) / 2) * 2 + 1*/; // случайное число в диапазоне от 2^255 до 2^256-1
		//cout << "Generating .....\n" << e << endl;
		map<map<int, big_integer>, big_integer> lResultForGcd = GCD(Phi, e);
		if (lResultForGcd.begin()->second == 1)
		{
			map<map<int, big_integer>, big_integer> lResultForGcd = GCD(Phi, e);
			big_integer d = ReverseNumber(e, Phi, lResultForGcd);
			//cout << "Модуль:\n" << Phi;
			//cout << "\nЧисло:\n" << e;
			//cout << "\nОбернене число:\n" << d;
			map<big_integer, big_integer> lDandE;
			lDandE.insert(make_pair(d, e));
			return lDandE;
		}
	}
}

///////////////////////////////////////////////////////////////////////////////////////////
void RSAKeys()
{
	big_integer l2("2"), LeftLimit = l2.pow(255), RightLimit = l2.pow(256) - 1;
	cout << LeftLimit << endl << RightLimit << endl;
	map<int, big_integer> RandSimpleValue;
	//auto begin = std::chrono::steady_clock::now();
	//while (RandSimpleValue.size() < 4)
	//{
	//	big_integer lRandSimleNumder = FindRandSimpleNumber(LeftLimit, RightLimit);
	//	if (RandSimpleValue.size() == 0) RandSimpleValue.insert(make_pair(1, lRandSimleNumder));
	//	else RandSimpleValue.insert(make_pair(prev(RandSimpleValue.end())->first + 1, lRandSimleNumder));
	//}
	//auto end = std::chrono::steady_clock::now();
	//auto elapsed_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - begin);
	//std::cout << "The time: " << elapsed_ms.count() << " ms\n";
	RandSimpleValue.insert(make_pair(1, "90537879588897465387133326884708486476041471186471324048449300458247492416481"));
	RandSimpleValue.insert(make_pair(2, "86150101796519139448559302808615911065040892953424399390382754402822117919089"));
	RandSimpleValue.insert(make_pair(3, "106308541180546410139254735352647313870913193670710452235270933900888536235361"));
	RandSimpleValue.insert(make_pair(4, "78603014483957224374389812927464060860199976595920782564577255051874782387819"));
	map<string, map<string, big_integer>> lPandQ = PandQ(RandSimpleValue);
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
	//Получаем н для а 
	cout << endl << "For Alice" << endl;
	big_integer nA = (lPandQ.begin()->second.begin()->second) * (next(lPandQ.begin()->second.begin())->second);
	cout << "Private key!" << endl;
	map<big_integer, big_integer> dA = Find_D_And_E((lPandQ.begin()->second.begin()->second), (next(lPandQ.begin()->second.begin())->second));
	cout << (lPandQ.begin()->second.begin()->first) << ":\t" << (lPandQ.begin()->second.begin()->second) << endl;
	cout << (next(lPandQ.begin()->second.begin())->first) << ":\t" << (next(lPandQ.begin()->second.begin())->second) << endl;
	cout << "d:" << "\t" << dA.begin()->first << endl;
	cout << "Public key!" << endl;
	cout << "n:\t" << nA << endl;
	cout << "e:\t" << dA.begin()->second << endl;
	//Получаем н для б
	cout << endl << "For Biba" << endl;
	big_integer nB = (next(lPandQ.begin())->second.begin()->second) * (next(next(lPandQ.begin())->second.begin())->second);
	cout << "Private key!" << endl;
	map<big_integer, big_integer> dB = Find_D_And_E((next(lPandQ.begin())->second.begin()->second), (next(next(lPandQ.begin())->second.begin())->second));
	cout  << (next(lPandQ.begin())->second.begin()->first) << ":\t" << (next(lPandQ.begin())->second.begin()->second) << endl;
	cout << (next(next(lPandQ.begin())->second.begin())->first) << ":\t" << (next(next(lPandQ.begin())->second.begin())->second);
	cout << endl << "d:" << "\t" << dB.begin()->first << endl;
	cout << "Public key!" << endl;
	cout << "n:\t" << nB << endl;
	cout << "e:\t" << dB.begin()->second << endl << endl;
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
	cout << "Biba send Alice messege!\n";
	string Messege;
	cout << "Enter messege Hex:\n";
	cin >> Messege;
	big_integer DecipherText = HEX_TO_DEC(Messege);
	//Шифруєм текст за РСА - C = ((M^e)(mod(n))
	big_integer CipherText = CipherTextRSA( DecipherText, dB.begin()->second, nB);
	cout << "Entcripted text:\n" << CipherText << endl;
	//Дешифруєм текст за РСА - M = ((C^d)(mod(n)) 
	big_integer M = GetM(DecipherText, dA.begin()->first, nA);
	cout << "M:\n" << M << endl;
	//Находимо цифровий підпис за РСА - S = ((M^d)(mod(n))
	big_integer S = DigitalSignatureRSA(M, dB.begin()->first, nB);
	cout << "S:\n" << S << endl << endl;
	//Результат проверки
	bool Check_Signatur = Check_Signature( M,  S, dB.begin()->second, nB);
	cout << "Результат проверки сигнатур: "<< Check_Signatur << endl;
	//Дешифруєм текст за РСА - M = ((C^d)(mod(n)) 
	big_integer DText = GetM(CipherText, dB.begin()->first, nB);
	string HEX = DEC_TO_HEX(DText);
	cout << "Decripted text Dec:\n" << DText << endl;
	cout << "Decripted text Hex:\n" << HEX << endl;
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
}
///////////////////////////////////////////////////////////////////////////////////////////
void RSADecipher()
{
	string lN = "", ld = "", Messege = "";
	cout << "Введите n:\n";
	cin >> lN;
	cout << "Введите d:\n";
	cin >> ld;
	cout << "Enter cipher messege in Hex:\n";
	cin >> Messege;
	big_integer MessegeHEX = HEX_TO_DEC(Messege);
	cout << "Dec:" << MessegeHEX << endl;
	big_integer N = HEX_TO_DEC(lN);
	big_integer D = HEX_TO_DEC(ld);
	//Дешифруєм текст за РСА - M = ((C^d)(mod(n)) 
	big_integer DText = GetM(MessegeHEX, D, N);
	string HEXCipherText = DEC_TO_HEX(DText);
	cout << "Decripted text:\n" << DText << endl;
	cout << "Decripted Hex text:\n" << HEXCipherText << endl;
}
void RSACipher()
{	
	string lN = "", lE = "", Messege = "";
	cout << "Введите n:\n";
	cin >> lN;
	cout << "Введите e:\n";
	cin >> lE;
	cout << "Enter messege in Hex:\n";
	cin >> Messege;
	big_integer DEC = HEX_TO_DEC(Messege);
	big_integer N = HEX_TO_DEC(lN);
	big_integer E = HEX_TO_DEC(lE);
	//Шифруєм текст за РСА - C = ((M^e)(mod(n))
	big_integer CipherText = CipherTextRSA(DEC, E, N);
	string HEXCipherText = DEC_TO_HEX(CipherText);
	cout << "Entcripted text:\n" << CipherText << endl;
	cout << "Entcripted Hex text:\n" << HEXCipherText << endl;
}
void RSASignature()
{
	string lS = "", lN = "", lE = "", Messege = "";
	cout << "Введите сообщение:\n";
	cin >> Messege;
	cout << "Введите сигнатуру(s):\n";
	cin >> lS;
	cout << "Введите модуль(n):\n";
	cin >> lN;
	cout << "Введите е:\n";
	cin >> lE;
	big_integer M = HEX_TO_DEC(Messege);
	big_integer S = HEX_TO_DEC(lS);
	big_integer N = HEX_TO_DEC(lN);
	big_integer E = HEX_TO_DEC(lE);
	//Результат проверки
	bool Check_Signatur = Check_Signature(M, S, E, N);
	cout << "Результат проверки сигнатур: " << Check_Signatur << endl;
}
int main()
{
	SetConsoleCP(1251);// установка кодовой страницы win-cp 1251 в поток ввода
	SetConsoleOutputCP(1251); // установка кодовой страницы win-cp 1251 в поток вывод
	system("color 0A");// устанливаем цвет нашей консольки(а почему бы и нет?))
	setlocale(LC_ALL, "ru");//подключаем русский язык 
	//RSACipher();
	//RSADecipher();
	//RSASignature();
	RSAKeys();
}


