from rest_framework import serializers
from .models import ReviewModel


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewModel
        fields = ["id", "user_id", "place_id", "rating", "comments"]
