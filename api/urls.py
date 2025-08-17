from django.urls import path, include
from . import views
from rest_framework import routers
from django.contrib.auth import get_user_model
from .views import (CompteComptableRetrieveUpdateDestroy, CompteComptableListView, get_ecritures_par_compte,
                    ecritures_par_compte)
from authentication.views import UserViewSet

User = get_user_model()

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('comptes/numero/', views.get_compte_by_numero, name='get_compte_by_numero'),
    path("comptes/", CompteComptableListView.as_view(), name="compte_list"),
    path("comptes/<int:pk>/", CompteComptableRetrieveUpdateDestroy.as_view(), name="update"),
    path('comptes/numero/', get_ecritures_par_compte, name='get_ecritures_par_compte'),
    path('ecritures/', ecritures_par_compte, name='ecritures_par_compte'),
    ]
