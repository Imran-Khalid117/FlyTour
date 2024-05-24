from rest_framework import serializers
from .models import FavouritesModel


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouritesModel
        fields = ["id", "user_id", "place_id"]
