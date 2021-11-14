import re
from collections import Counter


class Slammer:
    def __init__(self, path_to_file):
        self.keys = ['ой', 'как', 'этот', 'текст', 'зашифровался']
        self.path_to_file = path_to_file
        self.text = self.__getText()
        self.alphabet = self.__initAlphabetDict()

    def __getText(self):
        return re.sub(r"[^а-яА-Я]", "", open(self.path_to_file).read()).lower()

    def __initAlphabetDict(self):
        return ''.join([chr(i) for i in range(ord('а'), ord('а') + 32)])

    def __getComplianceIndex(self, text):
        compliance_index: int = 0
        frequency = Counter(text)
        for ch in frequency:
            compliance_index += frequency[ch] * (frequency[ch] - 1)
        compliance_index /= (len(text) * (len(text) - 1))
        return compliance_index

    def encrypt(self):
        print(self.__getComplianceIndex(self.text))
        for key in self.keys:
            cipher_text: str = ''
            for pointer, char in enumerate(self.text):
                plain_char_idx = self.alphabet.index(char)
                key_char_idx = self.alphabet.index(key[pointer % len(key)])
                cipher_text += self.alphabet[(plain_char_idx + key_char_idx) % len(self.alphabet)]
            compliance_index = self.__getComplianceIndex(cipher_text)
            with open(key + '.txt', 'w') as file:
                file.write(cipher_text)
                file.write(f"\n--------------\nCompliance index: {compliance_index}")

    def crack(self, pathToText):
        text = open(pathToText).read().replace("\n", "").replace(" ", "").replace("ё", "")



s = Slammer("text.txt")
s.encrypt()
