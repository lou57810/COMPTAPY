from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from authentication.permissions import role_required
from django.contrib import messages
from authentication.forms import SignupForm
from .utils import create_user_and_entreprise
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FolderForm, EntrepriseModifForm, CompteForm  # EntrepriseForm,
from .serializers import CompteComptableSerializer, EcritureJournalSerializer
from django.utils import timezone
from django.db import IntegrityError
from .models import CompteComptable, EcritureJournal, Entreprise, Journal
from django.db.models.functions import Substr

from rest_framework import generics, permissions
from .utils import get_accessible_entreprises, importer_pgc_pour_entreprise, get_entreprise_from_gerant
from django.core.paginator import Paginator
from django.http import JsonResponse
User = get_user_model()
from django.http import JsonResponse
from datetime import datetime
import json
from . import forms


"""
class CreateEntrepriseAPIView(generics.CreateAPIView):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        # L’entreprise est liée à l’utilisateur connecté
        serializer.save(owner=self.request.user)
"""

@login_required
def liste_entreprises(request):
    # entreprise_name = Entreprise.objects.filter(owner=request.user).first()
    entreprise = Entreprise.objects.filter(owner=request.user)
    entreprise_nom = entreprise[0].nom
    entreprises = get_accessible_entreprises(request.user)

    return render(request, "api/liste_entreprises.html",
                  {"entreprises": entreprises,
                   "entreprise_nom": entreprise_nom
                   })

"""
@login_required
def creer_dossier_gerant(request, gerant_id):
    print('gerant_id:', gerant_id)
    gerant = get_object_or_404(User, id=gerant_id)

    if request.user.role != "OWNER":
        return HttpResponseForbidden("Permission refusée")

    if request.method == "POST":
        form = FolderForm(request.POST)
        print("DEBUG - folder form errors:", form.errors)  # <--- utile pour debug
        if form.is_valid():
            entreprise = form.save(commit=False)
            # entreprise.created_by = gerant  # liaison entreprise → gérant
            # Lier la bonne relation User <-> Entreprise selon ce qui existe dans le modèle
            if hasattr(entreprise, "gerant"):
                entreprise.gerant = gerant
            elif hasattr(entreprise, "created_by"):
                entreprise.created_by = gerant
            else:
                # Par défaut, on rattache le owner (le comptable) ; si tu veux rattacher le gérant,
                # adapte selon ton modèle (ou ajoute le champ gerant dans le modèle Entreprise).
                entreprise.owner = request.user
            entreprise.save()
            importer_pgc_pour_entreprise(entreprise)
            # return redirect("dashboard")
            return redirect("accueil-manager") # C'est le propriétaire manager qui créée les dossiers et leurs gérants.
    else:
        form = FolderForm()

    return render(request, "api/ajouter_dossier.html", {
        "form": form,
        "gerant": gerant,
        "gerant_id": gerant_id
    })
"""
"""
@login_required
def creer_dossier_owner(request, user_id):
    print('user_id:', user_id)
    gerant = get_object_or_404(User, id=user_id)

    if request.user.role != "OWNER":
        return HttpResponseForbidden("Permission refusée")

    if request.method == "POST":
        form = FolderForm(request.POST)
        print("DEBUG - folder form errors:", form.errors)  # <--- utile pour debug
        if form.is_valid():
            entreprise = form.save(commit=False)
            # entreprise.created_by = gerant  # liaison entreprise → gérant
            # Lier la bonne relation User <-> Entreprise selon ce qui existe dans le modèle
            if hasattr(entreprise, "gerant"):
                entreprise.gerant = gerant
            elif hasattr(entreprise, "created_by"):
                entreprise.created_by = gerant
            else:
                # Par défaut, on rattache le owner (le comptable) ; si tu veux rattacher le gérant,
                # adapte selon ton modèle (ou ajoute le champ gerant dans le modèle Entreprise).
                entreprise.owner = request.user
            entreprise.save()
            importer_pgc_pour_entreprise(entreprise)
            # return redirect("dashboard")
            return redirect("accueil-manager")
    else:
        form = FolderForm()

    return render(request, "api/ajouter_dossier.html", {
        "form": form,
        "gerant": gerant,
        "gerant_id": user_id
    })
"""



