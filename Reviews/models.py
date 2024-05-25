from django.db import models
from AppUser.models import ApplicationUser
from Places.models import PlaceModel


# Create your models here.

class ReviewModel(models.Model):
    user_id = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE, related_name="user_reviews")
    place_id = models.ForeignKey(PlaceModel, on_delete=models.CASCADE, related_name="place_review")
    rating = models.IntegerField(blank=False, null=False)
    comments = models.CharField(max_length=250, blank=False, null=False)

    class Meta:
        db_table = "db_review"
