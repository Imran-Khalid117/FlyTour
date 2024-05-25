from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import PlaceModel
from .serializer import PlaceSerializer


# Create your views here.

class PlacesView(viewsets.ModelViewSet):
    queryset = PlaceModel.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]
