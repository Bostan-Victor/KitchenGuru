from rest_framework import generics, status, views, permissions, exceptions
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
from django.http import Http404
import os
import logging
import logging.config


openai.api_key = settings.CHATGPT_API_KEY
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'KitchenGuru', 'user_activity.conf')
logging.config.fileConfig(config_path, disable_existing_loggers=False)
USER_LOGGER = logging.getLogger('user')
config_path = os.path.join(current_dir, '..', 'KitchenGuru', 'system_activity.conf')
logging.config.fileConfig(config_path, disable_existing_loggers=False)
SYSTEM_LOGGER = logging.getLogger('activity')


class CreateRecipeView(generics.CreateAPIView):
    serializer_class = serializers.CreateRecipeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        USER_LOGGER.info(f'User {request.user} is attempting to create a recipe with data: {request.data} from remote address {request.META.get("REMOTE_ADDR")}')
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            recipe = serializer.save(created_by=request.user)
            USER_LOGGER.info(f'User {request.user} successfully created a recipe with id: {recipe.id}')
            SYSTEM_LOGGER.info(f"Recipe with id {recipe.id} was created by the user with the id {request.user.id}")
            return Response({'message': 'Recipe created!'}, status=status.HTTP_201_CREATED)
        else:
            USER_LOGGER.warning(f'User {request.user} submitted invalid data: {serializer.errors}')
            return Response({'message': 'Error creating the recipe!'}, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteRecipeView(generics.DestroyAPIView):
    serializer_class = serializers.RecipeIdSerialier
    permission_classes = [IsAuthenticated]

    
    def delete(self, request):
        user = request.user
        recipe_id = request.data['recipe_id']
        USER_LOGGER.info(f'User {request.user} is attempting to delete a recipe with id: {recipe_id} from remote address {request.META.get("REMOTE_ADDR")}')

        try:
            models.Recipes.objects.get(id=recipe_id, created_by_id=user.id).delete()
            USER_LOGGER.info(f'User {request.user} successfully deleted the recipe with id: {recipe_id}')
            return Response({'message': 'Recipe deleted succesfully!'}, status=status.HTTP_200_OK)
        except models.Recipes.DoesNotExist:
            USER_LOGGER.warning(f'User {request.user} failed to delete recipe with id: {recipe_id} - Not owned by this user')
            return Response({'message': 'This user did not create this recipe!'}, status=status.HTTP_404_NOT_FOUND)


class CreateReviewView(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        recipe_id = self.request.query_params.get('recipe_id', None)
        recipe = models.Recipes.objects.get(id=recipe_id)
        return models.Review.objects.filter(recipes=recipe)
        
    def create(self, request):
        data = request.data
        user = request.user
        USER_LOGGER.info(f'User {request.user} is attempting to create a review for recipe: {request.data.get("id")} from remote address {request.META.get("REMOTE_ADDR")}')
        try:
            recipe = models.Recipes.objects.get(id=data["id"])
        except models.Recipes.DoesNotExist:
            return Response({'message': 'This recipe does not exist!'}, status=status.HTTP_404_NOT_FOUND)
    
        review_exists = models.Review.objects.filter(user=user, recipes=recipe).exists()

        if review_exists:
            USER_LOGGER.warning(f'User {request.user} tried to create another review for recipe: {request.data.get("id")}')
            SYSTEM_LOGGER.warning(f"User {request.user.id} attempted to submit multiple reviews for recipe {data['id']}")
            return Response({'message': f'The user already submitted a review for this recipe!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            review = models.Review.objects.create(
                recipes=recipe, 
                user=user, 
                rating=data["rating"], 
                text=data["text"], 
                review_added=datetime.now())
            serializer = self.get_serializer(review, many=False)
            USER_LOGGER.info(f'User {request.user} successfully created a review for recipe: {request.data.get("id")}')
            SYSTEM_LOGGER.info(f"Review created successfully for recipe {data['id']} by user {request.user.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UpdateReviewView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'recipes_id'

    def get_queryset(self):
        recipes_id = self.kwargs.get('recipes_id')
        if self.request.user.is_superuser:
            user_id = self.request.data.get("user_id")
            if not user_id:
                USER_LOGGER.warning(f"Superuser {self.request.user.username} tried to update a review without providing a 'user_id'.")
                raise exceptions.ValidationError({"message": "The field 'user_id' is required for superusers."})

            reviews = self.queryset.filter(user_id=user_id, recipes_id=recipes_id)
            if not reviews.exists():
                USER_LOGGER.info(f"Superuser {self.request.user.username} tried to fetch a non-existent review for user_id: {user_id} and recipes_id: {recipes_id}.")
                raise exceptions.ValidationError({"message": "No reviews found for provided user_id and recipes_id."})
            return reviews

        else:
            reviews = self.queryset.filter(user_id=self.request.user.id, recipes_id=recipes_id)
            if not reviews.exists():
                USER_LOGGER.info(f"User {self.request.user.username} tried to fetch a non-existent review for recipes_id: {recipes_id}.")
                SYSTEM_LOGGER.warning(f"User {self.request.user.id} tried accessing a non-existing review for recipe {recipes_id}")
                raise exceptions.ValidationError({"message": "No reviews found for the authenticated user and provided recipes_id."})
            return reviews

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return serializers.AdminReviewSerializer
        return serializers.UserReviewSerializer


class GetRecipes(generics.ListAPIView):
    serializer_class = serializers.GetRecipesSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category:
            return models.Recipes.objects.filter(category=category).prefetch_related('images')
        return models.Recipes.objects.all().prefetch_related('images')
    

class GetRecipe(generics.ListAPIView):
    serializer_class = serializers.GetRecipesSerializer

    def list(self, request):
        is_favorite = False
        user = request.user

        recipe_id = request.query_params.get('recipe_id', None)
        if not recipe_id:
           USER_LOGGER.warning(f"{user.username if user.is_authenticated else 'Anonymous user'} attempted to retrieve a recipe without providing a recipe_id.")
           return Response({'message': 'Recipe id was not provided!'}, status=status.HTTP_400_NOT_FOUND)
        try:
            recipe = models.Recipes.objects.get(id=recipe_id)
        except:
            USER_LOGGER.warning(f"{user.username if user.is_authenticated else 'Anonymous user'} attempted to retrieve non-existent recipe with id: {recipe_id}.")
            SYSTEM_LOGGER.error(f"Attempted to access non-existent recipe with id {recipe_id}")
            return Response({'message': 'Recipe with the provided id was not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        if user.is_authenticated:
            if models.Favorites.objects.filter(recipe_id=recipe.id, user_id=user.id).exists():
                is_favorite = True

        serializer = self.get_serializer(recipe)
        data = {
            'recipe': serializer.data,
            'is_favorite': is_favorite
        }
        USER_LOGGER.info(f"{user.username if user.is_authenticated else 'Anonymous user'} retrieved recipe with id: {recipe_id}. Favorite status: {is_favorite}")
        return Response(data)


class GetIngredients(generics.ListAPIView):
    queryset = models.Ingredients.objects.all()
    serializer_class = serializers.GetIngredientsSerializer
    pagination_class = None


class AddFavorites(generics.CreateAPIView):
    serializer_class = serializers.RecipeIdSerialier
    permission_classes = [IsAuthenticated]


    def create(self, request):
        user = request.user
        recipe_id = request.data['recipe_id']
        try:
            recipe = models.Recipes.objects.get(id=recipe_id)
        except models.Recipes.DoesNotExist:
            USER_LOGGER.warning(f"User {user.username} tried to add non-existent recipe with id: {recipe_id} to favorites.")
            return Response({'message': 'This recipe does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        favorites_exists = models.Favorites.objects.filter(user=user, recipe=recipe).exists()

        if favorites_exists:
            USER_LOGGER.info(f"User {user.username} attempted to add recipe with id: {recipe_id} to favorites, but it's already in favorites.")
            SYSTEM_LOGGER.warning(f"User {user.id} attempted to add already favorited recipe {recipe_id}")
            return Response({'message': f'This recipe was already added to favorites for user_id={user.id}!'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            favorites_object = models.Favorites.objects.create(user=user, recipe=recipe)
            USER_LOGGER.info(f"User {user.username} added recipe with id: {recipe_id} to favorites.")
            SYSTEM_LOGGER.info(f"User {user.id} added recipe with id {recipe.id} to his list of favorites.")
            return Response({
                'message': 'The recipe was added to favorites!',
                'user_id': user.id,
                'recipes_id': recipe_id
            }, status=status.HTTP_201_CREATED)
        

class DeleteFavoritesView(generics.DestroyAPIView):
    serializer_class = serializers.RecipeIdSerialier
    permission_classes = [IsAuthenticated]


    def delete(self, request):
        user = request.user
        recipe_id = request.data['recipe_id']

        try:
            models.Favorites.objects.get(user_id=user.id, recipe_id=recipe_id).delete()
            USER_LOGGER.info(f"User {user.username} deleted recipe with id: {recipe_id} from favorites.")
            SYSTEM_LOGGER.info(f"User {user.id} deleted the recipe with id {recipe_id} from his list of favorites.")
            return Response({'message': 'Recipe deleted from favorites!'}, status=status.HTTP_200_OK)
        except models.Favorites.DoesNotExist:
            USER_LOGGER.info(f"User {user.username} failed to delete recipe with id: {recipe_id} from favorites, due to it not being there originally.")
            SYSTEM_LOGGER.warning(f"User {user.id} tried deleting a non-favorited recipe with id {recipe_id}")
            return Response({'message': 'The recipe is not in this users favorites!'}, status=status.HTTP_404_NOT_FOUND)
        

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
            SYSTEM_LOGGER.error(f"Invalid duration provided by user {self.request.user.id}")
            return Response({"message": "Duration should be a valid number."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not (0 <= duration_min <= duration_max <= db_max_duration):
            return Response({"message": "Invalid duration parameters."}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = queryset.filter(duration__gte=duration_min, duration__lte=duration_max)
        
        if categories:
            categories_list = categories.split(',')
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
            SYSTEM_LOGGER.error(f"User {self.request.user.id} provided malformed URL")
            return Response({"message": "Invalid URL format"}, status=status.HTTP_400_BAD_REQUEST)

        matched_recipes = []

        for recipe in queryset:
            recipe_ingredients = recipe.ingredient_tags.split(', ')
            matching_ingredients = set(recipe_ingredients).intersection(set(user_ingredients))
            missing_ingredients = set(recipe_ingredients).difference(set(user_ingredients))
            if len(matching_ingredients) > 0:
                matched_recipes.append({
                'recipe': recipe,
                'matching_ingredients': ', '.join(ingredient for ingredient in matching_ingredients).strip(),
                'missing_ingredients': ', '.join(ingredient for ingredient in missing_ingredients).strip()
                })
        if matched_recipes:
            sorted_recipes = sorted(matched_recipes, key=lambda x: len(x['missing_ingredients']))
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
                {"role": "user", "content": f'''Provide me a recipe from the categories {categories} that I can make with ingredients such as {ingredients} ? 
                 Separate the title, ingredients and instructions in the response and make sure that the response starts with
                 Title: title of the recipe\\n'''},
            ]
        )
        response_message = res["choices"][0]["message"]["content"]
        if response_message[:7] == "Title: ":
            recipe_title = response_message.split("\n")[0][7:]
            recipe_image_url = create_ai_recipe_image(recipe_title)
            return {"message": response_message, "image_url": recipe_image_url}, status.HTTP_200_OK
        else:
            return {"message": "Unexpected response format from OpenAI."}, status.HTTP_500_INTERNAL_SERVER_ERROR
    except openai.error.AuthenticationError:
        SYSTEM_LOGGER.error("Invalid API key for OpenAI")
        return {"message": "Invalid API key for OpenAI."}, status.HTTP_401_UNAUTHORIZED
    except openai.error.RateLimitError:
        SYSTEM_LOGGER.warning("Rate limit reached for requests to OpenAI")
        return {"message": "Rate limit reached for requests."}, status.HTTP_429_TOO_MANY_REQUESTS
    except (KeyError, IndexError):
        SYSTEM_LOGGER.warning("Unexpected response format from OpenAI")
        return {"message": "Unexpected response format from OpenAI."}, status.HTTP_500_INTERNAL_SERVER_ERROR
    except openai.error.ServiceUnavailableError:
        SYSTEM_LOGGER.error("Issue with the OpenAI API servers")
        return {"message": "Issue with the OpenAI API servers."}, status.HTTP_503_SERVICE_UNAVAILABLE


def create_ai_recipe_image(recipe_title):
    response = openai.Image.create(
        prompt=str(recipe_title),
        n=1,
        size="512x512"
    )
    return response['data'][0]['url']


class AIRecipesView(views.APIView):
    def post(self, request):
        user_categories = request.data.get('categories', [])
        user_ingredients = request.data.get('ingredients', None)
        
        if user_categories and user_ingredients:
            gpt_response, http_status = send_code_to_api(user_categories, user_ingredients)
            return Response(gpt_response, status=http_status)
        
        return Response({"message": "Invalid input."}, status=status.HTTP_400_BAD_REQUEST)
    

class CreateAIRecipesView(generics.ListCreateAPIView):
    queryset = models.AIRecipes.objects.all()
    serializer_class = serializers.AIRecipeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user_id = request.user.id
        queryset = self.queryset.filter(created_by=user_id).order_by('-created_at')
        if not queryset.exists():
            USER_LOGGER.info(f"User {request.user.username} tried to list AI generated recipes, but hasn't created any.")
            SYSTEM_LOGGER.warning(f"User {self.request.user.id} tried to access his AI created recipes, but has none")
            return Response({"message": "This user has not created any AI generated recipes"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset, many=True)
        USER_LOGGER.info(f"User {request.user.username} listed their AI generated recipes.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        data = request.data
        recipe = self.queryset.create(
            created_by = request.user,
            message = data['message'],
            image_url = data['image_url']    
        )
        serializer = self.serializer_class(recipe)
        USER_LOGGER.info(f"User {request.user.username} created a new AI generated recipe with id: {recipe.id}.")
        SYSTEM_LOGGER.info(f"User {self.request.user.id} created an AI recipe")
        return Response(serializer.data, status=status.HTTP_201_CREATED)  
