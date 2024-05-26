from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FavouritesModel
from .serializer import FavouritesSerializer


# Create your views here.
class FavouritesView(viewsets.ModelViewSet):
    """
        This is a Category view class inherited from viewsets.ModelViewSet.

        Methods:
            list: Provides a read-only endpoint to list all instances of the model.
            This corresponds to the HTTP GET method on the collection endpoint.
            To list all objects: `GET /favourites/`

        create: Provides a write endpoint to create a new instance of the model.
                This corresponds to the HTTP POST method on the collection endpoint.
                To create a new object: `POST /favourites/`

        retrieve: Provides a read-only endpoint to retrieve a specific instance of the model.
                This corresponds to the HTTP GET method on the detail endpoint.
                To retrieve a single object by its primary key: `GET /favourites/{pk}/`

        update: Provides an endpoint to update a specific instance of the model (full update).
                This corresponds to the HTTP PUT method on the detail endpoint.
                To update an existing object completely: `PUT /favourites/{pk}/`

        partial_update: Provides an endpoint to partially update a specific instance of the model.
                        This corresponds to the HTTP PATCH method on the detail endpoint.
                        To update an existing object partially: `PATCH /favourites/{pk}/`

        destroy: Provides an endpoint to delete a specific instance of the model.
                This corresponds to the HTTP DELETE method on the detail endpoint.
                To delete an existing object: `DELETE /favourites/{pk}/`

        """
    queryset = FavouritesModel.objects.all()
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated]
