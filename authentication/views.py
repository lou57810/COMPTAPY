# from django.shortcuts import render
from django.views import View
# from .forms import UserLoginForm
from django.http import HttpResponseForbidden
from . import forms
from .forms import LoginForm # , OwnerSignupForm
from authentication.forms import OwnerFullSignupForm
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, viewsets
from django.shortcuts import render, redirect
from .serializers import GroupSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from api.utils import importer_pgc_pour_entreprise
from api.models import Entreprise
from authentication.forms import AddUserForm


User = get_user_model()




"""
# On peut protéger une vue comme ceci :
from authentication.permissions import role_required

@role_required(["OWNER", "ADMIN"])
def modifier_dossier(request):

"""

"""
def signup_owner(request):

    # Création unique du propriétaire (OWNER) du logiciel.

    if User.objects.filter(role="OWNER").exists():
        messages.error(request, "Un propriétaire (OWNER) est déjà enregistré.")
        return redirect("accueil")

    if request.method == "POST":
        form = OwnerSignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                # Forcer explicitement le rôle OWNER (sécurité)
                user.role = "OWNER"
                user.save()
                messages.success(request, f"Propriétaire {user.email} créé avec succès.")
                return redirect("login")
            except Exception as e:
                messages.error(request, f"Erreur : {e}")
    else:
        form = OwnerSignupForm(initial={"role": "OWNER"})  # UX : pré-remplir OWNER

    return render(request, "authentication/owner_signup_back.html", {"form": form})



def signup_owner(request):

    # Empêche plusieurs propriétaires
    if User.objects.filter(role="OWNER").exists():
        messages.error(request, "Un propriétaire (OWNER) est déjà enregistré.")
        return redirect("accueil")

    if request.method == "POST":
        form = OwnerSignupForm(request.POST)

        if form.is_valid():
            try:
                # 1️⃣ Création du propriétaire
                user = form.save(commit=False)
                user.role = "OWNER"
                user.save()

                # 2️⃣ Création de l'entreprise personnelle du propriétaire
                entreprise = Entreprise.objects.create(
                    nom = f"Entreprise de {user.email}",
                    owner = user,        # 🔥 IMPORTANT : ton modèle utilise 'owner' pour le propriétaire
                    gerant = None,       # pas de gérant pour une entreprise personnelle
                    nom_gerant = "Propriétaire",  # optionnel, pure cosmétique
                )

                # 3️⃣ Import du PGC automatiquement pour cette entreprise
                importer_pgc_pour_entreprise(entreprise)

                # 4️⃣ Message + redirection
                messages.success(
                    request,
                    f"Propriétaire {user.email} créé avec son entreprise personnelle."
                )

                return redirect("accueil-manager")

            except Exception as e:
                messages.error(request, f"Erreur interne : {e}")

    else:
        form = OwnerSignupForm(initial={"role": "OWNER"})

    return render(request, "authentication/owner_signup_back.html", {"form": form})
"""


def signup_owner(request):
    if User.objects.filter(role="OWNER").exists():
        messages.error(request, "Un propriétaire (OWNER) existe déjà.")
        return redirect("accueil")

    if request.method == "POST":
        form = OwnerFullSignupForm(request.POST)

        if form.is_valid():
            try:
                # 1️⃣ création du propriétaire
                user = form.save(commit=True)

                # 2️⃣ préparation données entreprise
                data = form.get_entreprise_data()

                # 3️⃣ création entreprise personnelle
                entreprise = Entreprise.objects.create(
                    owner=user,
                    gerant=None,
                    **data
                )

                # 4️⃣ import PGC
                importer_pgc_pour_entreprise(entreprise)

                messages.success(request, "Propriétaire et entreprise créés avec succès.")
                return redirect("accueil-manager")

            except Exception as e:
                messages.error(request, f"Erreur : {e}")

    else:
        form = OwnerFullSignupForm()

    return render(request, "authentication/owner_signup.html", {"form": form})

"""
@login_required
def creer_gerant(request):
    if request.user.role != "OWNER":
        return HttpResponseForbidden("Seul le propriétaire peut créer un gérant")

    if request.method == "POST":
        form = AddUserForm(request.POST)
        print('post:', form)
        print("ERREURS:", form.errors)  # ← Ajoute ceci
        if form.is_valid():
            gerant = form.save()
            print('gerant:', gerant)
            return redirect("creer-dossier", gerant_id=gerant.id)
    else:
        form = AddUserForm()

    return render(request, "api/create_gerant.html", {"form": form})

"""

