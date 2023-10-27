import csv
import json

file_path = '../KitchenGuru/static/recipes/recipes.csv'

filename = open(file_path, 'r', encoding='utf-8')
f = csv.DictReader(filename)

data = []
data_names = []

# Load recipes
for col in f:
    dt = {
        'model': 'recipes.Recipes',
        'fields': {}
    }
    data_temp = {
        'title': '',
        'ingredients': '',
        'instructions': '',
        'category': '',
        'duration': '',
        'ingredient_tags': ''
    }
    # data_names_temp = {
    #     'title': ''
    # }
    # data_names_temp['title'] = col['\ufeffTitle']
    data_temp['title'] = col['\ufeffTitle']
    data_temp['ingredients'] = col['Ingredients']
    data_temp['instructions'] = col['Instructions']
    data_temp['category'] = col['Category'].lower()
    try:
      data_temp['duration'] = int(col['Duration'])
    except:
       pass
    data_temp['ingredient_tags'] = col['ingredient_tags'].lower()
    dt['fields'] = data_temp
    # data_names.append(data_names_temp)
    data.append(dt)

# with open('fixtures/titles.json', 'w') as f:
#     json.dump(data_names, f)

# # Load ingredients
# ingredients = []
# for col in f:
#     ingredients_temp = col['ingredient_tags'].lower().split(', ')
#     for ingredient in ingredients_temp:
#         if ingredient not in ingredients:
#             ingredients.append(ingredient)

# for ingredient in ingredients:
#     dt = {
#         'model': 'recipes.Ingredients',
#         'fields': {
#             'name': ingredient
#         }
#     }
#     data.append(dt)

