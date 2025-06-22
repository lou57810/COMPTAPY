from django.urls import include, path
from rest_framework import routers
import authentication.views

from django.conf import settings
from django.conf.urls.static import static


from  . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', authentication.views.LoginPage.as_view(), name='login'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('signup', authentication.views.signup_page, name='signup'),
    path('profile-photo/upload_profile_photo/', authentication.views.upload_profile_photo, name='upload_profile_photo')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

