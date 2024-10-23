import os
import json
import re
from bs4 import BeautifulSoup

# Директория с файлами .oembed
source_directory = '/Users/kristina/zoologist_scraper/downloaded_site/products'
# Директория для сохранения JSON файлов
destination_directory = '/Users/kristina/Documents/Projects/Zoologist/JSON'

# Создание директории, если она не существует
os.makedirs(destination_directory, exist_ok=True)

# Функция для извлечения нот из описания


def extract_notes(description):
    notes = {"top": [], "heart": [], "base": []}
    soup = BeautifulSoup(description, 'html.parser')

    # Извлечение всех тегов strong
    strong_tags = soup.find_all('strong')

    # Поиск нужных секций и извлечение текста
    for tag in strong_tags:
        if 'Top Notes:' in tag.text:
            top_notes_text = tag.next_sibling
            if top_notes_text:
                notes['top'] = [note.strip()
                                for note in top_notes_text.split(',')]
        elif 'Heart Notes:' in tag.text:
            heart_notes_text = tag.next_sibling
            if heart_notes_text:
                notes['heart'] = [note.strip()
                                  for note in heart_notes_text.split(',')]
        elif 'Base Notes:' in tag.text:
            base_notes_text = tag.next_sibling
            if base_notes_text:
                notes['base'] = [note.strip()
                                 for note in base_notes_text.split(',')]

    return notes


# Обработка каждого файла в директории
for filename in os.listdir(source_directory):
    if filename.endswith('.oembed'):
        filepath = os.path.join(source_directory, filename)

        # Чтение содержимого .oembed файла
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Извлечение нужных полей
        filtered_data = {
            'title': data.get('title'),
            'description': BeautifulSoup(data.get('description', ''), 'html.parser').get_text(),
            'notes': extract_notes(data.get('description', ''))
        }

        # Создание нового имени файла с расширением .json
        json_filename = filename.replace('.oembed', '.json')
        json_filepath = os.path.join(destination_directory, json_filename)

        # Сохранение данных в .json файл
        with open(json_filepath, 'w', encoding='utf-8') as json_file:
            json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

        print(f"Создан файл: {json_filepath}")

print("Преобразование завершено.")
