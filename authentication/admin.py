from django.contrib import admin

from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
# admin.site.register(CustomUserManager)  # TypeError: 'type' object is not iterable
admin.site.register(User)
# admin.site.register(BaseUserManager)

