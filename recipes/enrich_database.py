import csv
import json

file_path = '../KitchenGuru/static/recipes/recipes.csv'

filename = open(file_path, 'r', encoding='utf-8')
f = csv.DictReader(filename)

data = []

# Load recipes
# for col in f:
#     dt = {
#         'model': 'recipes.Recipes',
#         'fields': {}
#     }
#     data_temp = {
#         'title': '',
#         'ingredients': '',
#         'instructions': '',
#         'category': '',
#         'duration': '',
#         'ingredient_tags': ''
#     }
#     data_temp['title'] = col['\ufefftitle']
#     data_temp['ingredients'] = col['Ingredients']
#     data_temp['instructions'] = col['Instructions']
#     data_temp['category'] = col['Category'].lower()
#     data_temp['duration'] = int(col['Duration'])
#     data_temp['ingredient_tags'] = col['ingredient_tags'].lower()
#     dt['fields'] = data_temp
#     data.append(dt)

# Load ingredients
ingredients = []
for col in f:
    ingredients_temp = col['ingredient_tags'].lower().split(', ')
    for ingredient in ingredients_temp:
        if ingredient not in ingredients:
            ingredients.append(ingredient)

for ingredient in ingredients:
    dt = {
        'model': 'recipes.Ingredients',
        'fields': {
            'name': ingredient
        }
    }
    data.append(dt)

with open('fixtures/ingredients.json', 'w') as f:
    json.dump(data, f)
