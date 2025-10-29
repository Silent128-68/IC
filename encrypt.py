# --- encrypt.py ---

# 1. Алфавит. Должен быть одинаковым в обоих модулях.
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ALPHABET_LEN = len(ALPHABET)

def generate_full_table():
    """
    Генерирует полную квадратную таблицу Виженера 33x33.
    Каждая строка - циклический сдвиг алфавита.
    """
    table = []
    for i in range(ALPHABET_LEN):
        # Выполняем циклический сдвиг
        shifted_alphabet = ALPHABET[i:] + ALPHABET[:i]
        # Добавляем новую строку (как список символов для удобства)
        table.append(list(shifted_alphabet))
    return table

def process_key(key_text):
    """
    Очищает ключ: приводит к верхнему регистру и удаляет 
    все символы, не входящие в алфавит.
    """
    processed = ""
    for char in key_text.upper():
        if char in ALPHABET:
            processed += char
    return processed

def encrypt(plaintext, key, full_table):
    """
    Шифрует текст, используя метод поиска по полной таблице.
    """
    
    # Готовим ключ
    processed_key = process_key(key)
    if not processed_key:
        return "Ошибка: Ключ не содержит букв русского алфавита."

    ciphertext = ""
    key_index = 0 # Счетчик для "движения" по ключу

    # Это "первая строка подматрицы" из задания
    first_row = ALPHABET # Строка "АБВГ..."

    # Словарь для быстрого поиска индекса строки по букве ключа
    # 'А' -> 0, 'Б' -> 1, и т.д.
    alphabet_map = {char: i for i, char in enumerate(ALPHABET)}
    
    # ----------------------------------------------------
    # Цикл шифрования - точно по вашему описанию
    # ----------------------------------------------------
    for char in plaintext.upper():
        
        # Шифруем, только если это буква
        if char in ALPHABET:
            p_char = char # Буква исходного текста
            
            # 1. "под каждой буквой ... записываются буквы ключа"
            k_char = processed_key[key_index % len(processed_key)]
            
            # 2. "на пересечении линий..."
            
            # "...соединяющих буквы шифруемого текста в первой строке..."
            # Находим столбец, в котором находится наша буква p_char
            p_col_index = first_row.find(p_char)
            
            # "...и находящихся под ними букв ключа"
            # Находим строку, соответствующую букве ключа k_char
            # (Используем full_table, т.к. "подматрица" - это просто
            # выборка строк из полной таблицы)
            k_row_index = alphabet_map[k_char]
            key_row = full_table[k_row_index]
            
            # Находим букву на пересечении
            c_char = key_row[p_col_index]
            
            ciphertext += c_char
            
            # Сдвигаем индекс ключа
            key_index += 1
        
        else:
            # Не-буквы (пробелы, знаки) просто добавляем
            ciphertext += char
            
    return ciphertext

# --- Основная часть программы ---

print("--- Модуль Шифрования (Виженер, табличный метод) ---")

# 1. Генерируем полную таблицу (33x33)
vigenere_table = generate_full_table()

# 2. Получаем данные
text_to_encrypt = input("Введите текст для шифрования: ")
key = input("Введите ключ: ")

# 3. Шифруем
encrypted_text = encrypt(text_to_encrypt, key, vigenere_table)

# 4. Сохраняем в файл-контейнер
if "Ошибка" not in encrypted_text:
    try:
        with open("container.txt", "w", encoding="utf-8") as f:
            f.write(encrypted_text)
        print("\n[УСПЕХ]")
        print(f"Текст зашифрован и сохранен в файл 'container.txt'")
        print(f"Шифротекст: {encrypted_text}")
    except Exception as e:
        print(f"Произошла ошибка при записи файла: {e}")
else:
    print(f"\n[ОШИБКА]")
    print(encrypted_text)

print("Модуль шифрования завершил работу.")
