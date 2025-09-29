from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import get_user_model
from api.models import Entreprise
from authentication.forms import UserCreateForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.http import HttpResponse
import csv
from django.db.utils import IntegrityError

from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from authentication.permissions import role_required
from authentication.models import User

from django.http import JsonResponse
from django import forms
# from django.forms import ModelForm
from api import forms
from api.models import CompteComptable
from api.models import EcritureJournal

from django.views.decorators.csrf import csrf_exempt
import json

import io
import zipfile
from django.utils.text import slugify
# from .utils import create_user_and_entreprise
from api.utils import get_accessible_entreprises, create_user_and_entreprise

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now
from django.contrib.auth import login



@login_required
# @role_required(["OWNER", "ADMIN"])
@role_required(["OWNER"])
def afficher_modifier_dossier(request):
    entreprise = get_object_or_404(Entreprise, owner=request.user)
    if not entreprise:
        return redirect("setup")

    if request.method == "POST":
        form = forms.EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect("afficher-statuts")  # refresh
    else:
        form = forms.EntrepriseForm(instance=entreprise)

    return render(request, "frontend/afficher_statuts.html", {"form": form})

# =============== Accueil =========================

def start_app(request):
    return render(request, "frontend/start_app.html")

def accueil(request):
    return render(request, 'frontend/accueil.html')

@login_required
def liste_entreprises(request):
    entreprises = get_accessible_entreprises(request.user)
    return render(request, "frontend/liste_entreprises.html", {"entreprises": entreprises})



# Double emploi: déjà défini dans api/utils
"""
def get_accessible_entreprises(user):
    if user.role == "EXPERT_COMPTABLE":
        return Entreprise.objects.all()  # accès global
    return Entreprise.objects.filter(pk=user.entreprise_id) if user.entreprise else Entreprise.objects.none()
"""







@require_http_methods(["GET", "POST"])
def setup(request):
    role = request.GET.get("role")  # "GERANT" ou "EXPERT_COMPTABLE"
    print('role:', role)

    if request.method == "POST":
        print("➡️ POST reçu avec role:", role)
        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""
        full_name = (request.POST.get("full_name") or "").strip()
        print("Email:", email, "Password:", "****", "Nom complet:", full_name)
        # Champs entreprise
        nom = (request.POST.get("nom") or "").strip()
        siret = (request.POST.get("siret") or "").strip()
        ape = (request.POST.get("ape") or "").strip()
        adresse = (request.POST.get("adresse") or "").strip()
        date_creation = request.POST.get("date_creation") or now().date()

        if not email or not password:
            print("❌ Email ou password manquant, role:", role)
            return render(request, "frontend/setup.html", {
                "error": "Email et mot de passe requis.",
                "role": role
            })

        try:
            print("Tentative création user + entreprise…")
            user, entreprise = create_user_and_entreprise(
                email=email,
                password=password,
                role=role,
                nom=nom,
                siret=siret,
                ape=ape,
                adresse=adresse,
                date_creation=date_creation,
            )
            print("✅ Utilisateur créé:", user, "Entreprise:", entreprise)
            user.full_name = full_name
            print('full_name', user.full_name)
            user.save(update_fields=["full_name"])

            # Auto-login après setup
            login(request, user)
            return redirect("accueil")

        except Exception as e:
            return render(request, "frontend/setup.html", {
                "error": f"Erreur lors de la création: {str(e)}",
                "role": role
            })

    return render(request, "frontend/setup.html", {"role": role})





"""
def setup(request, mode="mono"):

    # mode = "mono" -> création d'un gérant (OWNER) + son entreprise
    # mode = "multi" -> création d'un expert comptable (EXPERT_COMPTABLE) sans entreprise liée

    email = request.POST.get("email")
    password = request.POST.get("password")

    with transaction.atomic():
        if mode == "mono":
            # Créer l'entreprise
            entreprise = Entreprise.objects.create(
                nom=request.POST.get("nom_entreprise"),
                siret=request.POST.get("siren"),
                ape=request.POST.get("ape"),
                adresse=request.POST.get("adresse"),
                date_creation=request.POST.get("date_creation"),
                owner=request.POST.get("user"),
            )

            # Créer l'utilisateur OWNER lié à cette entreprise
            user = User.objects.create_user(
                email=email,
                password=password,
                role="OWNER",
                is_owner=True,
                entreprise=entreprise
            )

        elif mode == "multi":
            # Créer uniquement l'utilisateur expert-comptable
            # (il pourra ensuite créer/accéder à plusieurs entreprises)
            user = User.objects.create_user(
                email=email,
                password=password,
                role="EXPERT_COMPTABLE",
                is_owner=False,
                entreprise=None
            )

        else:
            raise ValueError("Mode non reconnu (mono|multi)")

    return user
"""

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

