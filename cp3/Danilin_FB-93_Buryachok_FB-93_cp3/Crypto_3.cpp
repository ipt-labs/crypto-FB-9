#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <stack>
#include <set>
#define max_module 961
#define permutation_size 5

using namespace std;

pair<vector<int>, int> gcd(int a, int b)
{
	vector<int> q;
	
	while (a > 0 && b > 0)
	{
		if (a > b)
		{
			q.push_back(a / b);
			
			a %= b;
		}

		else
		{
			q.push_back(b / a);
			
			b %= a;
		}
	}
	
	return make_pair(q, a + b);
}



struct Number
{
	int value, mod;

	Number(int value, int mod)
	{
		while (value < 0)
		{
			value += mod;
		}
		
		this->value = value % mod;
		this->mod = mod;
	}

	Number(const Number& number)
	{
		this->value = number.value;
		this->mod = number.mod;
	}

	Number operator+(const Number& number)
	{
		if (this->mod != number.mod)
		{
			throw exception("mods not equal");
		}

		return Number((this->value + number.value) % this->mod, this->mod);
	}

	Number operator-(const Number& number)
	{
		if (this->mod != number.mod)
		{
			throw exception("mods not equal");
		}

		return Number((this->value - number.value) % this->mod, this->mod);
	}

	Number operator*(const Number& number)
	{
		if (this->mod != number.mod)
		{
			throw exception("mods not equal");
		}

		return Number((this->value * number.value) % this->mod, this->mod);
	}

	Number reverse()
	{
		pair<vector<int>, int> q = gcd(this->value, this->mod);

		if (q.second != 1)
		{
			throw exception("gcd not equal to 1");
		}
		
		vector<Number> result;

		result.push_back(Number(0, this->mod));
		result.push_back(Number(1, this->mod));

		for (int i = 0; i < q.first.size(); i++)
		{
			result.push_back((Number(-q.first[i], this->mod) * result[i + 1]) + result[i]);
		}

		return result[q.first.size()];
	}
};

vector<Number> linear_equation(int first, int second, int mod)
{
	pair<vector<int>, int> res = gcd(first, mod);

	if (res.second == 1)
	{
		Number a(first, mod), b(second, mod);

		vector<Number> result;

		result.push_back(a.reverse() * b);
		
		return result;
	}

	if (second % res.second > 0)
	{
		return vector<Number>();
	}

	int d = res.second;

	Number a(first / d, mod / d), b(second / d, mod / d);

	Number x0 = a.reverse() * b;

	vector<Number> result;

	for (int i = 0; i < d; i++)
	{
		result.push_back(Number(x0.value + i * mod / d, mod));
	}

	return result;
}

int char_to_int(char c)
{
	return c < -6 ? c + 32 : c - 1 + 32;
}

string int_to_char(int n)
{
	string c;

	c += n < 26 ? char(n - 32) : char(n + 1 - 32);
	
	return c;
}

int bigram_to_int(const string& bigram)
{
	return 31 * char_to_int(bigram[0]) + char_to_int(bigram[1]);
}

string int_to_bigram(int n)
{
	return int_to_char(n / 31) + int_to_char(n % 31);
}

pair<int, int> get_key(const string& text1, const string& text2, const string& cipher1, const string& cipher2)
{
	int x1 = bigram_to_int(text1);
	int x2 = bigram_to_int(text2);

	int y1 = bigram_to_int(cipher1);
	int y2 = bigram_to_int(cipher2);

	vector<Number> a = linear_equation(x1 - x2, y1 - y2, max_module);

	if (a.size() == 1)
	{
		Number b(y1 - a[0].value * x1, max_module);

		return make_pair(a[0].value, b.value);
	}
}

void all_permutations(int childs, array<bool, permutation_size>& denies, stack<int>& values, vector<array<int, permutation_size>>& permutations)
{
	if (childs != 0)
	{
		for (int i = 0; i < childs; i++)
		{
			int index = 0, k = 0;

			for (int j = 0; j < permutation_size; j++)
			{
				if (!denies[j])
				{
					if (k == i)
					{
						index = j;
						break;
					}

					k++;
				}
			}

			denies[index] = true;

			values.push(index);

			all_permutations(childs - 1, denies, values, permutations);

			values.pop();

			denies[index] = false;
		}
	}

	else
	{
		array<int, permutation_size> to_push;

		for (int i = 0; i < permutation_size; i++)
		{
			to_push[permutation_size - 1 - i] = values.top();

			values.pop();
		}

		for (int i = 0; i < permutation_size; i++)
		{
			values.push(to_push[i]);
		}

		permutations.push_back(to_push);
	}
}