@login_required
def creer_gerant(request):
    entreprise_name = Entreprise.objects.filter(owner=request.user).first()
    if request.method == "POST":
        form = AddUserForm(request.POST)

        if form.is_valid():
            try:
                # 1️⃣ création du gérant
                gerant = form.save(commit=True)
                print('gerant:', gerant)

                # 2️⃣ préparation données entreprise
                data = form.get_entreprise_data()

                # 3️⃣ création entreprise personnelle
                entreprise = Entreprise.objects.create(
                    owner=gerant,
                    gerant=None,
                    **data
                )

                # 4️⃣ import PGC
                importer_pgc_pour_entreprise(entreprise)

                messages.success(request, "Gérant et entreprise créés avec succès.")
                return redirect("accueil-manager")

            except Exception as e:
                messages.error(request, f"Erreur : {e}")

    else:
        form = AddUserForm()
    return render(request, "authentication/create_gerant.html", {"form": form, "entreprise_name": entreprise_name,})

"""
class LoginPage(View):

    form_class = LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class
        message = 'test fonction get'
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                print('user:', user)
                login(request, user)
                return redirect('accueil')
            else:
                message = 'Identifiants ou pass invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})
"""


class LoginPage(View):
    form_class = LoginForm
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class()  # ← corrige : on crée une instance
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''

        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)

                role = getattr(user, "role", None)
                print("LOGIN SUCCESS ROLE =", role)

                # 🔥 Redirection selon le rôle
                if role == "OWNER":
                    return redirect("accueil-manager")
                elif role == "GERANT":
                    return redirect("accueil-gerant")
                else:
                    return redirect("accueil")  # fallback

            else:
                message = "Identifiants ou mot de passe invalides."

        return render(request, self.template_name, context={'form': form, 'message': message})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]





"""
def signup_owner(request):
    # Vérifie s'il existe déjà un OWNER dans la base
    user_role = User.objects.filter(role="OWNER")
    print('user_signup_exist:', user_role)
    if User.objects.filter(role="OWNER").exists():
        messages.error(request, "Un propriétaire (OWNER) est déjà enregistré.")
        # return redirect("accueil")  # ou "accueil"
        return render(request, 'frontend/accueil_gerant.html')

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            print("✅ Formulaire signup_owner valide")
            # form.save()
            user = form.save()
            # login(request, user)    # Permet la connexion directement
            messages.success(request, "Compte créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = forms.SignupForm()
    return render(request, 'authentication/owner_signup_back.html', context={'form': form, 'user': user_role})

def signup_owner(request):

    # Création unique du propriétaire (OWNER) du logiciel.

    # Vérifie s'il existe déjà un OWNER
    if User.objects.filter(role="OWNER").exists():
        messages.error(request, "Un propriétaire (OWNER) est déjà enregistré.")
        return redirect("accueil")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            try:
                user = User.objects.create_user(
                    nom_gerant=data["nom_gerant"],
                    email=data["email"],
                    password=data["password1"],
                    role="OWNER",
                )

                messages.success(request, f"✅ Propriétaire {user.email} créé avec succès !")
                return redirect("login")  # ou "accueil"

            except Exception as e:
                messages.error(request, f"Erreur : {e}")

    else:
        form = SignupForm()

    return render(request, "authentication/owner_signup_back.html", {"form": form})

def signup_owner(request):
    # Vérifie s'il existe déjà un OWNER dans la base
    user_role = User.objects.filter(role="OWNER")
    # print('user_signup_exist:', user_role)
    if User.objects.filter(role="OWNER").exists():
        messages.error(request, "Un propriétaire (OWNER) est déjà enregistré.")
        # return redirect("accueil")  # ou "accueil"
        return render(request, 'frontend/accueil_gerant.html')

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user, entreprise = create_user_and_entreprise(
                nom_gerant=data["nom_gerant"],
                email=data["email"],
                password=data["password1"],
                role=data["role"],
                nom=data.get("nom"),
                siret=data.get("siret"),
                ape=data.get("ape"),
                adresse=data.get("adresse"),
                date_creation=data.get("date_creation"),
            )
            # return redirect("accueil")
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = forms.SignupForm()
    # return render(request, 'authentication/owner_signup_back.html', context={'form': form, 'user': user_role})
    return render(request, 'authentication/owner_signup_back.html', context={'form': form})
"""
def logout_user(request):
    logout(request)
    return redirect('accueil')


def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    # print('request.user:', request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})
