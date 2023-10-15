from rest_framework import generics, status, views
from recipes import serializers
from rest_framework.permissions import IsAuthenticated
from recipes import models
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Max, Count, Avg, F, Subquery
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from KitchenGuru import settings
import openai


openai.api_key = settings.CHATGPT_API_KEY

class CreateRecipeView(generics.CreateAPIView):
    serializer_class = serializers.CreateRecipeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            recipe = serializer.save(created_by=request.user)
            return Response({'message': 'Recipe created!'}, status=status.HTTP_201_CREATED)


class CreateReviewView(generics.CreateAPIView):
    serializer_class = serializers.RecipeReviewSerializer
    permission_classes = [IsAuthenticated]
        
    def create(self, request):
        data = request.data
        user = request.user
        recipe = models.Recipes.objects.get(title=data["title"])
        data.pop("title")
        review = models.Review.objects.create(
            recipes=recipe, 
            user=user, 
            rating=data["rating"], 
            text=data["text"], 
            review_added=datetime.now())
        serializer = serializers.RecipeReviewSerializer(review, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetRecipes(generics.ListAPIView):
    serializer_class = serializers.GetRecipesSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category:
            return models.Recipes.objects.filter(category=category).prefetch_related('images')
        return models.Recipes.objects.all().prefetch_related('images')
    

class GetRecipe(generics.ListAPIView):
    serializer_class = serializers.GetRecipeSerializer

    def get_queryset(self):
        recipe_id = self.request.query_params.get('recipe_id', None)
        if recipe_id:
            return models.Recipes.objects.filter(id=recipe_id).prefetch_related('images')
        raise models.Recipes.DoesNotExist('Recipe id was not provided!')


class GetIngredients(generics.ListAPIView):
    queryset = models.Ingredients.objects.all()
    serializer_class = serializers.GetIngredientsSerializer
    pagination_class = None


class AddFavorites(generics.CreateAPIView):
    serializer_class = serializers.AddFavoritesSerialier
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        recipe_id = request.data['recipe_id']
        try:
            recipe = models.Recipes.objects.get(id=recipe_id)
        except models.Recipes.DoesNotExist:
            return Response({'message': 'This recipe does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        favorites_exists = models.Favorites.objects.filter(user=user, recipe=recipe).exists()

        if favorites_exists:
            return Response({'message': f'This recipe was already added to favorites for user_id={user.id}!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            favorites_object = models.Favorites.objects.create(user=user, recipe=recipe)

            return Response({
                'message': 'The recipe was added to favorites!',
                'user_id': user.id,
                'recipes_id': recipe_id
            }, status=status.HTTP_201_CREATED)
        

class GetFavorites(generics.ListAPIView):
    serializer_class = serializers.GetRecipesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        favorites_entries = models.Favorites.objects.filter(user_id=user_id)
        recipe_ids = favorites_entries.values('recipe_id')
        return models.Recipes.objects.filter(id__in=Subquery(recipe_ids)).prefetch_related('images')
    
    def list(self, request):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({'message': 'This user has no favorite recipes'}, status=status.HTTP_404_NOT_FOUND)
        
        return super(GetFavorites, self).list(request)
        
        
class FilteringView(generics.ListAPIView):
    serializer_class = serializers.FilterRecipesSerializer
    ordering_fields = ['favorites_count', 'average_rating', 'review_count']

    def list(self, request):
        queryset = models.Recipes.objects.annotate(
                favorites_count=Count('favorites', distinct=True),
                review_count=Count('review', distinct=True),
                average_rating=Avg('review__rating')
            )
        db_max_duration = models.Recipes.objects.aggregate(db_max_duration=Max('duration'))['db_max_duration']

        sort_by = self.request.query_params.get('sort_by')
        categories = self.request.query_params.get('category')
        
        try:
            duration_min = int(self.request.query_params.get('duration_min', 0))
            duration_max = int(self.request.query_params.get('duration_max', db_max_duration))
        except ValueError:
            return Response({"message": "Duration should be a valid number."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not (0 <= duration_min <= duration_max <= db_max_duration):
            return Response({"message": "Invalid duration parameters."}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = queryset.filter(duration__gte=duration_min, duration__lte=duration_max)
        
        if categories:
            categories_list = categories.split(', ')
            queryset = queryset.filter(category__in=categories_list)
        
        order_by_field = sort_by if sort_by in self.ordering_fields else self.ordering_fields[0]
        queryset = queryset.order_by('-' + order_by_field)

        if not queryset.exists():
            return Response({"message": "There are no recipes that match these filters"}, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)



class SearchRecipesView(generics.ListAPIView):
    serializer_class = serializers.SearchRecipesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    def list(self, request):
        queryset = super().filter_queryset(models.Recipes.objects.all())
        try:
            user_ingredients = request.query_params.get('ingredients').split(', ')
            user_ingredients = [ingredient.strip() for ingredient in user_ingredients if ingredient != '']
        except AttributeError:
            return Response({"message": "Invalid URL format"}, status=status.HTTP_400_BAD_REQUEST)

        matched_recipes = []

        for recipe in queryset:
            recipe_ingredients = recipe.ingredient_tags.split(', ')
            matching_ingredients = set(user_ingredients).intersection(recipe_ingredients)
            if len(matching_ingredients) > 0:
                matched_recipes.append({
                'recipe': recipe,
                'matching_ingredients': ', '.join(ingredient for ingredient in matching_ingredients).strip()
                })
        if matched_recipes:
            sorted_recipes = sorted(matched_recipes, key=lambda x: len(x['matching_ingredients']), reverse=True)
        else:
            return Response({"message": "No recipes have the ingredients provided"}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(sorted_recipes)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


def send_code_to_api(categories, ingredients):
    try:
        res = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a food expert."},
                {"role": "user", "content": f"Provide me a recipe from the categories {categories} that I can make with ingredients such as {ingredients} ?"},
            ]
        )
        return res["choices"][0]["message"]["content"], status.HTTP_200_OK
    except openai.error.AuthenticationError:
        return "Invalid API key for OpenAI.", status.HTTP_401_UNAUTHORIZED
    except KeyError:
        return "Unexpected response format from OpenAI.", status.HTTP_500_INTERNAL_SERVER_ERROR
    except:
        return "There was an issue creating the recipe.", status.HTTP_500_INTERNAL_SERVER_ERROR


class AIRecipesView(views.APIView):
    def post(self, request):
        user_categories = request.data.get('categories', [])
        user_ingredients = request.data.get('ingredients', None)
        
        if user_categories and user_ingredients:
            gpt_response, http_status = send_code_to_api(user_categories, user_ingredients)
            return Response({"message": gpt_response}, status=http_status)
        return Response({"message": "Invalid input."}, status=status.HTTP_400_BAD_REQUEST)


class FilterRecipesView(generics.ListAPIView):
    queryset = models.Recipes.objects.all()
    serializer = serializers.GetRecipesSerializer


