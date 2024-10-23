import os
import json


def add_missing_urls(perfumes_json_path):
    # Проверка существования файла updated_all_perfumes.json
    if not os.path.isfile(perfumes_json_path):
        raise FileNotFoundError(
            f"Файл {perfumes_json_path} не найден или это не файл")

    # Чтение файла updated_all_perfumes.json
    with open(perfumes_json_path, 'r', encoding='utf-8') as f:
        perfumes_data = json.load(f)

    # Добавление шаблонов полей для продуктов, у которых они отсутствуют
    for perfume in perfumes_data:
        if not perfume.get('thumbnail_url'):
            perfume['thumbnail_url'] = ''
        if not perfume.get('url'):
            perfume['url'] = ''

    # Запись обновленных данных в файл updated_all_perfumes.json
    with open(perfumes_json_path, 'w', encoding='utf-8') as f:
        json.dump(perfumes_data, f, ensure_ascii=False, indent=4)
    print("Шаблоны полей 'thumbnail_url' и 'url' добавлены в файл.")


# Путь к файлу updated JSON
perfumes_json_file = '/Users/kristina/Documents/Projects/Zoologist/updated_all_perfumes.json'

add_missing_urls(perfumes_json_file)
