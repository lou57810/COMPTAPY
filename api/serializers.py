from rest_framework import serializers
from .models import CompteComptable, EcritureJournal



class CompteComptableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompteComptable
        fields = '__all__'


class EcritureJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcritureJournal
        fields = '__all__'

