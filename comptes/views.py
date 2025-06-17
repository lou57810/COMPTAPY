from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .models import CompteComptable
from .serializers import CompteComptableSerializer
from django.contrib.auth.decorators import login_required  # , permission_required


"""
class CompteComptableViewSet(viewsets.ModelViewSet):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer

    def perform_create(self, serializer):
        serializer.save(origine='user')
"""

# @login_required
class CompteComptableListView(generics.ListAPIView):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer


class CompteComptableRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompteComptable.objects.all()
    serializer_class = CompteComptableSerializer
    lookup_field = "pk"
