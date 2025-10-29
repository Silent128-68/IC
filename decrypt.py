# --- decrypt.py ---

# 1. Алфавит. Точно такой же, как в encrypt.py
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_LEN = len(ALPHABET)

def generate_full_table():
    """
    Генерирует полную квадратную таблицу Виженера 33x33.
    (Эта функция дублируется, т.к. модули независимы)
    """
    table = []
    for i in range(ALPHABET_LEN):
        shifted_alphabet = ALPHABET[i:] + ALPHABET[:i]
        # Здесь храним как список, т.к. в нем будем искать
        table.append(list(shifted_alphabet))
    return table

def process_key(key_text):
    """
    Очищает ключ: приводит к верхнему регистру и удаляет 
    все символы, не входящие в алфавит.
    """
    processed = ""
    for char in key_text.upper():
        if char in key_text.upper():
            processed += char
    return processed

def decrypt(ciphertext, key, full_table):
    """
    Дешифрует текст, используя метод поиска по полной таблице.
    """
    
    # Готовим ключ
    processed_key = process_key(key)
    if not processed_key:
        return "Ошибка: Ключ не содержит букв русского алфавита."

    plaintext = ""
    key_index = 0 # Счетчик для "движения" по ключу
    
    # Это "первая строка подматрицы" из задания
    first_row = full_table[0] # ['А', 'Б', 'В', ...]

    # Словарь для быстрого поиска индекса строки по букве ключа
    alphabet_map = {char: i for i, char in enumerate(ALPHABET)}

    # ----------------------------------------------------
    # Цикл дешифрования - точно по вашему описанию
    # ----------------------------------------------------
    for char in ciphertext.upper():
        
        # Дешифруем, только если это буква
        if char in ALPHABET:
            c_char = char # Буква шифротекста
            
            # 1. "над буквами ... надписываются буквы ключа"
            k_char = processed_key[key_index % len(processed_key)]
            
            # 2. "в строке ... соответствующей букве ключа..."
            # Находим строку, на которую указывает ключ
            k_row_index = alphabet_map[k_char]
            key_row = full_table[k_row_index]
            
            # "...отыскивается буква ... зашифрованного текста"
            # ИЩЕМ, в каком СТОЛБЦЕ в этой строке находится наша буква
            p_col_index = -1
            try:
                # list.index() - это и есть "отыскивается буква"
                p_col_index = key_row.index(c_char)
            except ValueError:
                # На всякий случай, если буква не найдется
                return f"Ошибка: Символ '{c_char}' не найден в строке ключа '{k_char}'."

            # "Находящаяся [в этом столбце] буква первой строки ... 
            # и будет буквой исходного текста."
            p_char = first_row[p_col_index]
            
            plaintext += p_char
            
            # Сдвигаем индекс ключа
            key_index += 1
        
        else:
            # Не-буквы просто переносим
            plaintext += char
            
    return plaintext

# --- Основная часть программы ---

print("--- Модуль Дешифрования (Виженер, табличный метод) ---")

try:
    # 1. Читаем контейнер
    with open("container.txt", "r", encoding="utf-8") as f:
        text_to_decrypt = f.read()
    
    print(f"Загружен шифротекст из 'container.txt': {text_to_decrypt}")
    
    # 2. Генерируем ту же самую таблицу (независимо)
    vigenere_table = generate_full_table()
    
    # 3. Запрашиваем ключ
    key = input("Введите ключ для дешифрования: ")
    
    # 4. Дешифруем
    decrypted_text = decrypt(text_to_decrypt, key, vigenere_table)
    
    if "Ошибка" not in decrypted_text:
        print("\n[УСПЕХ]")
        print(f"Расшифрованный текст: {decrypted_text}")
    else:
        print(f"\n[ОШИБКА]")
        print(decrypted_text)

except FileNotFoundError:
    print("\n[ОШИБКА]")
    print("Файл 'container.txt' не найден.")
    print("Сначала запустите модуль шифрования (encrypt.py).")
except Exception as e:
    print(f"Произошла ошибка при чтении файла: {e}")

print("Модуль дешифрования завершил работу.")
