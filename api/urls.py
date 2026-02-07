from django.urls import path, include
from rest_framework.generics import CreateAPIView

from . import views
# from frontend.views import accueil_dossier_compta
from rest_framework import routers
from django.contrib.auth import get_user_model
from .views import (CompteComptableRetrieveUpdateDestroy, CompteComptableListView, get_ecritures_par_compte,
                    ecritures_par_compte, compte_par_numero,   #  creer_dossier_gerant,
                    afficher_modifier_dossier, supprimer_entreprise, update_compte, auto_create_compte, liste_comptes
                     )  # creer_dossier_owner,liste_compte,
from authentication.views import UserViewSet

User = get_user_model()

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("comptes/<int:entreprise_id>/numero/", compte_par_numero, name="compte-par-numero"),
    path("comptes/", CompteComptableListView.as_view(), name="comptes"), # affiche l'api pgc
    path("comptes/<int:pk>/", CompteComptableRetrieveUpdateDestroy.as_view(), name="update"),
    path('comptes/numero/', get_ecritures_par_compte, name='get_ecritures_par_compte'),
    path("modifier_compte/<int:entreprise_id>/<int:compte_id>/", update_compte, name="update-compte"),
    path('ecritures/', ecritures_par_compte, name='ecritures_par_compte'),
    path('api/comptes/<int:entreprise_id>/auto-create/', auto_create_compte),
    path('afficher_modifier_dossier/<int:entreprise_id>', afficher_modifier_dossier, name='afficher-modifier-dossier'),
    path("entreprise/<int:entreprise_id>/supprimer/", supprimer_entreprise, name="supprimer-entreprise"),
    path("pgc/", liste_comptes, name="pgc"),
    path("liste_entreprises/", views.liste_entreprises, name="liste-entreprises"),
    # path("api/setup/", CreateEntrepriseAPIView.as_view(), name="setup-owner"),
    # path('comptes/numero/', views.get_compte_by_numero, name='get_compte_by_numero'),
    # path("journal/<int:entreprise_id>/", journal_ecritures, name="journal-ecritures"),
    # path("modifier_compte/<int:entreprise_id>/<int:compte_id>/", update_compte, name="update-compte"),
    # path('saisie_journal/<int:entreprise_id>/', views.saisie_journal, name='saisie-journal'),
    # path("ajouter_dossier/<int:gerant_id>", creer_dossier_gerant, name="creer-dossier"),
    # path("ajouter_dossier_owner/<int:gerant_id>", creer_dossier_owner, name="creer-dossier-owner"),
    # path("compta/<int:entreprise_id>/", accueil_dossier_compta, name="accueil-compta"),
    ]
