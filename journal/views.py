from django.shortcuts import render
import requests


from rest_framework import viewsets
from .models import Compte, EcritureJournal
from .serializers import CompteSerializer, EcritureJournalSerializer


def journal_achats(request):
    return render(request,'journal/journal_achats.html')


def journal_ventes(request):
    return render(request,'journal/journal_ventes.html')


def journal_od(request):
    return render(request,'journal/journal_od.html')


def journal_banque(request):
    return render(request,'journal/journal_banque.html')


def journal_caisse(request):
    return render(request,'journal/journal_caisse.html')


def journal_cpte_cheques_postaux(request):
    return render(request,'journal/journal_cpte_cheques_postaux.html')


def journal_effets_a_payer(request):
    return render(request,'journal/journal_effets_a_payer.html')


def journal_effets_a_recevoir(request):
    return render(request,'journal/journal_effets_a_recevoir.html')


def journal_report_nouveau(request):
    return render(request,'journal/journal_report_nouveau.html')


def journal_cloture(request):
    return render(request,'journal/journal_cloture.html')


def journal_expert_od(request):
    return render(request,'journal/journal_expert_od.html')


def journal_reouverture(request):
    return render(request,'journal/journal_reouverture.html')

def journal_type(request):
    return render(request,'journal/journal_type.html')


class CompteViewSet(viewsets.ModelViewSet):
    queryset = Compte.objects.all()
    serializer_class = CompteSerializer


class EcritureJournalViewSet(viewsets.ModelViewSet):
    queryset = EcritureJournal.objects.all()
    serializer_class = EcritureJournalSerializer


