from django.shortcuts import render
import requests
from PIL import Image




def accueil(request):
    return render(request,'frontend/accueil.html')
