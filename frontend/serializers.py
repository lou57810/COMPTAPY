from rest_framework import serializers
from comptes.models import CompteComptable


class CompteComptableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompteComptable
        fields = '__all__'
