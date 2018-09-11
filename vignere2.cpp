#include <ctype.h>
#include <string.h>
#include <iostream>

using namespace std;

char encryptLtr(char mChar, char kChar)
{

	bool isUpper = mChar >= 'A' && mChar <= 'Z';
	mChar = tolower(mChar);
	kChar = tolower(kChar);
	int keyValue = kChar - 'a';
	int messageValue = mChar - 'a';
	messageValue += keyValue;
	messageValue %= 26;
	mChar = messageValue + 'a';
	if (isUpper)
	{
		mChar = toupper(mChar);
	}
	return mChar;
}

string encrypt(string m, string k)
{
	string c = "";
	for (int pos = 0; pos < m.length(); pos++)
	{
		if ((m.at(pos) >= 'a' && m.at(pos) <= 'z') || (m.at(pos) >= 'A' && m.at(pos) <= 'Z'))
		{
			c += encryptLtr(m.at(pos), k.at(pos%k.length()));
		}
		else
		{
			c += m.at(pos);
		}
	}
	return c;
}

int main()
{
	cout << " ------------------------ " << endl
		 << "|   Vignere Cipher 1.0   |" << endl
		 << "|Author: Matt Jagodzinski|" << endl
		 << " ------------------------ " << endl;
	string message;
	string key = "Jagodzinski";
	cout << "Enter your message : " << endl;
	getline(cin, message);
	cout << encrypt(message, key) << endl;
	return 0;
}