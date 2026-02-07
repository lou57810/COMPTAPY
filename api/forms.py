from django import forms

from api import models
from .models import Entreprise
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CompteSearchForm(forms.Form):
    numero = forms.CharField(label="Numéro du compte", required=True)


class CompteForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom', "is_client", "is_fournisseur"]


class UpdateCompteForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom']


class CompteEditForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom']  # Les champs que tu autorises à modifier




class EntrepriseModifForm(forms.ModelForm):
    email = forms.EmailField(label="Email Gérant", required=False)
    # password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe", required=True)
    role = forms.ChoiceField(
        choices=[
            ("OWNER", "OWNER"),
            ("GERANT", "Gérant / Cogérant"),
        ],
        label="Rôle",
        required=True
    )

    class Meta:
        model = models.Entreprise
        fields = ["nom", "adresse", "nom_gerant", "siret", "ape", "date_creation"]

        # fields = ["email", "role", "nom", "nom_gerant", "siret", "ape", "adresse", "date_creation", "password1", "password2"]

        def __init__(self, *args, **kwargs):
            # On attend une instance d’entreprise + on récupère l'email du gérant
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.owner:
                self.fields['email'].initial = self.instance.owner.email

        # Champs optionnels pour entreprise
        nom_gerant = forms.CharField(label="Full Name", required=False)
        nom = forms.CharField(label="Nom de l’entreprise", required=False)
        siret = forms.CharField(label="SIRET", required=False)
        ape = forms.CharField(label="Code APE", required=False)
        adresse = forms.CharField(widget=forms.Textarea, required=False)
        date_creation = forms.DateField(required=False)

    def save(self, commit=True):
        entreprise = super().save(commit=False)
        # test = entreprise.owner.email
        email = self.cleaned_data['email']
        user = entreprise.owner
        # user.email = email
        # user.save(update_fields=['email'])
        if commit:
            entreprise.save()
        return entreprise


class FolderForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ["nom", "siret", "ape", "adresse", "date_creation"]

        widgets = {
            "date_creation": forms.DateInput(attrs={"type": "date"}),
        }
