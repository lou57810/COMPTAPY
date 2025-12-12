from django.urls import include, path
from rest_framework import routers
import authentication.views
from authentication.views import logout_user, signup_owner, creer_gerant, upload_profile_photo

from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', authentication.views.LoginPage.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('signup', signup_owner, name='signup'),                # Dossier manager
    path('creer_gerant', creer_gerant, name='creer-gerant'),    # Dossier gérants
    path('profile-photo/upload_profile_photo/', upload_profile_photo, name='upload_profile_photo')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
