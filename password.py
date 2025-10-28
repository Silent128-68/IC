import hashlib
import os
import getpass
import string 

# --- Константы ---
PASSWORD_FILE = 'pass_file.dat' 
MAGIC_WORD = 'INIT_MAGIC_WORD_123'
LOCK_MARK = 'ACCOUNT_LOCKED'
MAX_ATTEMPTS = 3

def hash_password(password: str) -> str:
    xor_sum = 0
    
    # 1. Превратить строку пароля в последовательность байт
    data_bytes = password.encode('utf-8')
    
    # 2. Идти по байтам с шагом 2 (по 16 бит / 2 байта)
    for i in range(0, len(data_bytes), 2):
        
        # 3. Взять "кусок" (chunk) в 2 байта
        chunk = data_bytes[i : i+2]
        
        # 4. Если в "куске" не хватает байта (т.е. это конец
        #    и у нас нечетное кол-во байт),
        #    дополнить его нулями (b'\x00')
        if len(chunk) == 1:
            chunk += b'\x00' # b'\x00' - это байт-ноль
            
        # 5. Превратить 2 байта в одно 16-битное число
        #    и "сложить" (XOR, ^) с предыдущим результатом
        xor_sum ^= int.from_bytes(chunk, 'big')
        
    # 6. Вернуть результат в виде СТРОКИ.
    #    Это важно, чтобы в файле могли лежать и "12345" (хэш),
    #    и "INIT_MAGIC_WORD_123", и "ACCOUNT_LOCKED".
    return str(xor_sum)

def check_password_complexity(password: str) -> bool:
    # Определяем наши наборы символов
    LATIN_CHARS = string.ascii_letters
    SPECIAL_AND_DIGITS = string.punctuation + string.digits
    CYRILLIC_CHARS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    
    # --- Начинаем проверки ---
    if len(password) < 6:
        print("Ошибка: Пароль должен быть не менее 6 символов.")
        return False
    
    # Проверка на латиницу
    if not any(c in LATIN_CHARS for c in password):
        print("Ошибка: Пароль должен содержать хотя бы один латинский символ (a-z, A-Z).")
        return False
        
    # Проверка на кириллицу
    if not any(c in CYRILLIC_CHARS for c in password):
        print("Ошибка: Пароль должен содержать хотя бы один кириллический символ (а-я, А-Я).")
        return False
        
    # Проверка на цифры/спецсимволы
    if not any(c in SPECIAL_AND_DIGITS for c in password):
        print("Ошибка: Пароль должен содержать хотя бы одну цифру или специальный символ (%, *, #...).")
        return False

    # --- НОВЫЕ ПРОВЕРКИ НА РЕГИСТР ---
    # (c.isupper() вернет True, если 'c' - буква в ВЕРХНЕМ регистре)
    if not any(c.isupper() for c in password):
        print("Ошибка: Пароль должен содержать хотя бы одну букву в верхнем регистре.")
        return False
        
    # (c.islower() вернет True, если 'c' - буква в нижнем регистре)
    if not any(c.islower() for c in password):
        print("Ошибка: Пароль должен содержать хотя бы одну букву в нижнем регистре.")
        return False
    # --- Конец новых проверок ---

    # Если все проверки пройдены:
    return True

def handle_first_run():
    print("--- Первый запуск программы ---")
    print("Необходимо установить пароль.")
    
    # --- Обновленный блок: Выводим критерии для наглядности ---
    print("\nТребования к паролю (должны выполняться ОДНОВРЕМЕННО):")
    print(" 1. Длина не менее 6 символов.")
    print(" 2. Содержит хотя бы 1 латинский символ (a-z, A-Z).")
    print(" 3. Содержит хотя бы 1 кириллический символ (а-я, А-Я).")
    print(" 4. Содержит хотя бы 1 цифру или спец. символ (!, #, $...).")
    print(" 5. Содержит хотя бы 1 букву в ВЕРХНЕМ регистре.")
    print(" 6. Содержит хотя бы 1 букву в нижнем регистре.")
    print("-" * 40)
    # --- Конец обновленного блока ---
    
    new_password = ""
    while True:
        # getpass.getpass скрывает ввод пароля (не показывает символы)
        new_password = getpass.getpass("Введите новый пароль: ")
        
        if check_password_complexity(new_password):
            new_hash = hash_password(new_password)
            try:
                with open(PASSWORD_FILE, 'w', encoding='utf-8') as f:
                    f.write(new_hash)
                print("Пароль успешно создан и сохранен.")
                break 
            except IOError as e:
                print(f"Критическая ошибка: Не удалось записать хэш в файл {PASSWORD_FILE}. {e}")
                break
        else:
            print("Пароль не соответствует требованиям. Попробуйте снова.")

def handle_subsequent_run(stored_hash: str):
    print("--- Проверка доступа ---")
    
    for attempt in range(MAX_ATTEMPTS):
        # Используем getpass.getpass() - он не показывает ввод, и это стандарт.
        user_pass = getpass.getpass(f"Введите пароль (попытка {attempt + 1}/{MAX_ATTEMPTS}): ")
        
        user_hash = hash_password(user_pass)
        
        if user_hash == stored_hash:
            print("Доступ разрешен. Программа продолжает работу.")
            print("... (основная логика программы) ...")
            return 
            
        else:
            print("Неверный пароль.")
            
    print("Превышено количество попыток ввода пароля.")
    
    try:
        with open(PASSWORD_FILE, 'w', encoding='utf-8') as f:
            f.write(LOCK_MARK)
        print(f"Учетная запись заблокирована. Файл {PASSWORD_FILE} обновлен.")
    except IOError as e:
        print(f"Критическая ошибка: Не удалось записать метку блокировки. {e}")

def main():
    if not os.path.exists(PASSWORD_FILE):
        print(f"Ошибка: Файл пароля '{PASSWORD_FILE}' не найден.")
        print("Для первого запуска создайте этот файл и поместите в него строку:")
        print(MAGIC_WORD)
        return 

    try:
        with open(PASSWORD_FILE, 'r', encoding='utf-8') as f:
            file_content = f.read().strip() 
    except IOError as e:
        print(f"Ошибка: Не удалось прочитать файл {PASSWORD_FILE}. {e}")
        return

    if file_content == LOCK_MARK:
        print("Доступ заблокирован (превышено число попыток).")
        return
        
    elif file_content == MAGIC_WORD:
        handle_first_run()
        
    else:
        handle_subsequent_run(stored_hash=file_content)

# --- Запуск программы ---
if __name__ == "__main__":
    main()
