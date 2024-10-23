import os
import json
import pandas as pd

# Директория с JSON файлами
directory = '/Users/kristina/Documents/Projects/Zoologist/JSON'

# Списки для хранения нот
top_notes = []
heart_notes = []
base_notes = []

# Обработка каждого файла в директории
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)

        # Чтение содержимого .json файла
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Добавление нот в соответствующие списки
        top_notes.extend(data['notes']['top'])
        heart_notes.extend(data['notes']['heart'])
        base_notes.extend(data['notes']['base'])

# Удаление дубликатов и сортировка
top_notes = sorted(set(top_notes))
heart_notes = sorted(set(heart_notes))
base_notes = sorted(set(base_notes))

# Создание DataFrame для удобства анализа
df_top_notes = pd.DataFrame(top_notes, columns=['Top Notes'])
df_heart_notes = pd.DataFrame(heart_notes, columns=['Heart Notes'])
df_base_notes = pd.DataFrame(base_notes, columns=['Base Notes'])

# Сохранение данных в Excel файл
with pd.ExcelWriter('notes_analysis.xlsx') as writer:
    df_top_notes.to_excel(writer, sheet_name='Top Notes', index=False)
    df_heart_notes.to_excel(writer, sheet_name='Heart Notes', index=False)
    df_base_notes.to_excel(writer, sheet_name='Base Notes', index=False)

print("Данные собраны и сохранены в файл 'notes_analysis.xlsx'")
