from django.dispatch import receiver
from django.db.models import Avg
from django.db.models.signals import post_save
from .models import ReviewModel
from Places.models import PlaceModel


@receiver(post_save, sender=ReviewModel)
def post_save_book(sender, instance, created, **kwargs):
    """
    This is a post save signal function, that will be called when we create or update the review record.
    We are updating the rating field of Place model with average of rating field in Review model.
    We are updating the rating field of Place model with respect to specific place_id.

    Params:
        sender: Object - (ReviewModel) - The sender parameter is used to specify the model or class that
                                            sends the signal.
        instance: Object - (ReviewModel) - This parameter is passed to the signal handler function and allows you to
                                            access and manipulate the specific model instance that triggered the signal.
        created: is a boolean flag that indicates whether a new instance was created or an existing
                instance was updated.
        **kwargs: key word arguments passed to this function.
    """
    # Getting the place object from instance.
    _place = instance.place_id
    # Calculate the average rating of a place.
    average_rating = ReviewModel.objects.filter(place_id=_place).aggregate(average=Avg('rating'))['average']

    # Update the place's average rating
    _place = PlaceModel.objects.get(pk=_place.id)
    _place.rating = average_rating
    _place.save()
