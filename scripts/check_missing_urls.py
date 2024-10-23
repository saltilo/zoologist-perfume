import json
import os


def find_missing_urls(perfumes_json_path):
    # Проверка существования файла updated_all_perfumes.json
    if not os.path.isfile(perfumes_json_path):
        raise FileNotFoundError(
            f"Файл {perfumes_json_path} не найден или это не файл")

    # Чтение файла updated_all_perfumes.json
    with open(perfumes_json_path, 'r', encoding='utf-8') as f:
        perfumes_data = json.load(f)

    missing_urls = []

    # Проверка на наличие полей thumbnail_url и url
    for perfume in perfumes_data:
        if not perfume.get('thumbnail_url') or not perfume.get('url'):
            missing_urls.append(perfume['title'])

    # Вывод результатов
    if missing_urls:
        print("Следующие продукты не имеют полей 'thumbnail_url' и/или 'url':")
        for title in missing_urls:
            print(f"- {title}")
    else:
        print("Все продукты имеют поля 'thumbnail_url' и 'url'.")


# Путь к файлу updated JSON
perfumes_json_file = '/Users/kristina/Documents/Projects/Zoologist/updated_all_perfumes.json'

find_missing_urls(perfumes_json_file)
