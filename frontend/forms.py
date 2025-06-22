from django import forms

from comptes import models


class CompteForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom', 'origine']
