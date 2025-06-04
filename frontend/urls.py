from . import views
from django.urls import path, include




urlpatterns = [

    #router.register(r'', views.accueil, basename='accueil'),
    path('', views.accueil, name='accueil'),
    path("journaux/", include("journaux.urls")),
]