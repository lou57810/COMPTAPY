# -*- coding: utf-8 -*

from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (accueil_manager, accueil_gerant, accueil_dossier_compta,
                    afficher_compte, create_compte, pgc_entreprise, search_modif_compte,
                    journal_ecritures, journal_page, saisie_journal, valider_journal)  #    liste_compte_entreprise
# from .views import ajouter_entreprise
# from api.utils import create_user_and_entreprise


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path("accueil_manager/", accueil_manager, name="accueil-manager"),
    path("accueil_gerant/", accueil_gerant, name="accueil-gerant"),
    path('start_app', views.start_app, name='start-app'),
    path("pgc_entreprise/<int:entreprise_id>/", pgc_entreprise, name="pgc-entreprise"),
    path('create_compte/<int:entreprise_id>/', create_compte, name='create-compte'),
    path('display_compte/<int:entreprise_id>/', views.display_compte, name='display-compte'),  # Affiche un compte depuis son numero
    path('search_compte/<int:entreprise_id>/', search_modif_compte, name='search-modif-compte'),
    path('saisie_journal/<int:entreprise_id>/', saisie_journal, name='saisie-journal'),
    path("journal_page/<int:entreprise_id>/", journal_page, name="journal-page"),
    path("journal/<int:entreprise_id>/", journal_ecritures, name="journal-ecritures"), # --> api json
    path('valider/<str:type_journal>/', valider_journal, name='valider-journal'),
    path('frontend/afficher_compte/<int:entreprise_id>/', afficher_compte, name='afficher-compte'),
    path('frontend/export_compta/', views.export_fec, name='export-fec'),
    path("frontend/manage_users/", views.manage_users, name="manage-users"),
    path("compta/<int:entreprise_id>/", accueil_dossier_compta, name="accueil-compta"),
    # path('signup/', signup_page, name='signup'),
    # path("entreprises/ajouter", ajouter_entreprise, name="ajouter-entreprise"),
    # path("entreprises/ajouter", views.setup, name="ajouter-entreprise"),
    # path("setup/expert/", views.setup, name="setup-expert"),
    # path("pgc/", views.liste_compte, name="pgc-gerant"),
    # path("update_compte/", views.update_compte, name="update_compte"),
    # path("modifier_compte/<int:entreprise_id>/<int:compte_id>/", update_compte, name="update-compte"),
    # path("modif_compte/<int:entreprise_id>//", modif_compte, name="modif-compte"),
    # path('create/<int:entreprise_id>/', views.create_compte, name='create-compte'),


    # path("compta/<int:entreprise_id>/", views.accueil_dossier_compta, name="accueil-compta"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
