# -*- coding: utf-8 -*

from . import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [

    #router.register(r'', views.accueil, basename='accueil'),
    path('', views.accueil, name='accueil'),
    path("journaux/", include("journaux.urls")),
    # path("api/comptes/", include("comptes.urls")),
    path("pgc/", views.liste_compte, name="pgc"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

