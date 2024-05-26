from rest_framework import serializers
from .models import FavouritesModel


class FavouritesSerializer(serializers.ModelSerializer):
    """
       Fields to show and save:
           'id', 'user_id', 'place_id'
       """
    class Meta:
        model = FavouritesModel
        fields = ["id", "user_id", "place_id"]
