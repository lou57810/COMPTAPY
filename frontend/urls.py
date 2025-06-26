# -*- coding: utf-8 -*

from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path("journaux/", include("journaux.urls")),
    path("pgc/", views.liste_compte, name="pgc"),
    path("formulaire-compte/", views.ajout_modif_compte, name="compte_form"),
    path('frontend/create/', views.create_compte, name='create_compte'),
    # path('frontend/update/', views.update_compte, name='update_compte'),
    # path('comptes/', views.compte_num_list, name='compte_num_list'),
    path('frontend/list/', views.compte_num_list, name='compte_num_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

