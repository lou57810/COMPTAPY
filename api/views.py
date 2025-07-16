from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import CompteComptableSerializer, EcritureJournalSerializer
from django.utils import timezone
from rest_framework.generics import ListAPIView

from .models import CompteComptable, EcritureJournal

# from .serializers import CompteComptableSerializer
from django.db.models.functions import Substr

"""
class CompteComptableListView(ListAPIView):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer
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


@api_view(['POST'])
def enregistrer_ecritures(request):
    lignes = request.data.get('lignes', [])

    for ligne in lignes:
        numero = ligne.get('numero')
        nom = ligne.get('nom')
        libelle = ligne.get('libelle') or ''
        debit = ligne.get('debit') or 0
        credit = ligne.get('credit') or 0

        CompteComptable.objects.create(
            numero=numero,
            nom=nom,
            libelle=libelle,
            debit=debit,
            credit=credit,
            date_saisie=timezone.now()
        )

    return Response({'message': 'Écritures enregistrées'}, status=status.HTTP_201_CREATED)


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



