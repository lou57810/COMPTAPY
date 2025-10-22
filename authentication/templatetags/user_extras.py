# authentication/templatetags/user_extras.py
from django import template
from django.contrib.auth import get_user_model

User = get_user_model()

register = template.Library()

@register.simple_tag
def owner_exists():
    """Retourne True si un OWNER existe déjà dans la base"""
    exists = User.objects.filter(role="OWNER").exists()
    print("DEBUG owner_exists ->", exists)
    # return User.objects.filter(role="OWNER").exists()
    return exists
