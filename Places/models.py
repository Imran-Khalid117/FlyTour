from django.db import models
from Catagories.models import CategoryModel


# Create your models here.
class PlaceModel(models.Model):
    """
        This model class is inherited from models.Model class.

        This class is used to define the fields and name the database table for `Place`
        """
    place_name = models.CharField(max_length=100, blank=False)
    category_id = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name="place_category")
    address = models.CharField(max_length=100, blank=False)
    contact_number = models.CharField(max_length=20, blank=False)
    latitude = models.CharField(max_length=20, blank=False)
    longitude = models.CharField(max_length=20, blank=False)
    image_url = models.CharField(max_length=100, blank=True, null=True)
    rating = models.FloatField(default=0.0)

    class Meta:
        db_table = "db_place"
