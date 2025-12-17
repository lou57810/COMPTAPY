from django.urls import path, include
from rest_framework.generics import CreateAPIView

from . import views
# from frontend.views import accueil_dossier_compta
from rest_framework import routers
from django.contrib.auth import get_user_model
from .views import (CompteComptableRetrieveUpdateDestroy, CompteComptableListView, get_ecritures_par_compte,
                    ecritures_par_compte, compte_par_numero,   #  creer_dossier_gerant,
                    afficher_modifier_dossier, supprimer_entreprise, update_compte,
                     )  # creer_dossier_owner,liste_compte,
from authentication.views import UserViewSet

User = get_user_model()

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('comptes/numero/', views.get_compte_by_numero, name='get_compte_by_numero'),
    path("comptes/<int:entreprise_id>/numero/", compte_par_numero, name="compte-par-numero"
    ),
    path("comptes/", CompteComptableListView.as_view(), name="compte_list"),

    path("comptes/<int:pk>/", CompteComptableRetrieveUpdateDestroy.as_view(), name="update"),
    path('comptes/numero/', get_ecritures_par_compte, name='get_ecritures_par_compte'),
    path("modifier_compte/<int:entreprise_id>/<int:compte_id>/", update_compte, name="update-compte"),
    path('ecritures/', ecritures_par_compte, name='ecritures_par_compte'),
    # path("ajouter_dossier/<int:gerant_id>", creer_dossier_gerant, name="creer-dossier"),
    # path("ajouter_dossier_owner/<int:gerant_id>", creer_dossier_owner, name="creer-dossier-owner"),
    path('afficher_modifier_dossier/<int:entreprise_id>', afficher_modifier_dossier, name='afficher-modifier-dossier'),
    path("entreprise/<int:entreprise_id>/supprimer/", supprimer_entreprise, name="supprimer-entreprise"),
    # path("compta/<int:entreprise_id>/", accueil_dossier_compta, name="accueil-compta"),
    # path("pgc/", liste_compte, name="pgc"),
    path("liste_entreprises/", views.liste_entreprises, name="liste-entreprises"),
    # path("api/setup/", CreateEntrepriseAPIView.as_view(), name="setup-owner"),
    ]
