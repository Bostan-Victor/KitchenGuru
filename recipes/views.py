from rest_framework import generics, status
from recipes import serializers, models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CreateRecipeView(generics.CreateAPIView):
    serializer_class = serializers.CreateRecipeSerializer
    permission_classes = [IsAuthenticated]

    
class CreateReviewView(generics.CreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.RecipeReviewSerializer
    permission_classes = [IsAuthenticated]
        
    def create(self, request):
        data = request.data
        user = request.user
        recipe = models.Recipes.objects.get(title=data["title"])
        review = models.Review.objects.create(recipes=recipe, user=user, rating=data["rating"], text=data["text"])
        serializer = serializers.RecipeReviewSerializer(review, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