"""
def liste_compte(request):
    return render(request, 'api/api_pgc.html', )
"""
def update_compte(request, entreprise_id, compte_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    compte = get_object_or_404(
        CompteComptable,
        id=compte_id,
        entreprise=entreprise
    )

    if request.method == "POST":
        form_edit = forms.UpdateCompteForm(request.POST, request.FILES, instance=compte)
        if form_edit.is_valid():
            form_edit.save()
           # return redirect('update-compte', entreprise_id=entreprise.id, compte_id=compte.id)
            return redirect('pgc-entreprise', entreprise_id=entreprise.id)
    else:
        form_edit = forms.UpdateCompteForm(instance=compte)

    return render(request, 'api/update_compte.html', {
        'entreprise': entreprise,
        'compte': compte,
        'form_edit': form_edit,
    })





"""
def update_compte(request, entreprise_id, compte_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    compte = get_object_or_404(CompteComptable, id=compte_id, entreprise=entreprise)

    if request.method == "POST":
        form = CompteForm(request.POST, instance=compte)
        print("POST reçu")  # pour vérifier que tu arrives là
        print('form_errors:', form.errors)  # <-- très important
        if form.is_valid():
            form.save()
            return redirect('pgc-entreprise', entreprise_id=entreprise_id)

    else:
        form = CompteForm(instance=compte)

    return render(request, "api/update_compte_back.html", {
        "entreprise": entreprise,
        "compte": compte,
        "form": form,
        "compte_id": compte_id,
        "entreprise_id": entreprise_id,
    })


def update_compte(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    # compte = get_object_or_404(CompteComptable, id=compte_id, entreprise=entreprise)
    compte = get_object_or_404(CompteComptable, entreprise=entreprise)
    entreprise_nom = entreprise.nom
    # compte_numero = compte.numero
    # print('entreprise_nom:', entreprise_nom, compte_numero)


    if request.method == "POST":
        form = CompteForm(request.POST, instance=compte)
        if form.is_valid():
            compte_modifie = form.save(commit=False)

            # 👉 Mise à jour du libellé uniquement pour les comptes user
            if compte_modifie.origine == "user":
                compte_modifie.libelle = compte_modifie.nom

            compte_modifie.save()

            return redirect('pgc-entreprise', entreprise_id=entreprise_id)

    else:
        form = CompteForm(instance=compte)

    return render(request, "api/update_compte.html", {
        "entreprise": entreprise,
        "compte": compte,
        "form": form,
        # "compte_id": compte_id,
        "entreprise_id": entreprise_id,
        "entreprise_nom": entreprise_nom,
    })
"""


@login_required
@role_required(["OWNER"])
def afficher_modifier_dossier(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)

    # Sinon, la rendre propriétaire (OWNER)
    if not entreprise:
        # entreprise = Entreprise.objects.filter(owner=request.user).first()
    # entreprise_nom = entreprise.nom
    # print('entreprise_nom:', entreprise.nom)
    # nom_gerant = entreprise.nom_gerant
        # entreprise_nom = entreprise.nom
        # print('entreprise_nom:', entreprise.nom)
        # nom_gerant = entreprise.nom_gerant
    # if not entreprise:
        return redirect("create-folder")

    if request.method == "POST":
        form = EntrepriseModifForm(request.POST, instance=entreprise)
        if form.is_valid():
            print('Valid')
            form.save()

            # entreprise.owner.email = form.cleaned_data["email"]
            entreprise.owner.email = form.cleaned_data["email"]
            # entreprise.owner.save(update_fields=["email"])
            entreprise.owner.save(update_fields=["email"])
            return redirect("liste-entreprises")
    else:

        form = EntrepriseModifForm(instance=entreprise, initial={
        "email": entreprise.owner.email if entreprise.owner else ""
        })
        print('unvalid')
    entreprise_nom = entreprise.nom
    nom_gerant = entreprise.nom_gerant

    return render(request, "api/afficher_modifier_dossier.html",
                  {"form": form,
                   "entreprise": entreprise,
                   'entreprise_nom': entreprise_nom,
                   "entreprise_id": entreprise_id,
                   "nom_gerant": nom_gerant}
                  )


@login_required
def supprimer_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)

    # Vérifie si l'utilisateur connecté est bien le propriétaire
    print("Request_user_role", request.user.role, "entreprise_owner_email", entreprise.owner, "request_user", request.user)
    # reponse requestuserrole = owner
    # entrepriseowner = test@localhost
    # request.user = ben@localhost
    if request.user.role == "OWNER": # and entreprise.owner == request.user:
        owner = entreprise.owner  # sauvegarde avant suppression
        entreprise.delete()
        messages.success(request, f"L'entreprise '{entreprise.nom}' a été supprimée.")
        """
        # Vérifie si c'était la dernière entreprise de ce propriétaire
        if not Entreprise.objects.filter(owner=owner).exists():
            owner.delete()  # supprime le compte propriétaire
            messages.info(request, "Le compte propriétaire a été supprimé car il n'avait plus d'entreprises.")
            return redirect("signup")  # retour vers l'écran d'inscription
        else:
        """
        return redirect("liste-entreprises")

    else:
        messages.error(request, "Action non autorisée.")
        return redirect("liste-entreprises")


"""
class CompteComptableViewSet(viewsets.ModelViewSet):
    serializer_class = CompteComptableSerializer

    # Tri numéro PGC en fonction des 3 premiers chiffres
    def get_queryset(self):
        return CompteComptable.objects.annotate(
            numero_prefix=Substr('numero', 1, 3)
        ).order_by('numero_prefix', 'numero')

    def perform_create(self, serializer):
        serializer.save(origine='user')
"""

class CompteComptableViewSet(viewsets.ModelViewSet):
    serializer_class = CompteComptableSerializer

    def get_queryset(self):
        qs = CompteComptable.objects.all()

        entreprise_id = self.request.query_params.get("entreprise_id")
        if entreprise_id:
            qs = qs.filter(entreprise_id=entreprise_id)

        return qs.order_by("numero")