string decode(string cipher, int key_a, int key_b)
{
	string text;
	
	Number a_reverse = Number(key_a, max_module).reverse();
	Number b(key_b, max_module);

	for (int i = 0; i < cipher.length(); i += 2)
	{
		int y = bigram_to_int(cipher.substr(i, 2));

		int x = ((Number(y, max_module) - b) * a_reverse).value;

		text += int_to_bigram(x);
	}

	return text;
}

int main()
{
	setlocale(LC_ALL, "Ru");

	//part 2
	
	string text_bigrams[] = { "то", "ен", "но", "на", "ст" };
	string cipher_bigrams[] = { "йа", "юа", "чш", "юд", "рщ" };

	//part 3

	string text1;
	string text2;

	string cipher1;
	string cipher2;

	array<bool, permutation_size> denies = { false };

	stack<int> values;

	vector<array<int, permutation_size>> permutations;

	all_permutations(permutation_size, denies, values, permutations);

	ofstream fout;

	fout.open("permutations.txt");

	set<pair<int, int>> all_keys;

	for (int i = 0; i < permutations.size(); i++)
	{
		fout << "Permutation #" << i + 1 << endl;

		for (int j = 0; j < permutation_size; j++)
		{
			fout << permutations[i][j] << " ";
		}

		fout << endl;

		for (int j = 0; j < permutation_size; j++)
		{
			fout << text_bigrams[j] << " ";
		}

		fout << endl;

		for (int j = 0; j < permutation_size; j++)
		{
			fout << cipher_bigrams[permutations[i][j]] << " ";
		}

		fout << endl;

		int a = -1, b = -1, k = 0;

		for (int j = 0; j < permutation_size - 1; j++)
		{
			text1 = text_bigrams[j];
			text2 = text_bigrams[j + 1];

			cipher1 = cipher_bigrams[permutations[i][j]];
			cipher2 = cipher_bigrams[permutations[i][j + 1]];

			fout << text1 << " -> " << cipher1 << "\t" << text2 << " -> " << cipher2 << endl;

			pair<int, int> key = get_key(text1, text2, cipher1, cipher2);

			fout << "a = " << key.first << "\tb = " << key.second << endl;

			if (gcd(key.first, max_module).second == 1)
			{
				all_keys.emplace(key);
			}

			if (j == 0)
			{
				a = key.first;
				b = key.second;
			}

			if (a == key.first && b == key.second)
			{
				k++;
			}
		}

		fout << "Count = " << k << endl;

		fout << endl;
	}

	fout.close();

	//part 4

	fout.open("keys.txt");

	for (auto key = all_keys.begin(); key != all_keys.end(); ++key)
	{
		fout << key->first << "\t" << key->second << endl;
	}

	fout.close();

	//decode

	pair<int, int> key(27, 211);

	string cipher = "рйрщкагппрфчгшрщйрпрффькрпьчшдвиыеюдучхулицплшющашдщныскющвпьюкджьйахещыйеьеюеэдсецчтыкйдшцчзюимевжшбушччэканылшолшкющчшэизупмзсбвжшбуойщаищмдпнрйуюфшхдтылшларюдезанпрбкажлащваэщюемечшщипнипнучбусхекайаэкяуклзщюгхегарпинцплппрффзшскыушщммеючогалчцпдшяуыуйацднфзхащаукйнхжукчщысаэарюжштнцмосхрхлтечшишваллмппртелиюдьпкуурдщерритыачтахщышкаюйзхцмздффнагещцлерьюбокцезацчучрйяыыунлсрорпрькрщэарючолаимхугшзепутэрщбероюазанхзушщимзсбючолаштэиэщюхжукчтдюагпшдормэрмыупьфуйабеюемдвитылшошрщышгпфуыуйацдаюваллйыачларщзщроюалахдорцпиыщылшошрщйьфуйазлиекдвифущлбшашваллюсхщрохеццэирщэаэшуоьюдэисфуриыугшэпзлиекдкглаедюднфэщйдшгфчпрбердрйуюпнсабдпннхцмрцсдрпющкммьлеешбпымюенпчщроюабучштечшюдушлсбубеюыхрдщндщфщейерйсдкммьофкаюйажйаидхйьнхерщхлкшьсжуиеишбпымюенпчщроюаеймюбероюарпинымжизаропйхлбшбуклзщзсэпюаиечшорэпьчкгипгекбхщжачойатеащваюдюдкйчбйкпмтырйюенщлучихечшчрпрфуклзщрусипнрйыуйаусйрпнцмшяхукчкйбвжшлжпшюечукемипнипцчушлсрйхпэснезщжмюдкенлхарпсдхйьчмэешйарпхппрэщцжыщпаюехдпьхуйанацчрбюдхушчкацкдщтеэдвиййтагшфичиорхлфдщфкшышвамносвиййдзьрыщышхемсующудршджьюанхрэцпымздффнарписюахьхууочрфчгшйкпаюехдсджжгшцчтыкйдшнануэифуларизсййушфиюдюдаюышькющяпцлдчьншгашэлашьухаедвизлиекдвидщлсхпкеышйрьчценавсачэаькудбюяхцмрцсдрпгекммьлекдхйыуыщйаудюлцчисуюэиффриещжзьргшкдыууоьдглэшешбероюачпщылшыщдшэасуйаьпымкуюсщгхелафитбюазуыщюаешуоналаолфдыууозмсдщьбукаощжзьрыщаыпмяызшхпбьйацчзюимпелумсрйюасавдыугшбрмэтдйкяуришпчиоскчтхэейыосййричикзддрятарщроюазахачшфщчшурпрбуашькщепщчшфитдьчфщроюазацквснхтбьечшчыачешудкгхавклаяхбмхашнэпосюеюазнтдщьбудшщепщчшфикайаэкишныцмбээелучылшрщашошзсбужифчмэйкблкмоснфэщкылшрщхлиечшритэзалаеймюбероюарптылшцюцрчийщпаюеющчшхпэщхеишашйамущьбукаьэзхцмустдмшыщдшцчсдхйыуыщйаудчикабпсаюезлиекдффыршдчимшлчлэфуюаззддрятачшсающчшййнцусюаьжхезнмшйщгпридщнйымюдкебдкйющешхщнкшлнуюсэебдьебпщьюарпжиегтдлэфщюенщдезаламдосусжулапасйюдаюнежсщьйкэытэшсосгпэпщепщчшфихехщюедшэпеемучщройкэысарепуосхасасйленкссвссеоамдосвпхрзшмейрцлтедчусхеццкемчььсдмэшсрморушнллирмффаыпмяызшщфзсййымзсхажалафщнпбупюоьюдкеещхщшпщяавцквснхтбьечшджпшюешпщьбуказаэплахщдщнйдщтечшджпшюешпщьбуэщшчсщряаюэщкацкышщехеаитбюарщлсцпэсеегпосщерпусдюйаюдбучихеэдэппртехарпеылегшмчхухаяютечшюдуссайщсллдыууокайасазаопчичпнхбморешэшсающуонафщгшмейррихушкдщнйдщтечшщукайаэкышхемчтэхевателуцчисхпкучызшцшмейряжпшюешпщьбудшоылшищгамуыщюаешлуьппрринхдщцадуришпчичифубелшмшмвкйуыгшхлвпьюзсййушфиюдпелучырйнхюайажлэщцжйацчушугрйхпцчсдьчфщроюаепжьюдмшеемучщроюазацчаябуащыщдшварчмэчинкныцмйквыдщлагчмэашзщэиьчщщчшмейртвещжзьргшкдтваыпмяызшыыдщнпщьбукачэрщмечшлжйазакмхйтвдебукчкйбвжшоыачлаоыьчмбюдпаюехдхввамнхукчкйбвжшгсйасандуссагшяснежсчикммьлезлиекдбюфшхдиырйгекбюдтдфчнцюдавлэкдусосйасадуклзщюдфчнцюдкемсуювпьюцкдщтечшэиащваейнцусюазблэчшгечофщгесаьпюачпжжпшюечуаюгарпсенуказаэпюазшлууросйасажлешзлйаудрйхрмэцпфжйахеродюыщжрпроппрчикммьлевлщднхбмнхшсзмгьхпэсрежаолфдыууофнрйнцусюазблэчшрщзщжацчтыкйкаешхакмхйтвжшусййушфиюдюдаюгпшгцчтыкйкающамджйазаддхухегарпцпбьюахщэдкгщыфутдаюащышэылшищяросчшмезахехщяпвсхйюдаюыущаидвцюдаюьичбзлцчтыкйэщыштыаччбзстдаюышхехаедюшзщрпщысагшлайеошцкнуфносачзюидцецчхйхажатечшжьйацчтыкйдшрщзщашчоыйыуйаусйрпнюлтевйвпрпгечпщачшкдььрмегфчпрбелшцающашчопаюебушщькышзшвыйафщышхпцмдрщыыуюехакчщуиезафнщыаччбзстдаюрщлаеебдкйлщйачнрйюблэчшшхнфрпющэплщцчсдфмчзьчжлаыпмяызшжхбмнхшсбужичлщерпюабуашькщыдщвйрмыулпбьйашдтыцмюарпхвцчьрдщгшашчоламчэичаэхшстдаюриэщйазнзсзшйшлшюагпчиеысагшлайезщайхлбшглэщйщчшчамеешвдбювсрэжичбзлэпрешхнфрплацсрчцпхюшрфчсимэоскгфуыйыхффэплщгарпсенуказарчыупмхуэсдммэтдяавдчишхтаичшзыйыуйаусйрпнушхакмюбпмншжлэщйщчшэирщлэгерпюабуосйещеэдсечушгцмпнщьбукаюдуыдщимюдкечушгмщрщашщппрэщкырйдщьлщеющвпьюриюдюашдйржахетсййвпэсгпчинаькгшхпннзщццтвкчисжлзсйепртшййыуйаусйрпншдажйазмгьусффщлщрбезахемчтэлекмаюрщудеапамдосшсцпфжнлзуыщюазреызшэатдрмхпщьбудшщыхубвчочпщаэщялчохехалюидвиаммсееапегкажлхехдпрчиилмечшшшцкдщтечшчызшэатдрмлэчлрщнаэшэдкйчбйкишугрййкоыдднпрщышлсбубеаунккмнежскгцчтыкйкавйыуйаусйрпносфнзвюаиейркезаокйщгаынрйщызюимюдаюаыпмяызшцлгпшгцчтыкйкаяхбмщырйнхкелиачгшшдсдмэшсрмфукукчщгчилиачгшзсечмбрмфуэснарпзючшпмвпфчбшмейрпныурщгпзхцмчэиорщэаэшшщрщхезакдььрмьрпнхщшдькюедефщроошкаюрпркдчэуырщлхчээпмеидбюхахщимюдюарппьщсрплаэщкаюытэтедщпуэщвкющиулаэиыйхлллнажахоусиппрсеэщюхыййаькэиеыйееуйафмыущфзщжбглщейеуозсащвашйымюдхунлищжанарпзючшбуосачиеэдщырйнхюахйщфрпешбероюарущефпкезарчцптддчщфдщпуэщвкющньйашегахлтейицмрйыезаокнейежпэиэщгэхувлуоыуыщимфмйщпшйрщьйапахпьююаяофэхувлуолиачйахагаодвимдчитысазшйыжжйажлчпнхыезахаэасачшашйарокамейецыьпяйхеейыуйаусйрнфйщхлюеерффасхйюдкемдсилэгерпйклижуашрщщейечшвппршгцчтыкйканущефптачштэрщзщяпэптбьерпимюдкеслщещцримежагекаюрэпьчяфьеруюсхпымздюлщелшашфьымосьрчифшцкщедеюакайасажлнктешщэилиачгшопьчффкммьофпаюечэрщошбеюеюылшищгаясбрмэтдюадуклзщачисюарехеэдпрмэтдавнкхатешщашлиачгшдчьнчиипяыачжижуыщашащышгпридчьнрифусицлщеомхпипчушгмщрщашгшмейрсемьюдкеипгекбхщвпчпжжйаайхлзаейуюфщроошэщнхльюаэпеямшщевлэияффубелшщфцчтыкйхрмсуювпьюыщдшварчмэчиащварщэщйщчшэийщхатешщчшбущефпсдюдисфуидчиеапячщ";
	
	fout.open("text.txt");
	
	fout << decode(cipher, key.first, key.second);

	fout.close();

	return 0;
}