import csv
import shutil
import json

file_path = '../KitchenGuru/static/recipes/recipes.csv'
path_start = '../KitchenGuru/static/recipes/recipes_images/'
images_path_from = 'C:/Users/Vain/Desktop/Food Images/'
images_path_to = 'C:/Users/Vain/Desktop/Kitchen Guru/KitchenGuru/KitchenGuru/static/recipes_images/'
n_recipes = 5

filename = open(file_path, 'r', encoding='utf8')
f = csv.DictReader(filename)

data = []

i = 50
for col in f:
    dt = {
        'model': 'recipes.Recipes',
        'fields': {}
    }
    data_temp = {
        'title': '',
        'ingredients': '',
        'instructions': '',
        'image_name': ''
    }
    data_temp['title'] = col['Title']
    data_temp['ingredients'] = col['Cleaned_Ingredients'][1:-1]
    data_temp['instructions'] = col['Instructions']
    data_temp['image_name'] = path_start + col['Image_Name'] + ".jpg"
    shutil.copy2(images_path_from + col['Image_Name'] + '.jpg', images_path_to + col['Image_Name'] + '.jpg')
    dt['fields'] = data_temp
    data.append(dt)
    i -= 1
    if not i:
        break

with open('fixtures/recipes.json', 'w') as f:
    json.dump(data, f)
