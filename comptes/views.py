# from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .models import CompteComptable
from .serializers import CompteComptableSerializer
from django.db.models.functions import Substr
# from django.contrib.auth.decorators import login_required  # , permission_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers



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
            numero_prefix=Substr('numero', 1, 3)
        ).order_by('numero_prefix', 'numero')


class CompteComptableRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer
    lookup_field = "pk"
"""


