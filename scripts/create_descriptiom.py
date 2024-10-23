import json

# Загрузка объединенного файла
with open('all_perfumes.json', 'r', encoding='utf-8') as infile:
    all_data = json.load(infile)

# Словарь для классификации нот
note_categories = {
    'floral': ['Acacia', 'Blue Lotus Accord', 'Carnation', 'Champaca', 'Frangipani', 'Geranium', 'Heliotrope', 'Honeysuckle', 'Hyacinth', 'Jasmine', 'Jasmine Absolute', 'Japanese Plum Blossom', 'Lily of the Valley', 'Linden-blossom', 'Marigold', 'Mimosa', 'Muguet', 'Night Blooming Jasmine', 'Orange Blossom', 'Orange Flower', 'Osmanthus', 'Peony', 'Red Rose', 'Rose', 'Rose Absolute', 'Snowdrop', 'Tuberose', 'Tulip', 'White Rose', 'Ylang Ylang'],
    'woody': ['Cedar', 'Cedarwood Atlas', 'Cashmeran', 'Dry Wood', 'Earthy Notes', 'Fir Balsam Absolute', 'Hinoki Wood', 'Hydro Carbon Resin', 'Incense', 'Labdanum Absolute', 'Oak Absolute', 'Patchouli', 'Styrax', 'Vetiver', 'Woody Notes'],
    'spicy': ['Anise', 'Cinnamon', 'Clove', 'Cumin', 'Davana', 'Galbanum', 'Jatamansi', 'Pink Pepper', 'Saffron', 'Turmeric Root'],
    'sweet': ['Amber', 'Benzoin', 'Beeswax', 'Cocoa', 'Coconut', 'Coconut Milk', 'Hazelnut', 'Honey', 'Mate', 'Milk', 'Myrrh', 'Orris', 'Orris Absolute', 'Orris Concrete', 'Powdery Notes', 'Suede', 'Wine Accord'],
    'fruity': ['Japanese Plum Blossom', 'Plum Accord'],
    'herbal': ['Camomile', 'Carrot Seeds', 'Clary Sage', 'Hay', 'Hay Absolute', 'Lavender', 'Mate', 'Peony', 'Violet Leaves'],
    'aquatic': ['Aquatic Florals', 'Bamboo', 'Sea Breeze', 'Salty Accord', 'Salty Skin Accord', 'Snowdrop', 'Water'],
    'resinous': ['African Stone', 'Benzoin', 'Fir Balsam Absolute', 'Frankincense', 'Labdanum Absolute', 'Myrrh', 'Opoponax', 'Styrax'],
    'musky': ['Light Musk', 'Suede', 'Leather', 'White Musk'],
    'other': ['Beer Extract CO₂', 'Black Ink Accord', 'Black Tea', 'Hydro Carbon Resin', 'Minerals', 'Whiskey']
}


def classify_notes(notes, categories):
    classified_notes = {category: 0 for category in categories.keys()}

    for note in notes['top'] + notes['heart'] + notes['base']:
        for category, keywords in categories.items():
            if note in keywords:
                classified_notes[category] += 1

    primary_category = max(classified_notes, key=classified_notes.get)
    return primary_category


# Создание описаний для каждого аромата
descriptions = []

for perfume in all_data:
    primary_category = classify_notes(perfume['notes'], note_categories)
    description = {
        "title": perfume['title'],
        "primary_category": primary_category,
        "description": f"{primary_category.capitalize()} аромат с нотами {', '.join(perfume['notes']['heart'])}, создающими основу аромата."
    }
    descriptions.append(description)

# Сохранение описаний в файл
with open('perfume_descriptions.json', 'w', encoding='utf-8') as outfile:
    json.dump(descriptions, outfile, ensure_ascii=False, indent=4)

print("Описания ароматов сохранены в файл 'perfume_descriptions.json'")
