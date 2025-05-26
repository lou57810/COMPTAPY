from django.shortcuts import render
import requests


from rest_framework import viewsets
from .models import Compte, EcritureJournal
from .serializers import CompteSerializer, EcritureJournalSerializer


def journal_type(request):
    return render(request,'journal/journal_type.html')


def journal_ventes(request):
    return render(request,'journal/journal_ventes.html')


def journal_achats(request):
    return render(request,'journal/journal_achats.html')


def journal_od(request):
    return render(request,'journal/journal_od.html')


def journal_report_nouveau(request):
    return render(request,'journal/journal_report_nouveau.html')


class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer


class EcritureJournalViewSet(viewsets.ModelViewSet):
    queryset = EcritureJournal.objects.all()
    serializer_class = EcritureJournalSerializer


