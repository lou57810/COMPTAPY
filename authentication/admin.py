from django.contrib import admin

from authentication.models import User

# Register your models here.
# admin.site.register(CustomUserManager)  # TypeError: 'type' object is not iterable
admin.site.register(User)
# admin.site.register(BaseUserManager)

