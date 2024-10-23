import os
import json


def update_perfumes_json(oembed_dir, perfumes_json_path):
    # Проверка существования файла updated_all_perfumes.json
    if not os.path.isfile(perfumes_json_path):
        raise FileNotFoundError(
            f"Файл {perfumes_json_path} не найден или это не файл")

    # Чтение исходного файла updated_all_perfumes.json
    with open(perfumes_json_path, 'r', encoding='utf-8') as f:
        perfumes_data = json.load(f)

    # Создание словаря для быстрого поиска по названию продукта (title)
    perfumes_dict = {perfume['title']: perfume for perfume in perfumes_data}

    # Проход по всем .oembed файлам в указанной директории
    for filename in os.listdir(oembed_dir):
        if "deluxe-bottle.oembed" in filename:
            oembed_file_path = os.path.join(oembed_dir, filename)
            try:
                if os.path.getsize(oembed_file_path) > 0:
                    with open(oembed_file_path, 'r', encoding='utf-8') as f:
                        oembed_data = json.load(f)
                else:
                    print(f"Файл пуст: {oembed_file_path}")
                    continue
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка чтения JSON из файла {oembed_file_path}: {e}")
                continue

            # Извлечение названия продукта из названия файла
            product_title = filename.replace(
                "-deluxe-bottle.oembed", "").replace("-", " ").title()
            print(
                f"Обработка файла: {oembed_file_path}, Название продукта: {product_title}")

            # Обновление данных в словаре
            for title in perfumes_dict:
                if product_title in title:
                    perfumes_dict[title]['thumbnail_url'] = oembed_data.get(
                        'thumbnail_url', '')
                    perfumes_dict[title]['url'] = oembed_data.get('url', '')
                    print(f"Обновлены данные для: {title}")
                    break

    # Преобразование словаря обратно в список
    updated_perfumes_data = list(perfumes_dict.values())

    # Запись обновленных данных в файл updated_all_perfumes.json
    with open(perfumes_json_path, 'w', encoding='utf-8') as f:
        json.dump(updated_perfumes_data, f, ensure_ascii=False, indent=4)
    print("Обновленные данные записаны в файл.")


# Путь к директории с .oembed файлами
oembed_directory = '/Users/kristina/zoologist_scraper/downloaded_site/products'
# Путь к файлу updated JSON
perfumes_json_file = '/Users/kristina/Documents/Projects/Zoologist/updated_all_perfumes.json'

update_perfumes_json(oembed_directory, perfumes_json_file)
