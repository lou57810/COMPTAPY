# from django.shortcuts import render
from django.views import View
# from .forms import UserLoginForm
from . import forms
from .forms import LoginForm
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, viewsets
from django.shortcuts import render, redirect
from .serializers import GroupSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import SignupForm
from api.utils import create_user_and_entreprise


User = get_user_model()




"""
# On peut protéger une vue comme ceci :
from authentication.permissions import role_required

@role_required(["OWNER", "ADMIN"])
def modifier_dossier(request):
    ...
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
            # print("Existe-t-il ?", User.objects.filter(email=form.cleaned_data['email']).exists())
            # print('Form valid, email, password: ', form.cleaned_data['email'], form.cleaned_data['password'])
            user = authenticate(request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            print('User: ', user)
            if user is not None:
                print('user:', user)
                login(request, user)
                return redirect('accueil')
            else:
                message = 'Identifiants ou pass invalides.'
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
        return render(request, 'frontend/accueil.html')

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
    return render(request, 'authentication/owner_signup.html', context={'form': form, 'user': user_role})
"""


def signup_owner(request):
    # Vérifie s'il existe déjà un OWNER dans la base
    user_role = User.objects.filter(role="OWNER")
    # print('user_signup_exist:', user_role)
    if User.objects.filter(role="OWNER").exists():
        messages.error(request, "Un propriétaire (OWNER) est déjà enregistré.")
        # return redirect("accueil")  # ou "accueil"
        return render(request, 'frontend/accueil.html')

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user, entreprise = create_user_and_entreprise(
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
    return render(request, 'authentication/owner_signup.html', context={'form': form, 'user': user_role})

def logout_user(request):
    logout(request)
    return redirect('accueil')


def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    print('request.user:', request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})
