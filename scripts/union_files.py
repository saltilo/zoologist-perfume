import os
import json

# Директория с JSON файлами
directory = '/Users/kristina/Documents/Projects/Zoologist/JSON'

# Список для хранения данных всех ароматов
all_data = []

# Обработка каждого файла в директории
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)

        # Чтение содержимого .json файла
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            all_data.append(data)

# Сохранение объединенных данных в один JSON файл
with open('all_perfumes.json', 'w', encoding='utf-8') as outfile:
    json.dump(all_data, outfile, ensure_ascii=False, indent=4)

print("Все данные объединены в файл 'all_perfumes.json'")
