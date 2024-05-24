from django.db import models
from AppUser.models import ApplicationUser
from Places.models import PlaceModel


# Create your models here.
class FavouritesModel(models.Model):
    user_id = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, related_name="user_favourites")
    place_id = models.ForeignKey(PlaceModel, on_delete=models.CASCADE, related_name="user_favourite_categories")

    class Meta:
        db_table = "db_favourites"
