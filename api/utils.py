# api/utils.py
from .models import Entreprise
from django.db import transaction
from django.utils.timezone import now
from authentication.models import User

def get_accessible_entreprises(user):
    """
    Retourne un queryset d'entreprises que l'utilisateur peut voir.
    """
    if user.role == "EXPERT_COMPTABLE":
        return Entreprise.objects.all()
    if user.entreprise:
        return Entreprise.objects.filter(pk=user.entreprise.pk)
    return Entreprise.objects.none()


def create_user_and_entreprise(email, password, role, nom=None, siret=None, ape=None, adresse=None, date_creation=None):
    """
    Crée un utilisateur et, si nécessaire (GERANT ou EXPERT_COMPTABLE), une entreprise associée.
    Retourne (user, entreprise).
    """
    print("➡️ [create_user_and_entreprise] Début")
    with transaction.atomic():
        print("Création user…")
        # 1. Créer l’utilisateur
        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            is_owner=(role in ["GERANT", "EXPERT_COMPTABLE"]),
            is_staff=(role == "EXPERT_COMPTABLE"),
        )
        print("✅ User créé:", user.email, "role:", user.role)

        entreprise = None

        # 2. Si gérant ou expert, on crée aussi l’entreprise
        if role in ["GERANT", "EXPERT_COMPTABLE"]:
            print("Création entreprise…")
            entreprise = Entreprise.objects.create(
                nom=nom or f"Entreprise de {email}",
                siret=siret or "00000000000000",
                ape=ape or "0000Z",
                adresse=adresse or "",
                date_creation=date_creation or now().date(),
                owner=user,
            )
            print("✅ Entreprise créée:", entreprise.nom)
            user.entreprise = entreprise
            user.save(update_fields=["entreprise", "is_owner"])

        return user, entreprise

