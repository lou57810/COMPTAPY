# from django.shortcuts import render
from django.views import View
from . import forms
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, viewsets
from django.shortcuts import render, redirect
from .serializers import GroupSerializer, UserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginPage(View):
    form_class = forms.LoginForm
    # template_name = 'authentication/login_back.html'
    template_name = 'authentication/login.html'

    def get(self, request):
        form = self.form_class
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('accueil')
            else:
                message = 'Identifiants ou pass invalides.'
        return render(
            request, self.template_name, context={'form': form, 'message': message})


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


def signup_page(request):
    # form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            # user = form.save()
            form.save()
            # login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = forms.SignupForm()
    return render(request, 'authentication/signup.html', context={'form': form})


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
