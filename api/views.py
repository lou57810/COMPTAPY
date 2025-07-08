# from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from .models import CompteComptable
from comptes import models, serializers
# from .serializers import CompteComptableSerializer
from django.db.models.functions import Substr


class CompteComptableViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompteComptableSerializer

    # Tri numéro PGC en fonction des 3 premiers chiffres
    def get_queryset(self):
        return models.CompteComptable.objects.annotate(
            numero_prefix=Substr('numero', 1, 3)
        ).order_by('numero_prefix', 'numero')

    def perform_create(self, serializer):
        serializer.save(origine='user')


# @login_required
class CompteComptableListView(generics.ListAPIView):
    serializer_class = serializers.CompteComptableSerializer

    # Tri numéro PGC en fonction des 3 premiers chiffres
    def get_queryset(self):
        return models.CompteComptable.objects.annotate(
            numero_prefix=Substr('numero', 1, 3)
        ).order_by('numero_prefix', 'numero')


class CompteComptableRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CompteComptable.objects.all()
    serializer_class = serializers.CompteComptableSerializer
    lookup_field = "pk"


@api_view(['GET'])
def get_compte_by_numero(request):
    numero = request.GET.get('numero')
    # if numero is None:
    if not numero:
        return Response({'error': 'Numéro manquant'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        compte = models.CompteComptable.objects.get(numero=numero)
        serializer = serializers.CompteComptableSerializer(compte)
        return Response(serializer.data)
    except models.CompteComptable.DoesNotExist:
        return Response({'error': 'Compte introuvable'}, status=status.HTTP_404_NOT_FOUND)
