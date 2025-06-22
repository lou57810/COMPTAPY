from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets

from .models import CompteComptable
from .serializers import CompteComptableSerializer


"""
class CompteComptableListView(generics.ListAPIView):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer


class CompteComptableViewSet(viewsets.ModelViewSet):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer
"""
