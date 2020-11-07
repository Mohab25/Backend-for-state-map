from django.shortcuts import render
from .serializers import RoadsSerializer 
from rest_framework import generics 
from .models import roads

class RoadListView(generics.ListCreateAPIView):
    queryset = roads.objects.all()
    serializer_class= RoadsSerializer
    name = 'road-list'

class RoadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset= roads.objects.all()
    serializer_class = RoadsSerializer
    name = 'road-detail'

