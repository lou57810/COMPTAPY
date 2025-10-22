from rest_framework import serializers
from .models import CompteComptable, EcritureJournal, Entreprise


class CompteComptableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompteComptable
        fields = '__all__'


class EcritureJournalSerializer(serializers.ModelSerializer):
    # numero = serializers.CharField(source='compte.numero')
    # nom = serializers.CharField(source='compte.nom')

    class Meta:
        model = EcritureJournal
        fields = ['date', 'numero_piece', 'libelle', 'debit', 'credit']


class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = '__all__'
