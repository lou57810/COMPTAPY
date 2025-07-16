from django import forms

from api import models


class CompteSearchForm(forms.Form):
        numero = forms.CharField(label="Numéro du compte", required=True)


class CompteForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom']

class UpdateCompteForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom']


class CompteEditForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom']  # Les champs que tu autorises à modifier