# @login_required
class CompteComptableListView(generics.ListAPIView):
    serializer_class = CompteComptableSerializer

    # Tri numéro PGC en fonction des 3 premiers chiffres
    def get_queryset(self):
        return CompteComptable.objects.annotate(
            numero_prefix=Substr('numero', 1, 6)
        ).order_by('numero_prefix', 'numero')


class CompteComptableRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer
    lookup_field = "pk"


@api_view(['GET'])
def get_compte_by_numero(request):
    numero = request.GET.get('numero')
    # if numero is None:
    if not numero:
        return Response({'error': 'Numéro manquant'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        compte = CompteComptable.objects.get(numero=numero)
        serializer = CompteComptableSerializer(compte)
        return Response(serializer.data)
    except CompteComptable.DoesNotExist:
        return Response({'error': 'Compte introuvable'}, status=status.HTTP_404_NOT_FOUND)


def compte_par_numero(request, entreprise_id):
    numero = request.GET.get("numero")

    compte = CompteComptable.objects.filter(
        entreprise_id=entreprise_id,
        numero=numero
    ).first()
    print('compte_par_numero', compte)
    if not compte:
        return JsonResponse({}, status=404)

    return JsonResponse({
        "numero": compte.numero,
        "nom": compte.libelle,
    })


"""
def journal_ecritures(request, entreprise_id):
    journal_type = request.GET.get("type")  # achats, ventes, etc.

    ecritures = EcritureJournal.objects.filter(
        entreprise_id=entreprise_id,
        journal=journal_type
    ).order_by("date", "id")

    data = []
    for e in ecritures:
        data.append([
            e.date.strftime("%d/%m/%Y"),
            e.compte.numero,
            e.compte.libelle,
            e.numero_piece,
            e.libelle,
            "", "", "",   # PU, Qté, TVA (selon ton modèle)
            float(e.debit),
            float(e.credit),
        ])

    return JsonResponse({"data": data})

def saisie_journal(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    print('entreprise:', entreprise)

    if not entreprise:
        messages.warning(request, "Veuillez d'abord sélectionner une entreprise.")
        return redirect("liste-entreprises")
    type_journal = request.GET.get('type', '')  # Par défaut : journal achats
    print('type_journal:', type_journal)
    context = {
        'type_journal': type_journal, "entreprise": entreprise
    }
    return render(request, 'frontend/journal_accueil.html', context)


def journal_ecritures(request, entreprise_id):
    journal_type = request.GET.get("type")
    print('Journal_Type, entreprise_id:', journal_type, entreprise_id)

    if not journal_type:
        return JsonResponse(
            {"error": "Type de journal manquant"},
            status=400
        )

    journal = get_object_or_404(
        Journal,
        entreprise_id=entreprise_id,
        type=journal_type
    )

    ecritures = (
        EcritureJournal.objects
        .filter(
            journal=journal,
            # entreprise=journal.entreprise,
        )
        .order_by("date", "id")
    )

    data = []
    for e in ecritures:
        data.append([
            e.date.strftime("%d/%m/%Y"),
            e.compte.numero,
            e.compte.libelle,
            e.numero_piece,
            e.libelle,
            float(e.pu_ht),
            float(e.quantite),
            float(e.taux),
            float(e.debit),
            float(e.credit),
        ])

    return JsonResponse({"data": data})
"""



"""
@api_view(['POST'])
def enregistrer_ecritures(request):
    lignes = request.data.get('lignes', [])

    for ligne in lignes:
        numero = ligne.get('numero')
        nom = ligne.get('nom')
        numero_piece = ligne.get('numero_piece')
        libelle = ligne.get('libelle') or ''
        debit = ligne.get('debit') or 0
        credit = ligne.get('credit') or 0

        CompteComptable.objects.create(
            numero=numero,
            nom=nom,
            numero_piece=numero_piece,
            libelle=libelle,
            debit=debit,
            credit=credit,
            date_saisie=timezone.now()
        )

    return Response({'message': 'Écritures enregistrées'}, status=status.HTTP_201_CREATED)

"""
@api_view(['GET'])
def get_ecritures_par_compte(request):
    numero = request.GET.get('numero')

    if numero:
        ecritures = EcritureJournal.objects.filter(compte__numero=numero).order_by('date')

        data = [
            {
                'date': ecriture.date.strftime('%d/%m/%Y'),
                'numero': ecriture.compte.numero,
                'nom': ecriture.nom,
                'numero_piece': ecriture.numero_piece,
                'libelle': ecriture.libelle,
                'debit': ecriture.debit,
                'credit': ecriture.credit
            }
            for ecriture in ecritures
        ]

        return Response(data, status=status.HTTP_200_OK)

    return Response({'message': 'Numéro de compte manquant'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ecritures_par_compte(request):
    numero = request.GET.get('numero')
    if numero:
        ecritures = EcritureJournal.objects.filter(compte__numero=numero).order_by('date')
        serializer = EcritureJournalSerializer(ecritures, many=True)
        return Response(serializer.data)
    return Response({'error': 'Numéro de compte requis'}, status=400)



