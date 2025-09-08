from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Gérant / Propriétaire"
        COMPTABLE = "COMPTABLE", "Comptable"
        COMMERCIAL = "COMMERCIAL", "Commercial"
        DRH = "DRH", "Ressources Humaines"
        ADMIN = "ADMIN", "Administrateur"  # si besoin de plus de droits

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OWNER,)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False)  # vrai seulement pour le créateur
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_photo = models.ImageField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
