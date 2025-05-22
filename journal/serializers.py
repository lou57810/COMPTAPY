from rest_framework import serializers
from .models import Compte, EcritureJournal



class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = '__all__'


class EcritureJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcritureJournal
        fields = '__all__'

