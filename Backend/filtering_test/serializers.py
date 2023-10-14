from rest_framework import serializers


class FilteringSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    comment_count = serializers.IntegerField()
    rating = serializers.FloatField()
    # ingredients = serializers.CharField(max_length=1024)
    # instructions = serializers.CharField(max_length=2048)
    category = serializers.CharField(max_length=255)
    favorites_count = serializers.IntegerField()
    duration_time = serializers.IntegerField()




