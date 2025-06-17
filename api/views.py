from django.shortcuts import render
from rest_framework import generics

from .models import CompteComptable
from .serializers import CompteComptableSerializer



class CompteComptableListView(generics.ListAPIView):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer

