import re

def cyrillic_to_latin(text):
    base_mapping = {
        'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v',
        'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd', 'Е': 'E', 'е': 'e',
        'Ё': 'Yo', 'ё': 'yo', 'Ж': 'J', 'ж': 'j', 'З': 'Z', 'з': 'z',
        'И': 'I', 'и': 'i', 'Й': 'Y', 'й': 'y', 'К': 'K', 'к': 'k',
        'Л': 'L', 'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n',
        'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R', 'р': 'r',
        'С': 'S', 'с': 's', 'Т': 'T', 'т': 't', 'У': 'U', 'у': 'u',
        'Ф': 'F', 'ф': 'f', 'Х': 'X', 'х': 'x', 'Ц': 'Ts', 'ц': 'ts',
        'Ч': 'Ch', 'ч': 'ch', 'Ш': 'Sh', 'ш': 'sh', 'Щ': 'Sh', 'щ': 'sh',
        'Ъ': "'",  'ъ': "'", 'Ь': '', 'ь': '', 'Э': 'E', 'э': 'e',
        'Ю': 'Yu', 'ю': 'yu', 'Я': 'Ya', 'я': 'ya',
        'Қ': 'Q', 'қ': 'q', 'Ғ': "G'", 'ғ': "g'", 'Ў': "O'", 'ў': "o'", 'Ҳ': 'H', 'ҳ': 'h',
    }

    vowels = 'АаЕеЁёИиОоУуЎўЭэЮюЯя'
    special_before_e = vowels + 'ЙйЪъ'

    def transliterate_word(word):
        mapping = {k: v.upper() for k, v in base_mapping.items()} if word.isupper() else base_mapping
        result = ''
        for i, char in enumerate(word):
            if char in ['Е', 'е']:
                prev = word[i - 1] if i > 0 else ' '
                if i == 0 or prev in special_before_e:
                    result += 'YE' if word.isupper() else ('Ye' if char == 'Е' else 'ye')
                else:
                    result += mapping.get(char, char)
            else:
                result += mapping.get(char, char)
        return result

    words = re.findall(r'\w+|\W+', text)
    return ''.join(transliterate_word(word) if word.strip().isalpha() else word for word in words)
