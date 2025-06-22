from django.urls import path
from comptes.views import CompteComptableRetrieveUpdateDestroy, CompteComptableViewSet

urlpatterns = [
    path("comptes/", CompteComptableViewSet.as_view({'get': 'list'}), name="liste-api-comptes"),
    path("comptes/<int:pk>/", CompteComptableRetrieveUpdateDestroy.as_view(), name="update"),
]
