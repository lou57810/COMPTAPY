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

def accueil(request):
    return render(request, 'frontend/accueil.html')


@require_http_methods(["GET", "POST"])
def setup(request):
    # si entreprise existe déjà, on bloque l’accès
    if Entreprise.objects.exists() or User.objects.filter(is_owner=True).exists():
        return redirect("accueil")  # ou tableau de bord

    if request.method == "POST":
        # récupérer champs entreprise
        nom = (request.POST.get("nom") or "").strip()
        siret = (request.POST.get("siret") or "").strip()
        ape = (request.POST.get("ape") or "").strip()
        adresse = (request.POST.get("adresse") or "").strip()
        date_creation = request.POST.get("date_creation") or now().date()

        email = (request.POST.get("email") or "").strip().lower()
        password = request.POST.get("password") or ""

        if not email or not password or not nom or not siret:
            # à toi d’améliorer les messages d’erreur/formulaire
            return render(request, "frontend/setup.html", {
                "error": "Champs requis manquants (email, mot de passe, nom, siret)."
            })
        try:
            with transaction.atomic():
                # 1) créer l’admin avec tous les droits
                user = User.objects.create_superuser(email=email, password=password)
                user.is_owner = True
                user.role = "OWNER"
                user.save(update_fields=["is_owner", "role"])
                """
                # 2) Créer l'utilisateur
                user = User.objects.create(
                    email=email,
                    password=make_password(password),
                    is_superuser=True,
                    is_staff=True,
                    is_owner=True,
                    role="OWNER",  # si tu as un champ role sur ton modèle User
                )
                """
                # 2) créer l’entreprise en liant owner
                entreprise = Entreprise.objects.create(
                    nom=nom,
                    siret=siret,
                    ape=ape,
                    adresse=adresse,
                    date_creation=date_creation,
                    owner=user,
                )
                # 3) Lier l'entreprise à l'utilisateur
                user.entreprise = entreprise
                user.save(update_fields=["entreprise"])

        except Exception as e:
            return render(request, "frontend/setup.html", {
                "error": f"Erreur lors de la création: {str(e)}"
            })

        return redirect("login")
    return render(request, "frontend/setup.html")


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
@role_required(["OWNER", "COMPTABLE"])
def export_fec(request):
    entreprise = request.user.entreprise
    ecritures = EcritureJournal.objects.filter(compte__entreprise=entreprise)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=FEC_{entreprise.nom}.csv'

    writer = csv.writer(response, delimiter='|')  # séparateur imposé = pipe
    writer.writerow([
        "JournalCode", "JournalLib", "EcritureNum", "EcritureDate",
        "CompteNum", "CompteLib", "CompAuxNum", "CompAuxLib",
        "PieceRef", "PieceDate", "EcritureLib",
        "Debit", "Credit", "EcritureLet", "DateLet",
        "ValidDate", "Montantdevise", "Idevise"
    ])

    for e in ecritures:
        writer.writerow([
            e.journal.code,
            e.journal.libelle,
            e.id,
            e.date.strftime("%Y%m%d"),
            e.compte.numero,
            e.compte.libelle,
            "",  # CompAuxNum à compléter si tu gères clients/fournisseurs
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

    return response


@login_required
@role_required(["OWNER", "DRH"])
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
        "utilisateurs": utilisateurs,
        "form": form
    })

