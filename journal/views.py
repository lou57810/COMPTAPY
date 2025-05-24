from django.shortcuts import render
import requests


from rest_framework import viewsets
from .models import Compte, EcritureJournal
from .serializers import CompteSerializer, EcritureJournalSerializer


def journal(request):
    return render(request,'journal/journal.html')


class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer


class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer

class EcritureJournalViewSet(viewsets.ModelViewSet):
    queryset = EcritureJournal.objects.all()
    serializer_class = EcritureJournalSerializer


