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
from django.http import JsonResponse


User = get_user_model()




"""
# On peut protéger une vue comme ceci :
from authentication.permissions import role_required

@role_required(["OWNER", "ADMIN"])
def modifier_dossier(request):

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
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            try:
                # 1️⃣ création du gérant
                gerant = form.save(commit=True)
                print('gerant', gerant)

                # 2️⃣ récupération des données pour sa nouvelle entreprise
                data = form.get_entreprise_data()
                print('data, REQUEST.USER, GERANT: \n', data, request.user, gerant)

                # 3️⃣ création de SON entreprise (distincte du propriétaire)
                entreprise = Entreprise.objects.create(
                    owner=request.user,  # le propriétaire reste owner !
                    gerant=gerant,       # le nouveau user devient gérant
                    **data
                )

                # 4️⃣ import PGC (une seule fois par entreprise)
                importer_pgc_pour_entreprise(entreprise)

                messages.success(request, "Gérant et entreprise créés avec succès.")
                return redirect("accueil-manager")

            except Exception as e:
                messages.error(request, f"Erreur : {e}")

    else:
        form = AddUserForm()

    return render(request, "authentication/create_gerant.html", {
        "form": form,
    })
"""



@login_required
def creer_gerant(request):
    entreprise_name = Entreprise.objects.filter(owner=request.user).first()
    print('entreprise_manager_name', entreprise_name)
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            try:
                # 1️⃣ création du gérant
                gerant = form.save(commit=True)
                print('gerant', gerant)

                # 2️⃣ récupération des données pour l’entreprise du gérant
                data = form.get_entreprise_data()
                print('data, REQUEST.USER, GERANT: \n', data, request.user, gerant)

                # 3️⃣ création de SON entreprise
                entreprise = Entreprise.objects.create(
                    owner=request.user,
                    gerant=gerant,
                    **data
                )
                print("ENTREPRISE", entreprise)
                # 4️⃣ import PGC
                importer_pgc_pour_entreprise(entreprise)


                print('Re test entreprise.id:', entreprise.id)
                # Sinon → redirection classique
                # messages.success(request, "Gérant et entreprise créés avec succès.")
                return redirect("accueil-manager")

            except Exception as e:
                messages.error(request, f"Erreur : {e}")

    else:
        form = AddUserForm()

    return render(request, "api/create_gerant.html", {
        "form": form,
    })

"""
@login_required
def creer_gerant(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            try:
                # 1️⃣ création du gérant
                gerant = form.save(commit=True)

                # 2️⃣ données entreprise
                data = form.get_entreprise_data()

                # 3️⃣ création entreprise
                entreprise = Entreprise.objects.create(
                    owner=request.user,
                    gerant=gerant,
                    **data
                )

                # 4️⃣ import PGC
                importer_pgc_pour_entreprise(entreprise)

                print("ENTREPRISE CRÉÉE AVEC ID =", entreprise.id)

                # 5️⃣ SI appel AJAX → renvoyer l’ID
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({
                        "success": True,
                        "gerant_id": gerant.id,
                        "entreprise_id": entreprise.id,
                    })

                # 6️⃣ sinon → redirection normale
                messages.success(request, "Gérant et entreprise créés avec succès.")
                return redirect("accueil-manager")

            except Exception as e:
                messages.error(request, f"Erreur : {e}")

    else:
        form = AddUserForm()

    return render(request, "authentication/create_gerant_js.html", {"form": form})
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
