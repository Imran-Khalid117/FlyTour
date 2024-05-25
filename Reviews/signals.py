from django.dispatch import receiver
from django.db.models import Avg
from django.db.models.signals import post_save
from .models import ReviewModel
from Places.models import PlaceModel


@receiver(post_save, sender=ReviewModel)
def post_save_book(sender, instance, created, **kwargs):
    # Calculate the average rating of a place.
    _place = instance.place_id
    average_rating = ReviewModel.objects.filter(place_id=_place).aggregate(average=Avg('rating'))['average']

    # Update the place's average rating
    _place = PlaceModel.objects.get(pk=_place.id)
    _place.rating = average_rating
    _place.save()
