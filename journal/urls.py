from rest_framework.routers import DefaultRouter
from .views import CompteViewSet, EcritureJournalViewSet


router = DefaultRouter()
router.register(r'comptes', CompteViewSet)
router.register(r'ecritures', EcritureJournalViewSet)

urlpatterns = router.urls
from . import views
from django.urls import path



urlpatterns = [
    path('journal/', views.journal, name='journal')

]