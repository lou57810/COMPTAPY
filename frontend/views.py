from datetime import datetime
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from api.models import Entreprise
from authentication.forms import SignupForm, UserCreateForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib import messages
import csv
from django.contrib.auth.decorators import login_required
from authentication.permissions import role_required

from django.http import JsonResponse
# from django import forms

from api import forms
from api.models import CompteComptable
from api.models import EcritureJournal
from api.views import get_compte_by_numero

from django.views.decorators.csrf import csrf_exempt
import json

import io
import zipfile
from django.utils.text import slugify
from api.utils import get_accessible_entreprises, create_user_and_entreprise

from django.shortcuts import render, redirect
from utils.session_utils import get_entreprise_active


User = get_user_model()


@login_required
@role_required(["OWNER", "GERANT"])
def afficher_modifier_dossier(request, entreprise_id):
    # 'owner=request.user' : empêche un utilisateur connecté d’accéder à une autre entreprise juste en modifiant l’URL
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    print('entreprise:', entreprise)
    if not entreprise:
        return redirect("setup")

    if request.method == "POST":
        form = forms.EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect("afficher-statuts", entreprise_id=entreprise.id)  # refresh
    else:
        form = forms.EntrepriseForm(instance=entreprise)

    return render(request, "frontend/afficher_statuts.html", {"form": form, "entreprise": entreprise})

# =============== Accueil =========================

def start_app(request):
    return render(request, "frontend/start_app.html")


def accueil(request):
    if User.objects.filter(role="OWNER").exists():
        messages.error(request, "Un propriétaire (OWNER) est déjà enregistré.")
    # Vérifier si l’utilisateur a une « entreprise active » sélectionnée

    entreprise_active = None
    if request.user.is_authenticated:
        entreprise_active = getattr(request.user, "entreprise", None)

    # Choix du template parent
    if not request.user.is_authenticated:
        base_template = "base0.html"
    elif not entreprise_active:
        base_template = "base0.html"
    else:
        base_template = "base.html"
    return render(request, 'frontend/accueil.html', {
        "base_template": base_template,
        "entreprise": entreprise_active,
    })


def accueil_dossier_compta(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    # On sauvegarde l'entreprise active dans la session
    request.session["entreprise_active_id"] = entreprise.id
    print('entreprise:', entreprise.nom)
    # if User.objects.filter(role="GERANT").exists():
    return render(request, "frontend/accueil_dossier_comptable.html", {"entreprise": entreprise, "entreprise.nom": entreprise.nom})

@login_required
def liste_entreprises(request):
    print('user:', request.user.role)
    entreprises = get_accessible_entreprises(request.user)
    return render(request, "frontend/liste_entreprises.html", {"entreprises": entreprises})

"""
@login_required
def ajouter_entreprise(request):
    role = request.GET.get("role")  # "GERANT" ou "EXPERT_COMPTABLE"
    print('get role:', role)
    # Permet au user connecté d’ajouter une entreprise
    if request.method == "POST":
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            entreprise = form.save(commit=False)
            entreprise.owner = request.user  # ou .created_by selon ton modèle
            entreprise.save()
            return redirect("liste-entreprises")
    else:
        form = EntrepriseForm()

    return render(request, "frontend/ajouter_entreprise.html", {"form": form})
"""

def setup(request):
    role = request.GET.get("role")  # "GERANT" ou "EXPERT_COMPTABLE"
    # print('get role:', role)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user, entreprise = create_user_and_entreprise(

                email=data["email"],
                password=data["password1"],
                role=data["role"],
                nom=data.get("nom"),
                siret=data.get("siret"),
                ape=data.get("ape"),
                adresse=data.get("adresse"),
                date_creation=data.get("date_creation"),
                # owner=request.user if request.user.is_authenticated else None,
            )
            return redirect("accueil")
    else:
        form = SignupForm()

    return render(request, "frontend/setup.html", {"form": form})


