from datetime import datetime
# import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from api.models import Entreprise, CompteComptable, EcritureJournal
from authentication.forms import SignupForm, UserCreateForm
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.hashers import make_password
# from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib import messages
import csv
from django.contrib.auth.decorators import login_required
from authentication.permissions import role_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

from django.http import JsonResponse

from api import forms
from api.forms import CompteForm


from api.views import get_compte_by_numero
# from django.views.decorators.csrf import csrf_exempt
import json

import io
import zipfile
from django.utils.text import slugify
from api.utils import create_user_and_entreprise, get_owner, get_entreprise_from_gerant


from utils.session_utils import get_entreprise_active


User = get_user_model()

"""
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
        # form = forms.FolderForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            # return redirect("afficher-statuts", entreprise_id=entreprise.id)  # refresh
            return redirect("afficher-statuts", entreprise_id=entreprise_id)  # refresh
    else:
        form = forms.EntrepriseForm(instance=entreprise)
        # form = forms.FolderForm(instance=entreprise)

    return render(request, "frontend/afficher_modifier_dossier.html", {"form": form, "entreprise": entreprise})
"""

# =============== Accueil =========================

def start_app(request):
    return render(request, "frontend/start_app.html")


def accueil(request):
    user = request.user

    # Si l'utilisateur n'est pas connecté, on le redirige vers la page de login
    if not user.is_authenticated:
        return redirect("login")

    # Si c’est un OWNER : il voit toutes les entreprises
    if getattr(user, "role", None) == "OWNER":
        entreprises = Entreprise.objects.all()
    # Si c’est un gérant : il ne voit que sa propre entreprise
    elif getattr(user, "role", None) == "GERANT":
        entreprises = Entreprise.objects.filter(gerant=user)
    else:
        entreprises = []

    entreprise_nom = entreprises.first().nom if entreprises else None

    context = {
        "entreprises": entreprises,
        "entreprise_nom": entreprise_nom,
        "is_owner": getattr(user, "role", None) == "OWNER",
        "gerant_id": request.user.id,
    }

    # return render(request, "frontend/accueil_manager.html", context)
    # return render(request, "frontend/accueil_gerant.html", context)
    return render(request, "frontend/accueil.html", context)


# def get_owner():
    # return User.objects.filter(role="OWNER").first()


@login_required
def accueil_manager(request):
    # toutes les entreprises du propriétaire
    # entreprises = Entreprise.objects.filter(owner=request.user)
    # entreprise = Entreprise.objects.filter(owner=request.user).first()
    entreprise = Entreprise.objects.get(id=1)

    print('entreprise, entreprise.nom:', entreprise, entreprise.owner)
    if not entreprise:
        print("pas d'entreprise")

        # entreprise = Entreprise.objects.filter(gerant=request.user).first()
        # entreprise = Entreprise.objects.filter(owner=request.user)

    return render(request, "frontend/accueil_manager.html", {
        "entreprise": entreprise,
        "is_owner": True,
        "gerant_id": request.user.id,
        "gerant": request.user,
    })


@login_required
def accueil_gerant(request):
    # Premièrement, tenter de récupérer l'entreprise où le user est gérant
    entreprise = Entreprise.objects.filter(gerant=request.user).first()
    # Sinon, la rendre propriétaire (OWNER)
    if not entreprise:
        entreprise = Entreprise.objects.filter(owner=request.user).first()
        print('entreprise:', entreprise)
    # entreprise = get_entreprise_from_gerant(request.user)
    entreprise_nom = entreprise.nom

    manager = get_owner()

    return render(request, "frontend/accueil_gerant.html", {
        # "entreprise_name": entreprise_name,
        "entreprise": entreprise,
        "entreprise_nom": entreprise_nom,
        "is_manager": True,
        "manager": manager,
        # "entreprise_id": entreprise_id if entreprise else None,
    })




def pgc_entreprise(request, entreprise_id):
    entreprise = Entreprise.objects.get(id=entreprise_id)

    classe = request.GET.get("classe")  # ex: "4"
    comptes = CompteComptable.objects.filter(entreprise=entreprise)

    if classe:
        comptes = comptes.filter(numero__startswith=classe)

    paginator = Paginator(comptes, 150)   # 50 par page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "frontend/pgc_entreprise_new.html", {
        "entreprise": entreprise,
        "entreprise_nom": entreprise.nom,
        "entreprise_id": entreprise.id,
        "page_obj": page_obj,
        "classe": classe,
        "comptes": page_obj,  # pour garder ton for
    })



