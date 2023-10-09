from rest_framework import generics, status
from recipes import serializers
from rest_framework.permissions import IsAuthenticated
from recipes import models
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Max, F
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend






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
    queryset = models.Recipes.objects.all().prefetch_related('images')
    serializer_class = serializers.GetRecipesSerializer


class GetIngredients(generics.ListAPIView):
    queryset = models.Ingredients.objects.all()
    serializer_class = serializers.GetIngredientsSerializer
    permission_classes = [IsAuthenticated]


class FilteringView(generics.ListAPIView):
    serializer_class = serializers.GetRecipesSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['duration', 'id']
    ordering = ['duration']
    # ordering_fields = ['comment_count', 'rating', 'favorites_count']
    # ordering = ['rating']

    def list(self, request):
        queryset = models.Recipes.objects.all()
        db_max_duration = models.Recipes.objects.aggregate(db_max_duration=Max('duration'))['db_max_duration']

        # sort_by = self.request.query_params.get('sort_by')
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
            categories_list = categories.split(',')
            queryset = queryset.filter(category__in=categories_list)
        
        # order_by_field = sort_by
        # order_by_field = sort_by if sort_by in self.ordering_fields else self.ordering[0]
        # queryset = queryset.order_by(order_by_field)

        if not queryset.exists():
            return Response({"message": "There are no recipes that match these filters"}, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchRecipesView(generics.ListAPIView):
    serializer_class = serializers.GetRecipesSerializer
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
                'match_count': len(matching_ingredients)
                })
        if matched_recipes:
            sorted_recipes = sorted(matched_recipes, key=lambda x: x['match_count'], reverse=True)
            sorted_recipes = [entry['recipe'] for entry in sorted_recipes]
        else:
            return Response({"message": "No recipes have the ingredients provided"}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(sorted_recipes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class FilterRecipesView(generics.ListAPIView):
    queryset = models.Recipes.objects.all()
    serializer = serializers.GetRecipesSerializer