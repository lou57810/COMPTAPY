from rest_framework import serializers
from .models import  EcritureJournal






class EcritureJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcritureJournal
        fields = '__all__'

