from rest_framework import serializers
from .models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    """
    Fields to show and save:
        'id', 'category_name'
    """
    class Meta:
        model = CategoryModel
        fields = ['id', 'category_name']
