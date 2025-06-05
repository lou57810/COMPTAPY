from django.urls import path
from comptes.views import CompteComptableListView


urlpatterns = [
    path("api/comptes/", CompteComptableListView.as_view(), name="liste-comptes"),
]
