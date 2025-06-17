from rest_framework import serializers
from .models import CompteComptable


class CompteComptableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompteComptable
        fields = '__all__'

