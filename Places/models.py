from django.db import models
from Catagories.models import CategoryModel


# Create your models here.
class PlaceModel(models.Model):
    place_name = models.CharField(max_length=100, blank=False)
    category_id = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name="place_category")
    address = models.CharField(max_length=100, blank=False)
    contact_number = models.CharField(max_length=20, blank=False)
    latitude = models.IntegerField(max_length=15, blank=False)
    longitude = models.IntegerField(max_length=15, blank=False)
    image_url = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(max_length=4, blank=True, null=False)

    class Meta:
        db_table = "db_place"
