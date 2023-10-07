from rest_framework import generics, status
from recipes import serializers
from rest_framework.permissions import IsAuthenticated
from recipes import models
from rest_framework.response import Response
from datetime import datetime, timedelta



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
