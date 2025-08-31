from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from api import forms
from api.models import CompteComptable
from api.models import EcritureJournal

from django.views.decorators.csrf import csrf_exempt
import json


# =============== Accueil =========================

def accueil(request):
    return render(request, 'frontend/accueil.html')


# ============== Journaux ==============================
"""
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
"""


# def journal_type(request):
def saisie_journal(request):
    type_journal = request.GET.get('type', '')  # Par défaut : journal achats
    context = {
        'type_journal': type_journal,
    }
    return render(request, 'frontend/journal_type.html', context)


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
    return render(request, 'frontend/create_compte.html', {'compte_form': compte_form})


def display_compte(request):
    # compte = None
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
                return redirect('display_compte')  # pour revenir proprement

    return render(request, 'frontend/display_compte.html', {
        'form_search': form_search,
        'form_edit': form_edit,
        'comptes': comptes,
    })


def afficher_compte(request):
    numero = []
    nom = []
    lignes = []
    numero = request.GET.get('numero')
    # print(f"DEBUG numero reçu: '{numero}'")

    comptes = list(CompteComptable.objects.values_list('numero', flat=True))
    # print(f"DEBUG comptes existants: {comptes}")
    if numero:
        # print(f"DEBUG numero reçu2: '{numero}'")
        # print("GET.numero =", repr(numero))
        # print("Comptes existants2:", list(CompteComptable.objects.values_list("numero", flat=True)[:5]))
        compte = get_object_or_404(CompteComptable, numero=numero)
        nom = compte.nom
        # print('compte:', nom)
        lignes = EcritureJournal.objects.filter(compte__numero=numero).order_by('date')
    else:
        nom, lignes = "", []

    return render(request, 'frontend/afficher_compte.html', {'lignes': lignes, 'numero': numero, 'nom': nom})


def update_compte(request):
    compte = None
    comptes = CompteComptable.objects.none()
    form_search = forms.CompteSearchForm(request.GET or None)
    form_edit = None

    if form_search.is_valid():
        numero = form_search.cleaned_data.get('numero')
        comptes = CompteComptable.objects.filter(numero=numero)
        if comptes.exists():
            compte = comptes.first()
            form_edit = forms.UpdateCompteForm(request.POST, request.FILES, instance=compte)
            if request.method == "POST" and form_edit.is_valid():
                form_edit.save()
                return redirect('update_compte')  # pour revenir proprement

    return render(request, 'frontend/update_compte.html', {
        'form_search': form_search,
        'form_edit': form_edit,
        'comptes': comptes,
    })


def get_pk_from_numero(request):
    numero = request.GET.get('numero')
    try:
        obj = CompteComptable.objects.get(numero=numero)
        return JsonResponse({'pk': obj.pk})
    except CompteComptable.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)


@csrf_exempt  # Si tu n'utilises pas {% csrf_token %}, sinon retire ça
def valider_journal(request, type_journal):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lignes = data.get('lignes', [])

            for ligne in lignes:
                # On récupère chaque champ par clé
                date_str = ligne.get('date')
                if date_str:
                    date = datetime.strptime(date_str, "%d/%m/%Y").date()  # ou %Y-%m-%d selon format reçu
                numero = ligne.get('numero')
                nom = ligne.get('nom')
                numero_piece = ligne.get('numero_piece')
                libelle = ligne.get('libelle')
                debit = ligne.get('debit', 0)
                credit = ligne.get('credit', 0)

                print("👉 Ligne reçue :", ligne)
                print("📅 Date extraite :", date)

                # ✅ On récupère l’instance du compte correspondant
                compte = CompteComptable.objects.filter(numero=numero).first()

                if not compte:
                    # Tu peux aussi lever une exception ou juste passer
                    print(f"⚠️ Compte non trouvé pour numéro {numero}")
                    continue

                # ✅ Enregistrement correct
                ecriture = EcritureJournal.objects.create(
                    date=date,
                    compte=compte,  # ici une vraie instance
                    nom=nom,
                    numero_piece=numero_piece,
                    libelle=libelle,
                    debit=debit,
                    credit=credit,
                    journal=type_journal  # Achats, Ventes, OD ...
                )
                print('Ecritures enregistrées:', ecriture)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("❌ ERREUR:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)


def ecritures_par_compte(numero):
    ecritures = EcritureJournal.objects.filter(compte=numero).values(
        'date', 'numero_piece', 'libelle', 'debit', 'credit'
    )
    return JsonResponse(list(ecritures), safe=False)





"""
# @login_required
def update_data_compte(request, compte_id=None):
    print('compte_id:', compte_id)
    instance_compte = CompteComptable.objects.get(pk=compte_id) if compte_id is not None else None
    if request.method == "GET":
        compte_form = forms.CompteForm(instance=instance_compte)
        context = {'compte_form:': compte_form}
        return render(request, 'frontend/update_compte.html', context=context)

    if request.method == "POST":
        compte_form = forms.CompteForm(request.POST, request.FILES, instance=instance_compte)
        if compte_form.is_valid():
            compte_form.save()
            return redirect('accueil')

def ajout_modif_compte(request):
    numero = request.GET.get("id")  # ici "id" représente en réalité le numéro comptable
    compte = None
    print('numero:', numero)

    if numero:
        compte = get_object_or_404(CompteComptable, numero=numero)
        print('compte:', compte)

    return render(request, "frontend/compte_form.html", {"compte": compte})
"""
