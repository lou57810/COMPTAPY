# -*- coding: utf-8 -*

from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.accueil, name='accueil'),
    # path("journaux/", include("api.urls")),
    path("pgc/", views.liste_compte, name="pgc"),
    path("formulaire-compte/", views.ajout_modif_compte, name="compte_form"),
    path('frontend/create/', views.create_compte, name='create_compte'),
    path('frontend/list/', views.compte_num_list, name='compte_num_list'),  # Affiche un compte depuis son numero

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
    path('valider-journal-achats/', views.valider_journal_achats, name='valider_journal_achats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

