from django.urls import include, path
from rest_framework import routers
import authentication.views
<<<<<<< HEAD
=======
from django.conf import settings
from django.conf.urls.static import static
>>>>>>> backDev

from  . import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', authentication.views.LoginPage.as_view(), name='login'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('signup', authentication.views.signup_page, name='signup'),
    path('profile-photo/upload_profile_photo/', authentication.views.upload_profile_photo, name='upload_profile_photo')
<<<<<<< HEAD
]
=======
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> backDev
