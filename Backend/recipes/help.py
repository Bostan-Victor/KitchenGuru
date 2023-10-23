import random
from datetime import datetime, timedelta
import json

def generate_review_text(rating):
    rating_texts = {
        "1": "This recipe is awful!",
        "2": "This recipe isn't great.",
        "3": "This recipe is okay.",
        "4": "This recipe is nice!",
        "5": "This recipe is amazing!"
    }
    return rating_texts[str(rating)]

def random_date_in_range(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

start_date = datetime(2023, 9, 1)
end_date = datetime(2023, 10, 19)

used_combinations = set()

reviews = []
for _ in range(500):
    user_id = str(random.randint(1, 8))
    recipes_id = str(random.randint(1, 217))
    while (user_id, recipes_id) in used_combinations:
        user_id = str(random.randint(1, 8))
        recipes_id = str(random.randint(1, 217))
    used_combinations.add((user_id, recipes_id))

    rating = str(random.randint(1, 5))
    review_text = generate_review_text(rating)
    review_added = random_date_in_range(start_date, end_date).strftime('%Y-%m-%d %H:%M:%S.%f')

    review = {
        "model": "recipes.Review",
        "fields": {
            "recipes_id": recipes_id,
            "user_id": user_id,
            "rating": rating,
            "text": review_text,
            "review_added": review_added
        }
    }
    reviews.append(review)


with open('reviews.json', 'w') as f:
    json.dump(reviews, f, indent=4)

