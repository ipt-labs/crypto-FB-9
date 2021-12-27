#include<algorithm>
#include <fstream>
#include <iostream>
#include<string>
#include<windows.h>
#include <stdio.h>
#include <string.h>
#include <cstring>
using namespace std;

const char alfabet[] = { 'а', 'б','в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к',
						 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
						'ц','ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', ' ' };
const int alfSize = 34;

void tolow()
{
	ifstream fin;
	ofstream fout;
	fin.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\text.txt");
	fout.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\sorttext.txt");
	char text;
	char tolow;
			while (fin.get(text))
			{
				tolow = tolower(text);
				fout << tolow;

			}
	fin.close();
	fout.close();
}
void regSymbol() 
{
	ifstream fin;
	ofstream fout;
	char text;
	fin.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\sorttext.txt");
	fout.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\filteredtext.txt");
	while (fin.get(text))
	{
		for (int i = 0; i < alfSize; i++)
		{
			if (text == alfabet[i])
			{
				if (text == 'ё')
				{
					fout << 'е';
				}
				else
				{
					fout << text;
				}
			}
		}
	}

	fin.close();
	fout.close();
}

void textSpace()
{
	ifstream fin;
	ofstream fout;
	fin.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\filteredtext.txt");
	fout.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\spacetext.txt");
	int probelCounts = 0;
	char text;
	char probel = ' ';
	while (fin.get(text))
	{
		if (text == probel)
		{
			probelCounts++;
		}
		else
		{
			probelCounts = 0;

		}
		if (probelCounts < 2)
		{
			fout << text;
		}
	}
	fin.close();
	fout.close();
}
void NotSpaceText()
{
	ifstream fin;
	ofstream fout;
	fin.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\spacetext.txt");
	fout.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\Notspacetext.txt");
	int probelCounts = 0;
	char text;
	char probel = ' ';
	while (fin.get(text))
	{
		if (text != probel)
		{
		
			fout << text;
		}
	}
	fin.close();
	fout.close();
}
void frequencyLettersWithSpace()
{
	cout << endl << "frequencyLettersWithSpace" << endl << endl;
	const char alphabet[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
						  'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
						  'ц','ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я', ' ' };
	char text;
	char text1;
	double numbers = 0;
	
	int alfsize = 32;
	ifstream fin;
	ofstream fout;
	fin.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\spacetext.txt");

	while (fin.get() != EOF)
	{
		numbers++;
	}
	fin.close();
	
	for (int i = 0; i < alfsize; i++)
	{
		fin.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\spacetext.txt");
		double letters = 0;
		double frequency = 0;
			while (fin.get(text1))
			{
				if (text1 == alphabet[i])
				{
					letters++;
				}
			}
			frequency = (letters) / (numbers);
			cout << alphabet[i] << "  " << letters << "       " << frequency << endl;
		
		fin.close();
	}
}

void frequencyLettersWithoutSpace()
{
	cout << endl << "frequencyLettersWithoutSpace" << endl<<endl;
	const char alphabet[] = { 'а', 'б','в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к',
						  'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
						  'ц','ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я' };
	char text;
	char text1;
	double numbers = 0;
	
	int alfsize = 31;
	ifstream fin;
	ofstream fout;
	fin.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\Notspacetext.txt");

	while (fin.get() != EOF)
	{
		numbers++;
	}
	fin.close();

	for (int i = 0; i < alfsize; i++)
	{
		fin.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\Notspacetext.txt");
		double letters = 0;
		double frequency = 0;
		while (fin.get(text1))
		{
			if (text1 == alphabet[i])
			{
				letters++;
			}
		}
		frequency = (letters) / (numbers);
		cout << alphabet[i] << " --- " << letters << "         " << frequency << endl;

		fin.close();
	}
}

