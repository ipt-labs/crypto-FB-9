import re
from collections import Counter


class Sys:
    @staticmethod
    def get_alphabet() -> str:
        return "абвгдежзийклмнопрстуфхцчшщьыэюя"

    @staticmethod
    def get_text(path_to_file) -> str:
        return re.sub(r"[^а-яА-Я]", "", open(path_to_file).read()).lower()

    @staticmethod
    def get_most_frequent_ru_bigrams() -> list:
        return ['ст', 'но', 'то', 'на', 'ен']

    @staticmethod
    def get_unavailable_bigrams() -> list:
        return ['аы', 'аь', 'еэ', 'жф', 'жч', 'жш', 'жщ', 'зп', 'зщ', 'йь', 'оы', 'уы', 'уь', 'фц', 'хщ', 'цщ', 'цэ',
                'чщ', 'чэ', 'шщ', 'ьы']

    @staticmethod
    def get_most_frequent_text_bigrams(text):
        return list(dict(
            sorted(Counter(text[idx:idx + 2] for idx in range(0, len(text) - 1, 2)).items(), key=lambda x: x[1],
                   reverse=True)).keys())[:5]

    @staticmethod
    def get_all_bigrams_from_text(text):
        return [text[idx:idx + 2] for idx in range(0, len(text) - 1, 2)]

    @staticmethod
    def log(line):
        with open("log.txt", "w") as file:
            file.write(line + "\n")
