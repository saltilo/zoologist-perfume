import os

# Директория с файлами
directory = '/Users/kristina/Documents/Projects/Zoologist/JSON'

# Поиск и удаление файлов с указанными подстроками в названии
for filename in os.listdir(directory):
    if 'deluxe-bottle' in filename or 'travel-spray' in filename:
        filepath = os.path.join(directory, filename)
        try:
            os.remove(filepath)
            print(f"Удален файл: {filepath}")
        except Exception as e:
            print(f"Не удалось удалить файл: {filepath}. Ошибка: {e}")

print("Удаление завершено.")