void spaceBigram()
{
	
	const char alphabet[] = "абвгдежзийклмнопрстуфхцчшщыьэюя ";
	const int len = (sizeof(alphabet) - 1);
	int bigrams = 0;
	double k = 0;
	char* point0 = NULL;
	int text;
	int counts[len][len];
	FILE* result;
	ofstream fout;
	fout.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\spaceBigram.txt");
	fopen_s(&result, "B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\spacetext.txt", "r");
	memset(counts, 0, sizeof(counts));

		while ((text = getc(result)) != EOF) {
			char* point1 = (char*)memchr(alphabet, text, len);
			if (point1 != NULL && point0 != NULL) {
				counts[point0 - alphabet][point1 - alphabet]++;
				k++;
			}
			point0 = point1;
		}
		fclose(result);
		for (size_t i = 0; i < len; i++) {
			for (size_t j = 0; j < len; j++) {
				double num = counts[i][j];
				if (num > 0) {
					bigrams++;
				}
			}
		}
		cout <<endl<< "Bigram counts = " << bigrams << endl;
		for (size_t i = 0; i < len; i++) {
			for (size_t j = 0; j < len; j++) {
				double num = counts[i][j];
				if (num > 0) {
					fout << "" << alphabet[i] << "" << alphabet[j] << "     " << num << "      " << num / k << endl;
				}
			}
		}
	
}
void notSpaceBigram()
{
	const char alphabet[] = "абвгдежзийклмнопрстуфхцчшщыьэюя";
	const int len = (sizeof(alphabet) - 1);
	int bigrams = 0;
	double k = 0;
	char* p0 = NULL;
	int text;
	int counts[len][len];
	FILE* result;
	ofstream fout;
	fout.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\NotSpaceBigram.txt");
	fopen_s(&result, "B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\Notspacetext.txt", "r");
	memset(counts, 0, sizeof(counts));

		while ((text = getc(result)) != EOF) {
			char* p1 = (char*)memchr(alphabet, text, len);
			if (p1 != NULL && p0 != NULL) {
				counts[p0 - alphabet][p1 - alphabet]++;
				k++;
			}
			p0 = p1;
		}
		fclose(result);
		for (size_t i = 0; i < len; i++) {
			for (size_t j = 0; j < len; j++) {
				double num = counts[i][j];
				if (num > 0) {
					bigrams++;
				}
			}
		}
		cout <<endl<< "Bigram counts = " << bigrams << endl;
		for (size_t i = 0; i < len; i++) {
			for (size_t j = 0; j < len; j++) {
				double num = counts[i][j];
				if (num > 0) {
					fout << "" << alphabet[i] << "" << alphabet[j] << "    " << num << "      " << num / k << endl;
				}
			}
		}
	
}
void BcrossSpace()
{
	const char alphabet[] = "абвгдежзийклмнопрстуфхцчшщыьэюя";
	const int len = (sizeof(alphabet) - 1);
	int bigrams = 0;
	double k = 0;
	char* point0 = NULL;
	int text;
	int counts[len][len];
	FILE* result;
	ofstream fout;
	fout.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\BcrossSpace.txt");
	fopen_s(&result, "B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\spacetext.txt", "r");
	memset(counts, 0, sizeof(counts));
	int s = 0;
	
		while ((text = getc(result)) != EOF) {
			char* point1 = (char*)memchr(alphabet, text, len);
			if (point1 != NULL && point0 != NULL) {
				if (s == 0)
				{
					counts[point0 - alphabet][point1 - alphabet]++;
					k++;
					s++;
				}
				else if (s == 1)
				{
					s = 0;
				}
			}
			point0 = point1;
		}
		fclose(result);
		for (size_t i = 0; i < len; i++) {
			for (size_t j = 0; j < len; j++) {
				double num = counts[i][j];
				if (num > 0) {
					bigrams++;
				}
			}
		}
		cout <<endl<< "Bigram counts = " << bigrams << endl;
		for (size_t i = 0; i < len; i++) {
			for (size_t j = 0; j < len; j++) {
				double num = counts[i][j];
				if (num > 0) {
					fout << "" << alphabet[i] << "" << alphabet[j] << " - " << num << "   " << num / k << endl;
				}
			}
		}
	
}
void BcrossNotspace()
{
	const char alphabet[] = "абвгдежзийклмнопрстуфхцчшщыьэюя ";
	const int len = (sizeof(alphabet) - 1);
	int bigrams = 0;
	double k = 0;
	char* point0 = NULL;
	int text;
	int counts[len][len];
	FILE* result;
	ofstream fout;
	int s = 0;
	fout.open("B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\BnotcrossNotSpace.txt");
	fopen_s(&result, "B:\\VisualStudio\\Projects\\cryptoLab1\\cryptoLab1\\Notspacetext.txt", "r");
	memset(counts, 0, sizeof(counts));
	

	while ((text = getc(result)) != EOF) {
		char* point1 = (char*)memchr(alphabet, text, len);
		if (point1 != NULL && point0 != NULL) {
			if (s == 0)
			{
				counts[point0 - alphabet][point1 - alphabet]++;
				k++;
				s++;
			}
			else if (s == 1)
			{
				s = 0;
			}
		}
		point0 = point1;
	}
	fclose(result);
	for (size_t i = 0; i < len; i++) {
		for (size_t j = 0; j < len; j++) {
			double num = counts[i][j];
			if (num > 0) {
				bigrams++;
			}
		}
	}
	cout <<endl<< "Bigram counts = " << bigrams << endl;
	for (size_t i = 0; i < len; i++) {
		for (size_t j = 0; j < len; j++) {
			double num = counts[i][j];
			if (num > 0) {
				fout << "" << alphabet[i] << "" << alphabet[j] << " - " << num << "   " << num / k << endl;
			}
		}
	}
}
int main()
{
	setlocale(LC_ALL, "Russian");
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	
	tolow();
	regSymbol();
	textSpace();
	NotSpaceText();
	frequencyLettersWithSpace();
	frequencyLettersWithoutSpace();
	spaceBigram();
	notSpaceBigram();
	BcrossSpace();
	BcrossNotspace();
}
