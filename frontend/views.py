from django.shortcuts import render, get_object_or_404
from comptes.models import CompteComptable
from django.contrib.auth.decorators import login_required
from . import forms


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

    return render(request, "frontend/compte_form.html", {"numero": numero})

@login_required
def update_compte(request, compte_id):
    compte = get_object_or_404(CompteComptable, id=compte_id)
    if request.method == "GET":
        compte_form = forms.CompteForm(instance=compte)
        return render(request, 'frontend/update_compte.html',
                      context={'compte': compte, 'compte_form': compte_form})

    if request.method == "POST":
        compte_form = forms.CompteForm(request.POST,
                                       request.FILES, instance=compte)
        if compte_form.is_valid():
            new_compte = compte_form.save(commit=False)
            new_compte.user = request.user
            new_compte.save()
            #return redirect('update_compte')



