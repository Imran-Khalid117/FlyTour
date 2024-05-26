from rest_framework import serializers
from .models import PlaceModel


class PlaceSerializer(serializers.ModelSerializer):
    """
       Fields to show and save:
           'id', 'place_name', 'category_id', 'address', 'contact_number', 'latitude', 'longitude', 'image_url',
           'rating' (Calculated Column)
    """
    class Meta:
        model = PlaceModel
        fields = ["id", "place_name", "category_id", "address", "contact_number", "latitude", "longitude",
                  "image_url", "rating"]
