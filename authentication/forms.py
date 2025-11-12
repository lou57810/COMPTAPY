from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(UserCreationForm):

    email = forms.EmailField(label="Email", required=True)
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

    # Champs optionnels pour entreprise
    # full_name = forms.CharField(label="Full Name", required=False)
    nom_gerant = forms.CharField(label="Full Name", required=False)
    nom = forms.CharField(label="Nom de l’entreprise", required=False)
    siret = forms.CharField(label="SIRET", required=False)
    ape = forms.CharField(label="Code APE", required=False)
    adresse = forms.CharField(widget=forms.Textarea, required=False)
    date_creation = forms.DateField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User  # ✅ ton modèle personnalisé
        fields = ["email", "role", "nom", "nom_gerant", "siret", "ape", "adresse", "date_creation", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
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


class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['profile_photo']


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput, max_length=64)


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "role", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

"""
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

"""

