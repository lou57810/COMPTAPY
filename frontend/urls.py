# -*- coding: utf-8 -*

from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path("pgc/", views.liste_compte, name="pgc"),
    path("update_compte/", views.update_compte, name="update_compte"),
    path('frontend/create/', views.create_compte, name='create_compte'),
    path('frontend/list/', views.display_compte, name='display_compte'),  # Affiche un compte depuis son numero
    path('saisie_journal/', views.saisie_journal, name='saisie-journal'),
    path('valider/<str:type_journal>/', views.valider_journal, name='valider-journal'),
    path('afficher_compte/', views.afficher_compte, name='afficher-compte'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
