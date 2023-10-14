from rest_framework import generics, status, views
from rest_framework.response import Response
from KitchenGuru import settings
import openai

openai.api_key = settings.CHATGPT_API_KEY

def send_code_to_api(categories, ingredients):
    res = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a food expert."},
            {"role": "user", "content": f"Provide me a recipe from the categories {categories} that I can make with ingredients such as {ingredients} ?"},
        ]
    )
    return res["choices"][0]["message"]["content"]


class AIRecipesView(views.APIView):
    def post(self, request):
        user_categories = request.data.get('categories', [])
        user_ingredients = request.data.get('ingredients', None)
        
        if user_categories and user_ingredients:
            gpt_response = send_code_to_api(user_categories, user_ingredients)
            return Response({"message": gpt_response}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid input."}, status=status.HTTP_400_BAD_REQUEST)

