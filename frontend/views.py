from django.shortcuts import render, redirect, get_object_or_404
# from comptes.models import CompteComptable

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . import forms
from api.models import CompteComptable
from api.models import EcritureJournal
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json

# import requests
# from PIL import Image
# from rest_framework import viewsets
# from .models import CompteComptable

# =============== Accueil =========================

def accueil(request):
    return render(request, 'frontend/accueil.html')

# ============== Journaux ==============================

def journal_achats(request):
    return render(request,'frontend/journal_achats.html')


def journal_ventes(request):
    return render(request,'frontend/journal_ventes.html')


def journal_od(request):
    return render(request,'frontend/journal_od.html')


def journal_banque(request):
    return render(request,'frontend/journal_banque.html')


def journal_caisse(request):
    return render(request,'frontend/journal_caisse.html')


def journal_cpte_cheques_postaux(request):
    return render(request,'frontend/journal_cpte_cheques_postaux.html')


def journal_effets_a_payer(request):
    return render(request,'frontend/journal_effets_a_payer.html')


def journal_effets_a_recevoir(request):
    return render(request,'frontend/journal_effets_a_recevoir.html')


def journal_report_nouveau(request):
    return render(request,'frontend/journal_report_nouveau.html')


def journal_cloture(request):
    return render(request,'frontend/journal_cloture.html')


def journal_expert_od(request):
    return render(request,'frontend/journal_expert_od.html')


def journal_reouverture(request):
    return render(request,'frontend/journal_reouverture.html')

def journal_type(request):
    return render(request,'frontend/journal_type.html')


# ========================== Comptes ===========================================

def liste_compte(request):
    return render(request, 'frontend/pgc.html')


@login_required
def create_compte(request):
    compte_form = forms.CompteForm()
    if request.method == 'POST':
        compte_form = forms.CompteForm(request.POST)
        if compte_form.is_valid():
            compte_form.save()
        # handle the POST request here
        context = {
            'compte_form': compte_form
        }
    return render(request, 'frontend/post_create_compte.html', {'compte_form': compte_form})


def ajout_modif_compte(request):
    numero = request.GET.get("id")  # ici "id" représente en réalité le numéro comptable
    compte = None
    print('numero:', numero)

    if numero:
        compte = get_object_or_404(CompteComptable, numero=numero)
        print('compte:', compte)

    return render(request, "frontend/compte_form.html", {"compte": compte})


def get_pk_from_numero(request):
    numero = request.GET.get('numero')
    try:
        obj = CompteComptable.objects.get(numero=numero)
        return JsonResponse({'pk': obj.pk})
    except CompteComptable.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)


@csrf_exempt  # Si tu n'utilises pas {% csrf_token %}, sinon retire ça
def valider_journal_achats(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lignes = data.get('lignes', [])

            for ligne in lignes:
                date, compte, nom, libelle, quantite, pu_ht, taux, debit, credit, journal = ligne

                # Exemple d'enregistrement (à adapter à ton modèle)
                EcritureJournal.objects.create(
                    date=date if date else None,
                    compte=compte,
                    nom=nom,
                    libelle=libelle,
                    PU=pu_ht,
                    quantite=quantite or 0,
                    taux=taux or 0,
                    debit=debit or 0,
                    credit=credit or 0,
                    journal=journal
                )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
"""
# @login_required
def update_compte(request, compte_id=None):
    print('compte_id:', compte_id)
    instance_compte = CompteComptable.objects.get(pk=compte_id) if compte_id is not None else None
    if request.method == "GET":
        compte_form = forms.CompteForm(instance=instance_compte)
        context = {'compte_form:': compte_form}
        return render(request, 'frontend/post_update_compte.html', context=context)

    if request.method == "POST":
        compte_form = forms.CompteForm(request.POST, request.FILES, instance=instance_compte)
        if compte_form.is_valid():
            compte_form.save()
            return redirect('accueil')
"""


def compte_num_list(request):
    compte = None
    comptes = CompteComptable.objects.none()
    form_search = forms.CompteSearchForm(request.GET or None)
    form_edit = None

    if form_search.is_valid():
        numero = form_search.cleaned_data.get('numero')
        comptes = CompteComptable.objects.filter(numero=numero)
        if comptes.exists():
            compte = comptes.first()
            form_edit = forms.CompteEditForm(request.POST or None, instance=compte)
            if request.method == "POST" and form_edit.is_valid():
                form_edit.save()
                return redirect('compte_num_list')  # pour revenir proprement

    return render(request, 'frontend/data_list.html', {
        'form_search': form_search,
        'form_edit': form_edit,
        'comptes': comptes,
    })





"""
def update_compte(request):
    compte_form = forms.CompteForm()
    if request.method == "POST":
        # compte_form = forms.CompteForm(request.POST, request.FILES, instance=instance_compte)
        compte_form = forms.CompteSearchForm(request.POST)
        if compte_form.is_valid():
            compte_form.save()
    context = {'compte_form': compte_form}
    return render(request, 'frontend/post_update_compte.html', context=context)
"""



