import sys
import os
import json

HASH_FILENAME = ".file_hashes.json"

def calculate_xor_hash(file_path):
    xor_sum = 0
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(2)
                if not chunk:
                    break
                if len(chunk) == 1:
                    chunk += b'\x00'
                xor_sum ^= int.from_bytes(chunk, 'big')
    except IOError as e:
        print(f"Ошибка чтения файла {file_path}: {e}")
        return None
    return xor_sum

def create_baseline(directory):
    print("Файл хэшей не найден. Создание новой базы...")
    hashes = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, directory)
            if relative_path == HASH_FILENAME:
                continue
            file_hash = calculate_xor_hash(file_path)
            if file_hash is not None:
                hashes[relative_path] = file_hash
    with open(os.path.join(directory, HASH_FILENAME), 'w') as f:
        json.dump(hashes, f, indent=4)
    print("База хэшей создана.")

def verify_directory(directory):
    print("Файл хэшей найден. Проверка целостности...")
    hash_file = os.path.join(directory, HASH_FILENAME)
    with open(hash_file, 'r') as f:
        stored = json.load(f)

    current = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, directory).replace("\\", "/")
            if rel_path == HASH_FILENAME:
                continue
            h = calculate_xor_hash(file_path)
            if h is not None:
                current[rel_path] = h

    stored_norm = {k.replace("\\", "/"): v for k, v in stored.items()}

    added = set(current) - set(stored_norm)
    deleted = set(stored_norm) - set(current)
    modified = [f for f in stored_norm if f in current and stored_norm[f] != current[f]]

    print("\n--- Отчет ---")
    if not (added or deleted or modified):
        print("Всё без изменений.")
    else:
        if added:
            print("\n[+] Новые файлы:")
            for f in added:
                print("  ", f)
        if deleted:
            print("\n[-] Удалённые файлы:")
            for f in deleted:
                print("  ", f)
        if modified:
            print("\n[!] Изменённые файлы:")
            for f in modified:
                print("  ", f)
    print("------------------")

def main():
    # если путь передан аргументом — используем его, иначе спрашиваем
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = input("Введите путь к папке: ").strip()

    if not os.path.isdir(target_dir):
        print(f"Ошибка: Каталог '{target_dir}' не найден.")
        return

    hash_path = os.path.join(target_dir, HASH_FILENAME)
    if os.path.exists(hash_path):
        verify_directory(target_dir)
    else:
        create_baseline(target_dir)

if __name__ == "__main__":
    main()
