from django.urls import path
import authentication.views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('login/', authentication.views.LoginPage.as_view(), name='login'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('signup', authentication.views.signup_page, name='signup'),
    path('profile-photo/upload_profile_photo/',
         authentication.views.upload_profile_photo, name='upload_profile_photo'),
]
"""Valable uniquement en developpement, avec DEBUG=True,

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    MEDIA_URL est l'URL depuis laquelle Django va essayer de servir des medias.
    MEDIA_ROOT indique le répertoire local dans lequel seront sauvegardées les
    images téléversées.
"""
