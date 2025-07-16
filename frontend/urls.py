# -*- coding: utf-8 -*

from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.accueil, name='accueil'),
    # path("journaux/", include("api.urls")),
    path("pgc/", views.liste_compte, name="pgc"),
    path("update_compte/", views.update_compte, name="update_compte"),
    path('frontend/create/', views.create_compte, name='create_compte'),
    path('frontend/list/', views.display_compte, name='display_compte'),  # Affiche un compte depuis son numero

    # path('compte/<str:numero>/ecritures/', views.ecritures_par_compte, name='ecritures-par-compte'),

    path('journal_achats/', views.journal_achats, name='journal_achats'),
    path('journal_ventes/', views.journal_ventes, name='journal_ventes'),
    path('journal_od/', views.journal_od, name='journal_od'),
    path('journal_banque/', views.journal_banque, name='journal_banque'),
    path('journal_caisse/', views.journal_caisse, name='journal_caisse'),
    path('journal_banque/', views.journal_banque, name='journal_banque'),
    path('journal_cpte_cheques_postaux/', views.journal_cpte_cheques_postaux, name='journal_cpte_cheques_postaux'),
    path('journal_effets_a_recevoir/', views.journal_effets_a_recevoir, name='journal_effets_a_recevoir'),
    path('journal_effets_a_payer/', views.journal_effets_a_payer, name='journal_effets_a_payer'),
    path('journal_report_nouveau/', views.journal_report_nouveau, name='journal_report_nouveau'),
    path('journal_cloture/', views.journal_cloture, name='journal_cloture'),
    path('journal_expert_od/', views.journal_expert_od, name='journal_expert_od'),
    path('journal_reouverture/', views.journal_reouverture, name='journal_reouverture'),
    path('journal_type/', views.journal_type, name='journal_type'),
    path('display_compte_view/', views.display_compte_view, name='display-compte-view'),
    path('valider_journal_achats/', views.valider_journal_achats, name='valider-journal-achats'),
    path('list/', views.afficher_compte, name='afficher-compte'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

