from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model

from . import forms

# Create your views here.
# user = get_user_model()


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


def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    print('request.user:', request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('accueil')

