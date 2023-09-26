from rest_framework import generics, status
from filtering_test import serializers, models
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class FilteringView(generics.ListAPIView):    
    def list(self, request):
        queryset = models.TestRecipes.objects.all()

        data = request.data
        sort_by = data.get('sort_by')
        category = data.get('category')
        duration_min = data.get('duration_min')
        duration_max = data.get('duration_max')

        if sort_by:
            queryset = queryset.order_by(sort_by)
        
        if category:
            queryset = queryset.filter(category__in=category)

        if duration_min:
            queryset = queryset.filter(duration_time__gte=duration_min)

        if duration_max:
            queryset = queryset.filter(duration_time__lte=duration_max)


        serializer = serializers.FilteringSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