"""
@login_required
def liste_compte_entreprise(request, entreprise_id):
    # Premièrement, tenter de récupérer l'entreprise où le user est gérant
    # entreprise = Entreprise.objects.filter(gerant=request.user).first()
    entreprise = Entreprise.objects.get(id=entreprise_id)

    if entreprise.owner != request.user and entreprise.gerant != request.user:
        return HttpResponseForbidden("Vous n’avez pas accès à cette entreprise.")

    # Sinon, la rendre propriétaire (OWNER)
    if not entreprise:
        entreprise = Entreprise.objects.filter(owner=request.user).first()

    # Si toujours rien, on informe l'utilisateur
    if not entreprise:
        messages.warning(request, "Aucune entreprise associée à votre compte.")
        # rendre la page sans comptes (ou rediriger vers une page d'erreur/creation)
        return render(request, "frontend/pgc_entreprise_new.html", {
            "entreprise": None,
            "entreprise_nom": None,
            "entreprise_id": None,
            "comptes_id": CompteComptable.objects.none(),
        })

    entreprise_nom = entreprise.nom
    print('entreprise_nom:', entreprise_nom)

    comptes = CompteComptable.objects.filter(entreprise=entreprise).order_by('numero')
    # compte_liste = CompteComptable.objects.filter(entreprise=entreprise).all()
    print(f"📊 {comptes.count()} comptes trouvés pour {entreprise_nom}")

    # paginator = Paginator(compte_liste, 50)
    # page_number = request.GET.get('page')
    # comte_liste = paginator.get_page(page_number)

    return render(request, 'frontend/pgc_entreprise_new.html', {
        'entreprise': entreprise,
        'entreprise_nom': entreprise_nom,
        'entreprise_id': entreprise_id,
        'comptes': comptes,
        #'compte_liste': compte_liste,
    })
"""
"""
def accueil_dossier_compta(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    entreprise_nom = None
    entreprise_gerant = None
    # entreprise_active = None

    if request.user.is_authenticated:
        # test = Entreprise.objects.filter(owner=request.user)
        entreprise_nom = entreprise.nom
        entreprise_gerant = entreprise.nom_gerant
        # entreprise_nom = test[0].nom
        # entreprise_gerant = test[0].nom_gerant
        # entreprise_active = getattr(request.user, "entreprise", None)
        # print('entreprise_gerant, test:', entreprise.nom, entreprise.nom_gerant)
    # On sauvegarde l'entreprise active dans la session
    # request.session["entreprise_active_id"] = entreprise.id
    request.session["entreprise_active_id"] = entreprise_id

    # if User.objects.filter(role="GERANT").exists():
    return render(request, "frontend/accueil_dossier_comptable.html", {"entreprise": entreprise, "entreprise_nom": entreprise_nom, "entreprise_gerant": entreprise_gerant})
"""


def setup(request):
    role = request.GET.get("role")  # "GERANT" ou "EXPERT_COMPTABLE"
    # print('get role:', role)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user, entreprise = create_user_and_entreprise(
                nom_gerant=data["nom_gerant"],
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

@login_required
def create_compte(request, entreprise_id):
    entreprise = Entreprise.objects.get(id=entreprise_id)
    entreprise_nom = entreprise.nom
    print('entreprise, e.nom:', entreprise, entreprise_nom)


    # Sinon, la rendre propriétaire (OWNER)
    # if not entreprise:
        # entreprise = Entreprise.objects.filter(owner=request.user).first()

    if request.method == 'POST':
        compte_form = CompteForm(request.POST)
        if compte_form.is_valid():
            compte = compte_form.save(commit=False)
            compte.entreprise = entreprise        # ✅ Lier explicitement
            compte.origine = 'user'
            libelle = compte.nom
            # ✅ Marquer comme créé par utilisateur
            print('data_valid:', compte.origine, compte, compte.entreprise, libelle)
            compte.save()
            messages.success(request, 'Le compte a été créé avec succès !')
            return redirect('accueil-compta', entreprise_id=entreprise_id)
    else:
        compte_form = CompteForm()

    # request.session["entreprise_active_id"] = entreprise_id
    return render(request, 'frontend/create_compte.html', {
        'compte_form': compte_form,
        'entreprise': entreprise,
        'entreprise_nom': entreprise_nom,

        # 'entreprise_id': entreprise_id
    })


def liste_compte(request):
    return render(request, 'frontend/api_pgc.html')


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


def afficher_compte(request, entreprise_id):
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
    return render(request, 'frontend/afficher_compte.html', {'entreprise_id': entreprise_id, 'lignes': lignes, 'numero': numero, 'nom': nom})

"""

def update_compte(request, entreprise_id, compte_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    compte = get_object_or_404(CompteComptable, id=compte_id, entreprise=entreprise)

    if request.method == "POST":
        form = CompteForm(request.POST, instance=compte)
        print("POST reçu")  # pour vérifier que tu arrives là
        print(form.errors)  # <-- très important
        if form.is_valid():
            form.save()
            return redirect('pgc-entreprise', entreprise_id=entreprise_id)

    else:
        form = CompteForm(instance=compte)

    return render(request, "frontend/update_compte.html", {
        "entreprise": entreprise,
        "compte": compte,
        "form": form,
        "compte_id": compte_id,
        "entreprise_id": entreprise_id,
    })
"""

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

"""
def afficher_statut_entreprise(request):
    print('affichage_statuts')
    return render(request, 'frontend/afficher_modifier_dossier.html')
"""

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