@login_required
def supprimer_entreprise(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    # Vérifier que l’utilisateur a le droit (ex : est OWNER de cette entreprise)
    if request.user.role == "OWNER" and entreprise.owner == request.user:
        entreprise.delete()
        # Message de succès (optionnel)
        messages.success(request, "Entreprise supprimée.")
    else:
        # Message d’erreur ou access interdit
        messages.error(request, "Vous n’êtes pas autorisé.")
        pass
    return redirect("list-entreprises")


def saisie_journal(request):
    entreprise = get_entreprise_active(request)

    if not entreprise:
        messages.warning(request, "Veuillez d'abord sélectionner une entreprise.")
        return redirect("liste-entreprises")
    type_journal = request.GET.get('type', '')  # Par défaut : journal achats
    context = {
        'type_journal': type_journal, "entreprise": entreprise
    }
    return render(request, 'frontend/journal_accueil.html', context)

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
            messages.success(request, 'Le compte a été créé avec succès !')
            return render(request, 'frontend/create_compte.html', {'compte_form': compte_form})
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

    comptes = list(CompteComptable.objects.values_list('numero', flat=True))
    if numero:
        compte = get_object_or_404(CompteComptable, numero=numero)
        nom = compte.nom
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


# frontend/views.py
@login_required
def valider_journal(request, type_journal):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    entreprise_id = request.GET.get("entreprise_id")
    entreprise = get_object_or_404(Entreprise, id=entreprise_id, owner=request.user)

    try:
        payload = json.loads(request.body)
        lignes = payload.get("lignes", [])
    except json.JSONDecodeError:
        return JsonResponse({"error": "Format JSON invalide"}, status=400)

    saved = []
    for ligne in lignes:
        if not ligne.get("date"):
            continue

        ecriture = EcritureJournal.objects.create(
            entreprise=entreprise,  # 👈 Nouveau champ à ajouter au modèle
            date=datetime.strptime(ligne["date"], "%d/%m/%Y").date(),
            # compte_id=get_compte_from_numero(ligne["numero"]),  # à adapter selon ta logique
            compte_id=get_compte_by_numero(ligne["numero"]),  # à adapter selon ta logique
            nom=ligne["nom"],
            numero_piece=ligne["numero_piece"],
            libelle=ligne["libelle"],
            debit=ligne["debit"],
            credit=ligne["credit"],
            journal=type_journal,
        )
        saved.append(ecriture.id)

    return JsonResponse({"success": True, "saved_ids": saved})


"""
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

                # print("👉 Ligne reçue :", ligne)
                # print("📅 Date extraite :", date)

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
                # print('Ecritures enregistrées:', ecriture)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print("❌ ERREUR:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
"""

def ecritures_par_compte(numero):
    ecritures = EcritureJournal.objects.filter(compte=numero).values(
        'date', 'numero_piece', 'libelle', 'debit', 'credit'
    )
    return JsonResponse(list(ecritures), safe=False)


def afficher_statut_entreprise(request):
    print('affichage_statuts')
    return render(request, 'frontend/afficher_statuts.html')


@login_required
@role_required(["GERANT", "COMPTABLE", "EXPERT_COMPTABLE"])
def export_fec(request):
    # Si GLOBAL_COMPTABLE → toutes les entreprises
    if request.user.role == "EXPERT_COMPTABLE":
        entreprises = Entreprise.objects.all()
        is_multi = True
    else:
        entreprises = [request.user.entreprise]
        is_multi = False

    if is_multi:
        # Création d'un fichier ZIP en mémoire
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for entreprise in entreprises:
                csv_buffer = io.StringIO()
                writer = csv.writer(csv_buffer, delimiter='|')
                _write_fec_header(writer)

                ecritures = EcritureJournal.objects.filter(compte__entreprise=entreprise)
                for e in ecritures:
                    _write_fec_row(writer, e)

                # Ajouter le CSV de cette entreprise dans le ZIP
                zip_file.writestr(f"FEC_{slugify(entreprise.nom)}.csv", csv_buffer.getvalue())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=FEC_all.zip'
        return response

    else:
        # Cas simple → une seule entreprise → CSV direct
        entreprise = entreprises[0]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=FEC_{slugify(entreprise.nom)}.csv'

        writer = csv.writer(response, delimiter='|')
        _write_fec_header(writer)

        ecritures = EcritureJournal.objects.filter(compte__entreprise=entreprise)
        for e in ecritures:
            _write_fec_row(writer, e)

        return response


def _write_fec_header(writer):
    """Écrit les en-têtes du FEC (factorisé pour CSV unique et ZIP)."""
    writer.writerow([
        "JournalCode", "JournalLib", "EcritureNum", "EcritureDate",
        "CompteNum", "CompteLib", "CompAuxNum", "CompAuxLib",
        "PieceRef", "PieceDate", "EcritureLib",
        "Debit", "Credit", "EcritureLet", "DateLet",
        "ValidDate", "Montantdevise", "Idevise"
    ])


def _write_fec_row(writer, e):
    """Écrit une ligne FEC pour une écriture donnée."""
    writer.writerow([
        e.journal.code,
        e.journal.libelle,
        e.id,
        e.date.strftime("%Y%m%d"),
        e.compte.numero,
        e.compte.libelle,
        "",  # CompAuxNum
        "",
        e.piece_ref or "",
        e.piece_date.strftime("%Y%m%d") if e.piece_date else "",
        e.libelle,
        e.debit or "0.00",
        e.credit or "0.00",
        "",
        "",
        e.date.strftime("%Y%m%d"),
        "",
        ""
    ])


@login_required
@role_required(["EXPERT_COMPTABLE", "GERANT", "DRH"])
def manage_users(request):
    entreprise = request.user.entreprise
    utilisateurs = User.objects.filter(entreprise=entreprise)

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.entreprise = entreprise
            user.save()
            return redirect("manage-users")
    else:
        form = UserCreateForm()

    return render(request, "frontend/manage_users.html", {
        "entreprise": entreprise,
        "utilisateurs": utilisateurs,
        "form": form
    })

