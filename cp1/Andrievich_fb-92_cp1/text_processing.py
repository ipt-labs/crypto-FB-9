def process_text(alphabet):
    with open("text.txt", "r", encoding='1251') as file:
        text = file.read().replace("\n", " ").replace("\r", "").lower().replace("ั", "ะต").replace("ั", "ั")
        for char in text[:]:
            if char not in alphabet and char != " ":
                text = text.replace(char, "")
        return " ".join(text.split())
