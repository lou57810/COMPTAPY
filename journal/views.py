# from django.shortcuts import render

from rest_framework import viewsets
from .models import Compte, EcritureJournal
from .serializers import CompteSerializer, EcritureJournalSerializer

class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer


class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer

class EcritureJournalViewSet(viewsets.ModelViewSet):
    queryset = EcritureJournal.objects.all()
    serializer_class = EcritureJournalSerializer


