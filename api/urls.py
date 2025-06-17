from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from comptes.views import CompteComptableListView, CompteComptableRetrieveUpdateDestroy
User = get_user_model()


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/',UserViewSet.as_view(), name="api"),
    path("comptes/", CompteComptableListView.as_view(), name="liste-api-comptes"),
    path("comptes/<int:pk>/", CompteComptableRetrieveUpdateDestroy.as_view(), name="update"),
]
