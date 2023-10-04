from rest_framework import generics, status
from filtering_test import serializers, models
from rest_framework.response import Response
from django.db.models import Max


class FilteringView(generics.ListAPIView):
    serializer_class = serializers.FilteringSerializer
    ordering_fields = ['comment_count', 'rating', 'favorites_count']
    ordering = ['rating']

    def list(self, request):
        queryset = models.TestRecipes.objects.all()
        db_max_duration = models.TestRecipes.objects.aggregate(db_max_duration=Max('duration_time'))['db_max_duration']

        sort_by = self.request.query_params.get('sort_by')
        categories = self.request.query_params.get('category')
        
        try:
            duration_min = int(self.request.query_params.get('duration_min', 0))
            duration_max = int(self.request.query_params.get('duration_max', db_max_duration))
        except ValueError:
            return Response({"message": "Duration should be a valid number."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not (0 <= duration_min <= duration_max <= db_max_duration):
            return Response({"message": "Invalid duration parameters."}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = queryset.filter(duration_time__gte=duration_min, duration_time__lte=duration_max)
        
        if categories:
            categories_list = categories.split(',')
            queryset = queryset.filter(category__in=categories_list)
        
        order_by_field = sort_by if sort_by in self.ordering_fields else self.ordering[0]
        queryset = queryset.order_by(order_by_field)

        if not queryset.exists():
            return Response({"message": "There are no recipes that match these filters"}, status=status.HTTP_404_NOT_FOUND)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