# data_image_names = [
#     {
#         "image": "https://veganfamilyrecipes.com/wp-content/uploads/2018/02/Creamy-Almond-Soup-Recipe-Vegan-4-of-7.jpg"
#       },
#       {
#         "image": "https://veggiedesserts.com/wp-content/uploads/2021/01/jerusalem-artichoke-soup-1.jpg"
#       },
#       {
#         "image": "https://www.recipegirl.com/wp-content/uploads/2006/10/Chilled-Avocado-Soup-2.jpg"
#       },
#       {
#         "image": "https://static01.nyt.com/images/2017/12/05/dining/20COOKING-SPLITPEASOUP2/20COOKING-SPLITPEASOUP2-articleLarge.jpg"
#       },
#       {
#         "image": "https://therecipecritic.com/wp-content/uploads/2023/02/Borscht-1.jpg"
#       },
#       {
#         "image": "https://c8.alamy.com/comp/AYC1TF/boston-bean-soup-AYC1TF.jpg"
#       },
#       {
#         "image": "https://www.lecremedelacrumb.com/wp-content/uploads/2022/01/carrot-coriander-soup-10sm-6.jpg"
#       },
#       {
#         "image": "https://salu-salo.com/wp-content/uploads/2014/11/Catalan-Fish-Soup-3.jpg"
#       },
#       {
#         "image": "https://cdn.greatlifepublishing.net/wp-content/uploads/sites/2/2018/12/21230059/Cauliflower-Walnut-Soup-OG.jpg"
#       },
#       {
#         "image": "https://www.saga.co.uk/contentlibrary/saga/publishing/verticals/food/recipes/soup/creamy-fenland-celery-soup-with-stilton-cheese-2.jpg"
#       },
#       {
#         "image": "https://thecozycook.com/wp-content/uploads/2023/02/Creamy-Chicken-Soup-1.jpg"
#       },
#       {
#         "image": "https://hips.hearstapps.com/hmg-prod/images/chicken-noodle-soup-index-644c2bec1ce0c.jpg?crop=0.6666666666666666xw:1xh;center,top&resize=1200:*"
#       },
#       {
#         "image": "https://thecozycook.com/wp-content/uploads/2022/10/Clam-Chowder-f.jpg"
#       },
#       {
#         "image": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/recipe-image-legacy-id-1217476_10-14b2467.jpg?resize=768,574"
#       },
#       {
#         "image": "https://apinchofsaffron.nl/wp-content/uploads/2021/04/22A9008.jpg"
#       },
#       {
#         "image": "https://www.gimmesomeoven.com/wp-content/uploads/2017/01/Chinese-Hot-and-Sour-Soup-Recipe-1-2.jpg"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2019/04/White-Fish-Soup_6.jpg"
#       },
#       {
#         "image": "https://cookinglsl.com/wp-content/uploads/2018/10/green-bean-soup-social-warfare.jpg"
#       },
#       {
#         "image": "https://www.onceuponachef.com/images/2019/02/french-onion-soup-1.jpg"
#       },
#       {
#         "image": "https://www.allrecipes.com/thmb/d_1S6Av48F5LBfP-Z4W8VTD9U4I=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222331-Chef-Johns-Gazpacho-ddmfs-4x3-2781-67624a59fa4c4375b9149d06f6c32348.jpg"
#       },
#       {
#         "image": "https://www.foodandwine.com/thmb/GWpIhm_82oEDMGenF6rDyN62Qa4=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/FAW-cold-cucumber-soup-yogurt-and-dill-hero-02-19e5f8e4943f478f813c26a977e40a14.jpg"
#       },
#       {
#         "image": "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2022/03/Potato-Leek-Soup-main-1.jpg"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2020/11/Beef-and-Lentil-Soup_9-SQ.jpg"
#       },
#       {
#         "image": "https://assets.epicurious.com/photos/57c5b088d8f441e50948d298/master/w_1000,h_667,c_limit/lettuce-soup.jpg"
#       },
#       {
#         "image": "https://www.aheadofthyme.com/wp-content/uploads/2021/08/minestrone-soup-4.jpg"
#       },
#       {
#         "image": "https://www.mushroomcouncil.com/wp-content/uploads/2017/11/mushroom-soup-3-scaled.jpg"
#       },
#       {
#         "image": "https://www.simplyrecipes.com/thmb/gsbFOv1Kup_Pn-4GvBNDfflC9Do=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2015__09__mulligatawny-soup-horiz-a-1500-bb866c4e3ef145ad8d8f30298b53fe5a.jpg"
#       },
#       {
#         "image": "https://www.thespruceeats.com/thmb/XO_fVSfQdP77TTpR_hw8rXT4yI8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/oxtail-soup-recipe-1809192-hero-01-346f226cecca4eec8a89a87b4e7b7bb5.jpg"
#       },
#       {
#         "image": "https://i0.wp.com/shewearsmanyhats.com/wp-content/uploads/2015/02/oyster-stew-3.jpg"
#       },
#       {
#         "image": "https://www.foodandwine.com/thmb/P24Qe5RX1sv2BhP0TF3Eqck0fwg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/200807xl-chilled-spring-pea-soup-2000-84c33cbf00594576b3693579ac09120a.jpg"
#       },
#       {
#         "image": "https://www.thespruceeats.com/thmb/vtzXYlKcq7ABaVQrx04GUW_0_Nc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/super-easy-pea-and-mint-soup-435604-hero_1-2c7e3183b54b449db87efd8e99244507.jpg"
#       },
#       {
#         "image": "https://sugarspunrun.com/wp-content/uploads/2018/01/potato-soup-recipe-1-of-1.jpg"
#       },
#       {
#         "image": "https://theforkedspoon.com/wp-content/uploads/2015/11/Spinach-Pear-and-Feta-Salad-with-Walnuts-and-Pomegranate-Arils-3.jpg"
#       },
#       {
#         "image": "https://cdn.loveandlemons.com/wp-content/uploads/2015/04/IMG_2015_03_17_03400.jpg"
#       },
#       {
#         "image": "https://www.foodiecrush.com/wp-content/uploads/2018/05/Tuscan-Tuna-and-Arugula-Salad-foodiecrush.com-018.jpg"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2019/01/Prawn-Avocado-Mango-Salad-with-Lime-Dressing_2-SQ.jpg"
#       },
#       {
#         "image": "https://assets.bonappetit.com/photos/624215f8a76f02a99b29518f/1:1/w_2800,h_2800,c_limit/0328-ceasar-salad-lede.jpg"
#       },
#       {
#         "image": "https://www.patagoniaprovisions.com/cdn/shop/articles/recipe-mussel-salad-fennel_1200x.jpg?v=1632779919"
#       },
#       {
#         "image": "https://feelgoodfoodie.net/wp-content/uploads/2017/05/Asian-Noodle-Salad-9.jpg"
#       },
#       {
#         "image": "https://hips.hearstapps.com/thepioneerwoman/wp-content/uploads/2018/06/chicken-waldorf-sald-08.jpg"
#       },
#       {
#         "image": "https://www.crowdedkitchen.com/wp-content/uploads/2019/04/spring-potato-salad-18.jpg"
#       },
#       {
#         "image": "https://i.guim.co.uk/img/media/c11fffa9d3a92bfbcc3453aa811e5d9b9b1fa00f/0_1356_3731_2238/master/3731.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=4dac457577174f9bbfe83d7e97491b85"
#       },
#       {
#         "image": "https://www.inspiredtaste.net/wp-content/uploads/2020/07/Bean-Salad-Recipe-2-1200.jpg"
#       },
#       {
#         "image": "https://static01.nyt.com/images/2019/08/06/dining/lh-tomato-and-white-bean-salad/lh-tomato-and-white-bean-salad-articleLarge-v2.jpg"
#       },
#       {
#         "image": "https://www.southernkitchen.com/gcdn/presto/2021/09/17/NSKT/0cbe7eed-61f2-4276-a6d0-68ed24bc6964-crab__melons__onions_salad.jpg?width=660&height=353&fit=crop&format=pjpg&auto=webp"
#       },
#       {
#         "image": "https://peasandcrayons.com/wp-content/uploads/2019/04/easy-black-bean-salsa-recipe-3.jpg"
#       },
#       {
#         "image": "https://www.acouplecooks.com/wp-content/uploads/2022/03/Tofu-Salad-011.jpg"
#       },
#       {
#         "image": "https://saffronandmore.com.au/wp-content/uploads/2019/11/jewelledPersianRiceSalad-1-1.jpg"
#       },
#       {
#         "image": "https://img.taste.com.au/HL2VG6lc/taste/2016/11/borlotti-bean-salad-28864-1.jpeg"
#       },
#       {
#         "image": "https://hips.hearstapps.com/hmg-prod/images/greek-salad-index-642f292397bbf.jpg?crop=0.6666666666666667xw:1xh;center,top&resize=1200:*"
#       },
#       {
#         "image": "https://www.nospoonnecessary.com/wp-content/uploads/2021/05/Crab-pasta-recipe-crab-meat-pasta-74.jpg"
#       },
#       {
#         "image": "https://www.foodandwine.com/thmb/EhwVcbPf5a7Hr4_v0_zY3xuRRL8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/201307-xl-tuna-and-white-bean-salad-2000-6afa98794c2649eba3af96c3689fb154.jpg"
#       },
#       {
#         "image": "https://jamjarkitchen.com/wp-content/uploads/2021/06/IMG_0103.jpg"
#       },
#       {
#         "image": "https://www.brit.co/media-library/salmon-ni-u00e7oise.jpg?id=34640107&width=760&quality=80"
#       },
#       {
#         "image": "https://grilledcheesesocial.com/wp-content/uploads/2019/07/thai-noodle-salad-grilled-cheese-social-5-500x500.jpg"
#       },
#       {
#         "image": "https://www.strongfitnessmag.com/wp-content/uploads/2023/03/Fish-086091-Edit.jpg"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2015/07/Thai-Beef-Salad_2.jpg"
#       },
#       {
#         "image": "https://www.foodandwine.com/thmb/D8pWfFtuEyoih1EOPUj529Q_1w8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/2012-r-xl-curly-endive-salad-with-bacon-and-poached-eggs-2000-c08e7cf3af4d489e9d9902ce7225dbf5.jpg"
#       },
#       {
#         "image": "https://www.foodandwine.com/thmb/ZRwHglsD9JNlDtGtiXyuj8E2w_U=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/201101-xl-smoked-mackerel-salad-with-crunchy-vegetables-1df6d96682cb44f4abce5efd9d799e69.jpg"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2016/12/Prawn-Cocktails-900px.jpg"
#       },
#       {
#         "image": "https://itsnotcomplicatedrecipes.com/wp-content/uploads/2021/10/Tomato-Onion-Salad-Feature.jpg"
#       },
#       {
#         "image": "http://ripe-life.com/wp-content/uploads/2015/09/pearandgrapesalad4.jpg"
#       },
#       {
#         "image": "https://img.sndimg.com/food/image/upload/q_92,fl_progressive,w_1200,c_scale/v1/img/recipes/43/18/4/wDym2QRZaq8BfSkA14Zw_IMG_0634%20(3).JPG"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2020/09/Brown-Rice-Salad_8.jpg?w=900"
#       },
#       {
#         "image": "https://nourishingamy.com/wp-content/uploads/2019/06/nutty-rice-salad-50.jpg?w=683"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2019/09/Rocket-Salad-with-Balsamic-Dressing_1.jpg"
#       },
#       {
#         "image": "https://www.sainsburysmagazine.co.uk/uploads/media/1800x1800/04/4044-Beetroot-orange-feta-salad-1120.jpg?v=1-0"
#       },
#       {
#         "image": "http://www.jennaseverythingblog.com/wp-content/uploads/2011/07/dsc_0016.jpg?w=640"
#       },
#       {
#         "image": "https://www.littlebroken.com/wp-content/uploads/2020/02/Berry-Spinach-Salad-with-Raspberry-Vinaigrette-15.jpg"
#       },
#       {
#         "image": "https://cardamomandtea.com/wp-content/uploads/2017/05/IMG_7506-1copy.jpg"
#       },
#       {
#         "image": "https://www.eatwell101.com/wp-content/uploads/2020/11/Shredded-Carrot-Salad-recipe.jpg"
#       },
#       {
#         "image": "http://freakingdelish.com/wp-content/uploads/2020/10/1046_201806_Dupree_RealMomNationRecipes_0022-748x1024.jpg"
#       },
#       {
#         "image": "https://d1pfz4jrn3ewag.cloudfront.net/wp-content/uploads/2017/05/26121804/Turnip-Salad-with-Yogurt_.jpg"
#       },
#       {
#         "image": "https://farmersdaughterct.files.wordpress.com/2008/05/0541.jpg"
#       },
#       {
#         "image": "http://thecookingjar.com/wp-content/uploads/2013/10/2013-10-11-15.55.07-2-.jpg"
#       },
#       {
#         "image": "https://www.familyfreshmeals.com/wp-content/uploads/2019/02/Easy-Creamy-Seafood-Lasagna-Family-Fresh-Meals-recipe.jpg"
#       },
#       {
#         "image": "https://i0.wp.com/spainonafork.wpengine.com/wp-content/uploads/2018/02/tunasoup1-22.png?resize=531%2C800&ssl=1"
#       },
#       {
#         "image": "https://n6a7k3g3.rocketcdn.me/wp-content/uploads/2020/04/Stir-Fried-Garlic-Noodles-with-Shrimp-and-Scallops-1200.jpg"
#       },
#       {
#         "image": "https://www.supergoldenbakes.com/wordpress/wp-content/uploads/2019/02/Curried_prawns-2.jpg"
#       },
#       {
#         "image": "https://www.marionskitchen.com/wp-content/uploads/2022/05/Sambal-Sotong-02.jpg"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2021/08/Fish-in-white-wine-cream-sauce_95.jpg"
#       },
#       {
#         "image": "https://www.babaganosh.org/wp-content/uploads/2022/12/fish-loaf-14.jpg"
#       },
#       {
#         "image": "https://cdn.momsdish.com/wp-content/uploads/2021/06/Pan-Fried-Halibut-11.jpg"
#       },
#       {
#         "image": "https://myfoodbook.com.au/sites/default/files/styles/schema_img/public/recipe_photo/Garlic-&-herb-buttery-mash-&-serving_V_10292_WEB.jpg"
#       },
#       {
#         "image": "https://greatcurryrecipes.net/wp-content/uploads/2020/05/fishbalti-480x360.jpg"
#       },
#       {
#         "image": "https://www.foodandwine.com/thmb/gzEsG7jjG3zWj8dKB4xKyA94uso=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/200704-r-xl-grilled-seafood-kebabs-and-orecchiette-with-arugula_0-ec998a595e954c619de181d5886cd50b.jpg"
#       },
#       {
#         "image": "https://images.eatsmarter.com/sites/default/files/styles/300x225-webp/public/plaice-rolls-with-asparagus-479453.jpg"
#       },
#       {
#         "image": "https://shop.luzerne.com/cdn/shop/articles/Luzerne_Blog_Post_1_1066x.png?v=1652776221"
#       },
#       {
#         "image": "https://hips.hearstapps.com/goodhousekeeping-uk/main/embedded/26536/cheesy-smoked-haddock-tart.jpg?crop=0.886xw:0.443xh;0.0489xw,0.331xh&resize=1200:*"
#       },
#       {
#         "image": "http://mydeliciousblog.com/wp-content/uploads/2015/11/Fish-Wellingtons.jpg"
#       },
#       {
#         "image": "https://www.spendwithpennies.com/wp-content/uploads/2017/12/Creamy-Shrimp-Chowder-23.jpg"
#       },
#       {
#         "image": "http://guiltykitchen.com/wp-content/uploads/2010/05/Asparagus-Paneer-Skewers-1.jpg"
#       },
#       {
#         "image": "https://i0.wp.com/stephanieleenutrition.com/wp-content/uploads/2018/01/img_2750.jpg?fit=4352%2C3977&ssl=1"
#       },
#       {
#         "image": "https://www.marthastewart.com/thmb/yp8jOO1aOJldNp0lF7-tW_oYF7g=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/whole-salmon-0397-mla96059_vert-a3a3c98afe6a4c2ebe27ada4611ada33.jpgitokPWHxszGg"
#       },
#       {
#         "image": "https://blog.goodpairdays.com/content/images/2019/08/Depositphotos_150376402_xl-2015.jpg"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2023/05/Creamy-baked-fish-on-potato-gratin_7.jpg"
#       },
#       {
#         "image": "https://tasteasianfood.com/wp-content/uploads/2022/09/squid-curry-recipe-5.jpeg"
#       },
#       {
#         "image": "https://www.cuisinefiend.com/RecipeImages/Prawn%20burgers/burger.jpg"
#       },
#       {
#         "image": "https://redhousespice.com/wp-content/uploads/2022/02/squid-with-salt-and-pepper-seasoning-scaled.jpg"
#       },
#       {
#         "image": "https://i2.wp.com/www.downshiftology.com/wp-content/uploads/2021/01/Shrimp-Fajitas-10-1.jpg"
#       },
#       {
#         "image": "https://img.jamieoliver.com/jamieoliver/recipe-database/oldImages/large/956_36_1434037341.jpg?tr=w-800,h-1066"
#       },
#       {
#         "image": "https://foodiesterminal.com/wp-content/uploads/2019/09/Salmon-Chowder-3-679x1024.jpg"
#       },
#       {
#         "image": "https://www.deliciousmagazine.co.uk/wp-content/uploads/2018/09/519553-1-eng-GB_pan-fried-dover-sole-with-caper-lemon-and-parsley-butter-sauce.jpg"
#       },
#       {
#         "image": "https://realfood.tesco.com/media/images/sole-veronique-0001-h-1d02cc23-790a-4464-9a71-58ece511513a-0-472x310.jpg"
#       },
#       {
#         "image": "https://www.mygourmetconnection.com/wp-content/uploads/seafood-medley-soft-polenta.jpg"
#       },
#       {
#         "image": "https://www.cookingclassy.com/wp-content/uploads/2020/09/ceviche-6.jpg"
#       },
#       {
#         "image": "https://www.olivetomato.com/roasted-sardines/samsung-csc-771/"
#       },
#       {
#         "image": "https://youngsseafood.co.uk/wp-content/uploads/2017/03/Ocean-Pie.jpg"
#       },
#       {
#         "image": "https://www.walterpurkisandsons.com/wp-content/uploads/2015/02/skate-with-black-butter-plate.jpg"
#       },
#       {
#         "image": "https://allthemeals.com/meallogo/36/smoked-haddocks.JPG"
#       },
#       {
#         "image": "https://thecaglediaries.com/wp-content/uploads/2021/10/Stuffed-Crab-Featured-Image.jpg"
#       },
#       {
#         "image": "https://www.deliciousmagazine.co.uk/wp-content/uploads/2010/02/quick-salmon-prawn-lasagne.jpg"
#       },
#       {
#         "image": "https://thewoksoflife.com/wp-content/uploads/2018/07/baked-stuffed-lobster-8.jpg"
#       },
#       {
#         "image": "https://www.wcrf-uk.org/wp-content/uploads/2021/05/Prawn-and-pepper-gumbo-04-R-SQ.jpg"
#       },
#       {
#         "image": "https://img.delicious.com.au/iuY3vYHN/del/2015/10/plum-tarts-21943-1.jpg"
#       },
#       {
#         "image": "https://blackcurrantfoundation.co.uk/wp-content/uploads/2019/04/recipes-pancakes.jpg"
#       },
#       {
#         "image": "https://www.shutterstock.com/image-photo/closeup-thin-pancakes-exotic-fruits-260nw-579865498.jpg"
#       },
#       {
#         "image": "https://bellyfull.net/wp-content/uploads/2023/08/Pan-Fried-Bananas-blog-3.jpg"
#       },
#       {
#         "image": "https://www.daringgourmet.com/wp-content/uploads/2016/12/Spotted-Dick-8-cropped.jpg"
#       },
#       {
#         "image": "https://www.brit.co/media-library/sweet-potato-souffl-u00e9.webp?id=49820607&width=760&quality=80"
#       },
#       {
#         "image": "https://www.ndtv.com/cooks/images/baked%20apples_medium.jpg"
#       },
#       {
#         "image": "https://pastrychefonline.com/wp-content/uploads/2015/01/Hot-Chocolate-Custard-3-425x700.jpg"
#       },
#       {
#         "image": "https://s3-media0.fl.yelpcdn.com/bphoto/O1qzere8_vj9JA_RvDbv-g/258s.jpg"
#       },
#       {
#         "image": "https://www.allrecipes.com/thmb/xhJ9RMLH55EHbNQ7WBfy-hMC83Y=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/9419726-b84ebd467b574ae4af7e995387056e74.jpg"
#       },
#       {
#         "image": "https://www.missallieskitchen.com/wp-content/uploads/2019/10/Caramel-Apple-Tart-1392.jpg"
#       },
#       {
#         "image": "https://static01.nyt.com/images/2018/07/05/fashion/05skin/05skin-videoSixteenByNine3000.jpg?year=2018&h=1688&w=3000&s=ea26c739de516c42d1239a178dcbae8399ccf9a998c62f0cbb7f508d1281865e&k=ZQJBKqZ0VN&tw=1"
#       },
#       {
#         "image": "https://www.brit.co/media-library/sweet-potato-souffl-u00e9.webp?id=49820607&width=760&quality=80"
#       },
#       {
#         "image": "https://www.deliciousmagazine.co.uk/wp-content/uploads/2018/09/447237-1-eng-GB_hazelnut-meringue-cake-768x739.jpg"
#       },
#       {
#         "image": "https://tastesbetterfromscratch.com/wp-content/uploads/2020/07/Orange-Ice-Cream-5.jpg"
#       },
#       {
#         "image": "https://assets.untappd.com/photos/2023_10_18/dd918ea177b337257df72bfa4c13336e_640x640.jpg"
#       },
#       {
#         "image": "https://amandascookin.com/wp-content/uploads/2019/04/lemon-blueberry-trifle-RC-500x500.jpg"
#       },
#       {
#         "image": "https://www.delscookingtwist.com/wp-content/uploads/2021/12/Chocolate-Charlotte_1.jpg"
#       },
#       {
#         "image": "https://natashaskitchen.com/wp-content/uploads/2017/02/Raspberry-Mousse-Cups-2.jpg"
#       },
#       {
#         "image": "https://www.openforvintage.com/cdn/shop/products/2000_1f6d9f3b-c7ed-404c-9ccd-c3382eb77823.jpg?v=1670700853&width=1946"
#       },
#       {
#         "image": "https://icecreamfromscratch.com/wp-content/uploads/2021/06/Marshmallow-Ice-Cream-1.2.jpg"
#       },
#       {
#         "image": "https://www.thefoodiecorner.gr/wp-content/uploads/2014/06/TFC_Grilled-Grapefruit1.jpg"
#       },
#       {
#         "image": "https://www.superhealthykids.com/wp-content/uploads/2015/06/healthy-fruit-fondue-14-480x270.jpg"
#       },
#       {
#         "image": "https://oliveandvyne.com/cdn/shop/files/CucumberlimeSalad.jpg?v=1692041311&width=1946"
#       },
#       {
#         "image": "https://m.media-amazon.com/images/I/71zDauabPEL.jpg"
#       },
#       {
#         "image": "https://toriavey.com/images/2011/09/TOA87_01.jpeg"
#       },
#       {
#         "image": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/recipe-image-legacy-id-560848_11-41a0359.jpg?quality=90&resize=440,400"
#       },
#       {
#         "image": "https://www.7x7.com/media-library/the-famous-zuni-caf-u00e9-roast-chicken.jpg?id=18842288&width=776&quality=80"
#       },
#       {
#         "image": "https://opengraph.githubassets.com/ee290d5547e70918d3592d1a7a3cc980ecc7130dd59f54203e9d9df3f94cd513/Nathansbud/Jeopardizer"
#       },
#       {
#         "image": "https://discovercaliforniawines.com/wp-content/uploads/2016/03/2016_1_BAKED_PEARS_WINEc-California-Wine-Institute.jpg"
#       },
#       {
#         "image": "http://www.foodiecrush.com/wp-content/uploads/2016/05/Cucumber-Basil-and-Watermelon-Salad-foodiecrush.com-011.jpg"
#       },
#       {
#         "image": "https://pacificcoastproducers.com/wp-content/uploads/2016/06/Mandarin-Bowl.png"
#       },
#       {
#         "image": "https://tastesbetterfromscratch.com/wp-content/uploads/2023/03/Coconut-Cake-1.jpg"
#       },
#       {
#         "image": "https://www.mybakingaddiction.com/wp-content/uploads/2022/03/cherry-turnover-cut-in-half.jpg"
#       },
#       {
#         "image": "http://wtop.com/wp-content/uploads/2017/07/harris_comp-727x485.jpg"
#       },
#       {
#         "image": "https://hips.hearstapps.com/hmg-prod/images/sticky-plum-tart-64c8d33f05a74.jpg"
#       },
#       {
#         "image": "https://i0.wp.com/twimii.com/wp-content/uploads/2018/11/feature-fruit-salad-cake.jpg?fit=1200%2C600"
#       },
#       {
#         "image": "https://www.thespruceeats.com/thmb/48MwYE_xzZnw31K4_Z81fw0FxrA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/traditional-scottish-dundee-cake-recipe-435067-hero-02-41514a0a054d486990fb3910fc7ec1b6.jpg"
#       },
#       {
#         "image": "https://www.mybakingaddiction.com/wp-content/uploads/2017/06/bite-from-banana-cake-700x1050.jpg"
#       },
#       {
#         "image": "https://img.taste.com.au/x2_EfxgS/taste/2016/11/brandy-chocolate-cake-22776-1.jpeg"
#       },
#       {
#         "image": "https://www.christinascucina.com/wp-content/uploads/2014/04/fullsizeoutput_d35e-720x540.jpeg"
#       },
#       {
#         "image": "https://sallysbakingaddiction.com/wp-content/uploads/2013/04/triple-chocolate-cake-4.jpg"
#       },
#       {
#         "image": "https://hips.hearstapps.com/hmg-prod/images/20190503-delish-blt-ehg-337-1593548719.jpg"
#       },
#       {
#         "image": "https://www.missionfoods.com/wp-content/uploads/2022/06/margherita-flatbread-pizza.jpg"
#       },
#       {
#         "image": "https://www.twopeasandtheirpod.com/wp-content/uploads/2023/08/Chicken-Caesar-Wraps-14.jpg"
#       },
#       {
#         "image": "https://images.ctfassets.net/j8tkpy1gjhi5/NtsKuEzyidPqHQ4qzhzHP/ad0a7e75bdaeae01e082027f98f69bcd/classic-grilled-cheese-hero.jpg"
#       },
#       {
#         "image": "https://www.foodandwine.com/thmb/Pd-Q1_aCb3WkSt7Dq49cDIRZS9k=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/201310-xl-spicy-guacamole-recipe-2000-68431ba5dc474dce895d12bb4c3b0ccc.jpg"
#       },
#       {
#         "image": "https://sugarspunrun.com/wp-content/uploads/2021/07/Homemade-Mozzarella-Sticks-Recipe-1-of-1-500x500.jpg"
#       },
#       {
#         "image": "https://myfoodstory.com/wp-content/uploads/2015/09/no-brainer-loaded-nachos-platter-recipe.1024x1024-1-500x375.jpg"
#       },
#       {
#         "image": "https://www.foodandwine.com/thmb/cLAsJswKgpqst5XsLvd16vsrzhg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/200306-r-xl-classic-beef-burgers-2000-863d4559081b41f78efe87e2e8062caf.jpg"
#       },
#       {
#         "image": "https://assets.bonappetit.com/photos/62b5fec6094fcaa09e5a30ea/3:2/w_4307,h_2871,c_limit/BA0822chintan06.jpg"
#       },
#       {
#         "image": "https://sallysbakingaddiction.com/wp-content/uploads/2018/07/best-black-bean-burgers-2.jpg"
#       },
#       {
#         "image": "https://images-gmi-pmc.edge-generalmills.com/144e3e98-69a3-496a-bdf0-2a25164dd4ac.jpg"
#       },
#       {
#         "image": "https://cdn.loveandlemons.com/wp-content/uploads/2019/06/portabello-mushroom-burger-recipe.jpg"
#       },
#       {
#         "image": "https://images.prismic.io/eataly-us/ed3fcec7-7994-426d-a5e4-a24be5a95afd_pizza-recipe-main.jpg?auto=compress,format"
#       },
#       {
#         "image": "https://s23209.pcdn.co/wp-content/uploads/2021/10/BBQ-Chicken-PizzaIMG_0027-760x1140.jpg"
#       },
#       {
#         "image": "https://sundayfoodapprentice.files.wordpress.com/2014/04/dscn4367.jpg"
#       },
#       {
#         "image": "https://www.acozykitchen.com/wp-content/uploads/2021/10/MeatLoversPizza-8-1.jpg"
#       },
#       {
#         "image": "http://ciaoflorentina.com/wp-content/uploads/2015/09/Ricotta-Spinach-Pizza-Recipe-1.jpg"
#       },
#       {
#         "image": "https://sallysbakingaddiction.com/wp-content/uploads/2014/08/It-doesnt-get-much-better-than-Homemade-Hawaiian-Pizza.-Tropical-paradise-for-dinner-2.jpg"
#       },
#       {
#         "image": "https://thealmondeater.com/wp-content/uploads/2020/06/Sun-Dried-Tomato-Pizza-1-7.jpg"
#       },
#       {
#         "image": "https://staticcookist.akamaized.net/wp-content/uploads/sites/22/2022/07/Hot-dogs-10-1200x675.jpg"
#       },
#       {
#         "image": "https://www.joyousapron.com/wp-content/uploads/2023/04/chili-cheese-dog-sq.jpg"
#       },
#       {
#         "image": "https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/stray-dogs-stroll-along-the-bruckner-new-york-daily-news-archive.jpg"
#       },
#       {
#         "image": "https://www.charbroil.com/media/ctm//I/M/IMG_8323_1__1.jpg.jpeg"
#       },
#       {
#         "image": "https://hips.hearstapps.com/hmg-prod/images/190130-chicken-shwarma-horizontal-1549421250.png?crop=0.8893333333333334xw:1xh;center,top&resize=1200:*"
#       },
#       {
#         "image": "https://www.oliveandmango.com/images/uploads/2022_03_18_beef_shawarma_2.jpg"
#       },
#       {
#         "image": "https://www.recipetineats.com/wp-content/uploads/2018/01/Lamb-Shawarma_4.jpg"
#       },
#       {
#         "image": "http://theherbeevore.com/wp-content/uploads/2021/03/wp-16146583179017563948739731921138.jpg"
#       },
#       {
#         "image": "https://img.hellofresh.com/f_auto,fl_lossy,h_640,q_auto,w_1200/hellofresh_s3/image/classic-beef-tacos-cf4226b3.jpg"
#       },
#       {
#         "image": "https://tatyanaseverydayfood.com/wp-content/uploads/2022/08/Easy-Grilled-Chicken-Tacos-Recipe-1.jpg"
#       },
#       {
#         "image": "https://www.shelikesfood.com/wp-content/uploads/2019/05/Black-Bean-Tacos-with-Summer-Vegetables-4847.jpg"
#       },
#       {
#         "image": "https://thecozyapron.com/wp-content/uploads/2020/01/beef-goulash_thecozyapron_1.jpg"
#       },
#       {
#         "image": "https://s23209.pcdn.co/wp-content/uploads/2019/10/Easy-Steak-FajitasIMG_0418.jpg"
#       },
#       {
#         "image": "https://i0.wp.com/bakeatmidnite.com/wp-content/uploads/2014/10/orange-beef-fire-peppers-43-o-1024x768.jpg"
#       },
#       {
#         "image": "https://media-cdn2.greatbritishchefs.com/media/l3ylkds3/img28470.jpg"
#       },
#       {
#         "image": "https://www.eatingwell.com/thmb/0sYzpAydhffO9boYQzdqsuzgXN0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/1606p34-spicy-thai-red-curry-beef-2000-0e0f127c288d4cfabef0cc6b0c3b2408.jpg"
#       },
#       {
#         "image": "https://www.cuisinefiend.com/RecipeImages/Beef%20roulade/beef-porcini-2.jpg"
#       },
#       {
#         "image": "https://hips.hearstapps.com/hmg-prod/images/beef-wellington-index-65149c4448c77.jpg?crop=0.6666666666666667xw:1xh;center,top&resize=1200:*"
#       },
#       {
#         "image": "https://www.kitchensanctuary.com/wp-content/uploads/2018/04/Crispy-Chilli-Beef-square-FS-18-500x500.jpg"
#       },
#       {
#         "image": "https://www.gimmesomeoven.com/wp-content/uploads/2020/10/Beef-Stroganoff-Recipe-9.jpg"
#       },
#       {
#         "image": "https://img.delicious.com.au/KXLipn70/del/2021/02/beef-chilli-tortillas-145539-2.jpg"
#       },
#       {
#         "image": "https://img.taste.com.au/WhmZngzk/taste/2017/07/lean-beef-126586-2.jpg"
#       },
#       {
#         "image": "https://i.ytimg.com/vi/0c6WPIAMAf0/maxresdefault.jpg"
#       },
#       {
#         "image": "https://cdn.mos.cms.futurecdn.net/inTEXPLhSDr8sUhS2h7ZBa.jpg"
#       },
#       {
#         "image": "https://cdn.apartmenttherapy.info/image/upload/f_jpg,q_auto:eco,c_fill,g_auto,w_1500,ar_1:1/k%2FPhoto%2FRecipe%20Ramp%20Up%2F2021-09-Daube-Beef%2FDaube_Beef_1"
#       },
#       {
#         "image": "https://opengraph.githubassets.com/39a7e56a0e55927c52a5ebed7aa7996a13f2ace487d5705b9a08ce514b10be10/openai/finetune-transformer-lm"
#       },
#       {
#         "image": "https://img.jamieoliver.com/jamieoliver/recipe-database/63138359.jpg?tr=w-800,h-1066"
#       },
#       {
#         "image": "https://www.spendwithpennies.com/wp-content/uploads/2022/12/1200-The-Best-Meatloaf-Recipe-SpendWithPennies.jpg"
#       },
#       {
#         "image": "https://img.jamieoliver.com/home/wp-content/uploads/2014/11/beefstewwithcarrots630x420.jpg"
#       },
#       {
#         "image": "http://embed.widencdn.net/img/beef/9mqeetszjr/exact/smoked-steak-skewers-with-tomatoes-onions-and-olives-tablescape.tif?keep=c&u=7fueml"
#       },
#       {
#         "image": "https://blog.fitbit.com/wp-content/uploads/2018/04/0410-beef-burger-recipes-Blog-Hero.jpg"
#       },
#       {
#         "image": "https://hips.hearstapps.com/hmg-prod/images/delish-191217-veal-marsala-152-landscape-pf-1-1578325633.jpg?crop=0.8891228070175439xw:1xh;center,top&resize=1200:*"
#       },
#       {
#         "image": "https://img.sndimg.com/food/image/upload/q_92,fl_progressive,w_1200,c_scale/v1/img/recipes/58/09/3/picYdHDSP.jpg"
#       },
#       {
#         "image": "https://images.themodernproper.com/billowy-turkey/production/posts/2020/Herb-crusted-Pork-Tenderloin-with-Port-Wine-Sauce-14.jpg?w=1200&h=1800&q=82&fm=jpg&fit=crop&dm=1608040544&s=20c3361cd0a0bfcc62919a67dfb2d31c"
#       },
#       {
#         "image": "https://www.savoryonline.com/app/uploads/recipes/165170/honey-and-gingerglazed-ham-640x640-c-default.jpg"
#       },
#       {
#         "image": "https://img.jamieoliver.com/jamieoliver/recipe-database/Do0XkKqpKZ-9UQr26bkEjY.jpg?tr=w-800,h-1066"
#       },
#       {
#         "image": "https://c.recipeland.com/images/r/21484/4ef73f3caf68e306fe5b_1024.jpg"
#       },
#       {
#         "image": "https://4.bp.blogspot.com/_tJBtn57VtWI/THFNqe1Tw6I/AAAAAAAAC2E/YNNxGDVxJKw/s1600/DSC04317.jpg"
#       },
#       {
#         "image": "https://www.theseoldcookbooks.com/wp-content/uploads/2019/01/Baked-Cranberry-Pork-Chops-14.jpg"
#       },
#       {
#         "image": "https://madaboutfood.co/wp-content/uploads/2019/08/DSC02699-scaled.jpg"
#       },
#       {
#         "image": "https://imgur.com/a/aX3mFnG"
#       },
#       {
#         "image": "https://thehappyfoodie.co.uk/wp-content/uploads/2021/08/pork_pork_with_black_bean_sauce_complete_chinese_coo_s900x0_c2207x1290_l0x904.jpg"
#       }
# ]

# rec_id = 1
# for col in f:
#     print(data_image_names[rec_id-1]['image'], rec_id-1)
#     dt = {
#         'model': 'recipes.RecipesImages',
#         'fields': {
#             'image': data_image_names[rec_id-1]['image'],
#             'recipe_id': rec_id
#         }
#     }
#     rec_id += 1
#     data.append(dt)

with open('fixtures/recipes.json', 'w') as f:
    json.dump(data, f)
