from django import forms

from api import models
from .models import Entreprise
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()



class CompteSearchForm(forms.Form):
    numero = forms.CharField(label="Numéro du compte", required=True)


class CompteForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'libelle']


class UpdateCompteForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom']


class CompteEditForm(forms.ModelForm):
    class Meta:
        model = models.CompteComptable
        fields = ['numero', 'nom']  # Les champs que tu autorises à modifier


"""
class EntrepriseForm(forms.ModelForm):
    email = forms.EmailField(label="Email Gérant", required=False)
    # password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe", required=True)
    role = forms.ChoiceField(
        choices=[
            ("OWNER", "Propriétaire"),
            ("GERANT", "Gérant / Cogérant"),
            ("EXPERT_COMPTABLE", "Expert-Comptable"),
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
        user.email = email
        user.save(update_fields=['email'])
        if commit:
            entreprise.save()
        return entreprise
"""
"""
class EntrepriseModifForm(forms.ModelForm):
    email = forms.EmailField(label="Email Gérant", required=False)
    # password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe", required=True)
    # gerant = forms.CharField(label="Full Name", required=False)
    gerant = forms.CharField(label="Full Name", required=False)
    role = forms.ChoiceField(
        choices=[
            ("OWNER", "Propriétaire"),
            ("GERANT", "Gérant / Cogérant"),
            ("EXPERT_COMPTABLE", "Expert-Comptable"),
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
        user = entreprise.gerant.nom_gerant
        print('USER_user:', user)
        # user.email = email
        # user.save(update_fields=['email'])
        email = entreprise.gerant
        # user.save(update_fields=['nom_gerant'])
        if commit:
            entreprise.save()
        return entreprise
"""
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

"""
class FolderForm(UserCreationForm):

    # Champs optionnels pour entreprise
    nom_gerant = forms.CharField(label="Full Name", required=False)
    nom = forms.CharField(label="Nom de l’entreprise", required=False)
    siret = forms.CharField(label="SIRET", required=False)
    ape = forms.CharField(label="Code APE", required=False)
    adresse = forms.CharField(widget=forms.Textarea, required=False)
    date_creation = forms.DateField(required=False)

    # class Meta(UserCreationForm.Meta):
    class Meta:
        model = User  # ✅ ton modèle personnalisé
        fields = ["email", "role", "nom", "nom_gerant", "siret", "ape", "adresse", "date_creation", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print('EMAIL:', email)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un utilisateur avec cet email existe déjà.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        print('DATAFORM:', user, user.email, user.role)
        if commit:
            user.save()
        return user

    def save(self, commit=True):
        entreprise = super().save(commit=False)

        email = self.cleaned_data['email']
        print('EMAIL:', email)
        # user = super().save(commit=False)
        user = entreprise.owner
        print('USER_email:', user)
        # user.email = self.cleaned_data["email"]
        user.email = email
        user.save(update_fields=['email'])
        # user.role = self.cleaned_data["role"]
        # print('DATAFORM:', user, user.email, user.role)
        if commit:
            entreprise.save()
        return entreprise


class FolderForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ["nom", "nom_gerant", "siret", "ape", "adresse", "date_creation"]
        widgets = {
            "date_creation": forms.DateInput(attrs={"type": "date"}),
            "adresse": forms.Textarea(attrs={"rows": 3}),
        }



class FolderForm(UserCreationForm):
    email = forms.EmailField(label="Email du gérant", required=True)
    nom_gerant = forms.CharField(label="Nom complet du gérant", required=True)

    # Champs entreprise
    nom = forms.CharField(label="Nom de l’entreprise", required=True)
    siret = forms.CharField(label="SIRET", required=False)
    ape = forms.CharField(label="Code APE", required=False)
    adresse = forms.CharField(widget=forms.Textarea, required=False)
    date_creation = forms.DateField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "nom_gerant", "email",
            "password1", "password2",
            "nom", "siret", "ape", "adresse", "date_creation"
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un utilisateur avec cet email existe déjà.")
        return email
"""

class FolderForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ["nom", "siret", "ape", "adresse", "date_creation"]

        widgets = {
            "date_creation": forms.DateInput(attrs={"type": "date"}),
        }
