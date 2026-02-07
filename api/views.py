from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from authentication.permissions import role_required
from django.contrib import messages
from django.views.decorators.http import require_POST
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

def liste_comptes(request):
    return render(request, 'api/api_pgc.html')


@require_POST
def auto_create_compte(request, entreprise_id):
    entreprise = Entreprise.objects.get(id=entreprise_id)
    data = json.loads(request.body)

    numero_saisi = data.get("numero")
    nom_saisi = data.get("nom")
    type_journal = data.get("journal_type")

    # Déterminer client/fournisseur
    if type_journal == "achats":
        compte = CompteComptable.objects.create(
            entreprise=entreprise,
            nom=nom_saisi or f"Fournisseur {numero_saisi}",
            is_fournisseur=True
        )

    elif type_journal == "ventes":
        compte = CompteComptable.objects.create(
            entreprise=entreprise,
            nom=nom_saisi or f"Client {numero_saisi}",
            is_client=True
        )

    return JsonResponse({
        "numero": compte.numero,
        "nom": compte.nom
    })


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



# Affiche la liste des dossiers entreprises et modifiables avec des boutons
@login_required
@role_required(["OWNER"])
def afficher_modifier_dossier(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)

    # Sinon, la rendre propriétaire (OWNER)
    if not entreprise:
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

    if request.user.role == "OWNER": # and entreprise.owner == request.user:
        owner = entreprise.owner  # sauvegarde avant suppression
        entreprise.delete()
        messages.success(request, f"L'entreprise '{entreprise.nom}' a été supprimée.")
        return redirect("liste-entreprises")

    else:
        messages.error(request, "Action non autorisée.")
        return redirect("liste-entreprises")


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



