# -*- coding: utf-8 -*

from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from authentication.views import signup_page
# from .views import ajouter_entreprise
# from api.utils import create_user_and_entreprise

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('start_app', views.start_app, name='start-app'),
    # path('signup/', signup_page, name='signup'),
    # path("entreprises/ajouter", ajouter_entreprise, name="ajouter-entreprise"),
    path("entreprises/ajouter", views.setup, name="ajouter-entreprise"),
    # path("setup/expert/", views.setup, name="setup-expert"),
    # path("pgc/", views.liste_compte, name="pgc"),
    path("update_compte/", views.update_compte, name="update_compte"),
    # path('create/<int:entreprise_id>/', views.create_compte, name='create-compte'),
    path('frontend/list/', views.display_compte, name='display_compte'),  # Affiche un compte depuis son numero
    path('saisie_journal/', views.saisie_journal, name='saisie-journal'),
    path('valider/<str:type_journal>/', views.valider_journal, name='valider-journal'),
    path('frontend/afficher_compte/', views.afficher_compte, name='afficher-compte'),
    path('frontend/export_compta/', views.export_fec, name='export-fec'),
    path("frontend/manage_users/", views.manage_users, name="manage-users"),
    path("frontend/liste_entreprises/", views.liste_entreprises, name="liste-entreprises"),

    # path("compta/<int:entreprise_id>/", views.accueil_dossier_compta, name="accueil-compta"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
