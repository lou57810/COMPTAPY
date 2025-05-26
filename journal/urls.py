from rest_framework.routers import DefaultRouter
from .views import CompteViewSet, EcritureJournalViewSet


router = DefaultRouter()
router.register(r'comptes', CompteViewSet)
router.register(r'ecritures', EcritureJournalViewSet)

# urlpatterns = router.urls
from . import views
from django.urls import path



urlpatterns = [
    path('journal_type/', views.journal_type, name='journal_type'),
    path('journal_ventes/', views.journal_ventes, name='journal_ventes'),
    path('journal_achats/', views.journal_achats, name='journal_achats'),
    path('journal_od/', views.journal_od, name='journal_od'),
    path('journal_report_nouveau/', views.journal_report_nouveau, name='journal_report_nouveau'),

]