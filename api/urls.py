from django.urls import path, include
from . import views
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from .views import CompteComptableRetrieveUpdateDestroy, CompteComptableViewSet # CompteComptableListView,
from authentication.views import UserViewSet

User = get_user_model()

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'comptes', CompteComptableViewSet, basename='comptes')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('comptes/numero/', views.get_compte_by_numero, name='get_compte_by_numero'),
    path("comptes/", CompteComptableViewSet.as_view({'get': 'list'}), name="liste-api-comptes"),
    path("comptes/<int:pk>/", CompteComptableRetrieveUpdateDestroy.as_view(), name="update"),
]
