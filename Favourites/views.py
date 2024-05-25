from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FavouritesModel
from .serializer import FavouritesSerializer


# Create your views here.
class FavouritesView(viewsets.ModelViewSet):
    queryset = FavouritesModel.objects.all()
    serializer_class = FavouritesSerializer
    permission_classes = [IsAuthenticated]
