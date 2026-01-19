# api/utils.py
from pathlib import Path
from django.db import transaction
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .models import Entreprise, CompteComptable, CompteComptableReference
from django.conf import settings
from pathlib import Path
import json
from django.core.exceptions import ObjectDoesNotExist

from authentication.models import User
# User = get_user_model()



def importer_pgc_pour_entreprise(entreprise):
    """Importe le plan comptable pour une entreprise donnée, si non déjà présent."""
    print('entreprise_importe_pgc...:', entreprise)
    if CompteComptable.objects.filter(entreprise=entreprise, origine="pgc").exists():
        print(f"ℹ️ Le PGC est déjà importé pour {entreprise}")
        return

    pgc_path = Path(settings.BASE_DIR) / "pgc.json"
    with open(pgc_path, encoding="utf-8") as f:
        data = json.load(f)

    comptes = []
    for item in data:
        fields = item["fields"]
        comptes.append(
            CompteComptable(
                entreprise=entreprise,
                numero=fields.get("numero"),
                # libelle=fields.get("nom"),
                nom=fields.get("nom"),
                type_compte=fields.get("type_compte"),
                origine="pgc",
            )
        )
    CompteComptable.objects.bulk_create(comptes)
    print(f"✅ {len(comptes)} comptes importés pour {entreprise}")



def get_accessible_entreprises(user):
    """
    Retourne un queryset d'entreprises que l'utilisateur peut voir.
    """
    if user.role == "OWNER":
        # entreprise_comptable = Entreprise.objects.filter(owner=user).first()
        # print('Entreprise', entreprise_comptable)
        return Entreprise.objects.all()
    if user.entreprise:
        return Entreprise.objects.filter(pk=user.entreprise.pk)
    return Entreprise.objects.none()


def get_owner():
    return User.objects.filter(role="OWNER").first()


def get_entreprise_from_gerant(user):
    return Entreprise.objects.filter(gerant=user).first()


def create_user_and_entreprise(
    nom_gerant, email, password, role, nom, siret, ape, adresse, date_creation):
    """Crée un gérant (utilisateur) et une entreprise liée au propriétaire unique (OWNER)."""
    try:
        owner = User.objects.get(role="OWNER")
        print('OWNER:', owner)
    except ObjectDoesNotExist:
        raise ValueError("Aucun propriétaire (OWNER) n’est défini dans la base.")

    # Vérifie si un utilisateur avec le même e-mail existe déjà
    if User.objects.filter(email=email).exists():
        raise ValueError(f"L'adresse e-mail '{email}' est déjà utilisée.")

    # Création du gérant
    user = User.objects.create_user(
        nom_gerant=nom_gerant,
        email=email,
        password=password,
        role=role or "GERANT",
    )
    print('user, owner:', user, owner)

    # Création de l’entreprise
    entreprise = Entreprise.objects.create(
        owner=owner,
        gerant=user,
        nom=nom,
        siret=siret,
        ape=ape,
        adresse=adresse,
        date_creation=date_creation,
        nom_gerant=nom_gerant,
    )
    print('entreprise:', entreprise)

    # Import du plan comptable général pour cette entreprise
    importer_pgc_pour_entreprise(entreprise)
    print(f"✅ Entreprise Fonction importer_pgc... '{entreprise.nom}' créée avec succès pour le gérant '{user.email}'.")
    return user, entreprise

"""
@transaction.atomic
def create_user_and_entreprise(
    email,
    password,
    role,
    nom=None,
    siret=None,
    ape=None,
    adresse=None,
    date_creation=None,
    owner=None,
    nom_gerant=None,
):

    # Crée un utilisateur et une entreprise associée.
    # - OWNER : crée le propriétaire principal (expert comptable)
    # - GERANT : crée un gérant pour une entreprise, liée à l'OWNER existant


    # 🧱 Cas 1️⃣ : Création du propriétaire (OWNER)
    if role == "OWNER":
        # Vérifier qu’il n’existe pas déjà un propriétaire
        if User.objects.filter(role="OWNER").exists():
            raise ValueError("Un propriétaire (OWNER) est déjà enregistré.")

        # Créer le propriétaire principal
        user = User.objects.create_user(
            email=email,
            password=password,
            role="OWNER",
            nom_gerant=nom_gerant,
        )
        user.save()

        # Créer éventuellement une entreprise de référence (facultatif)
        entreprise = Entreprise.objects.create(
            nom=nom or "Cabinet comptable",
            siret=siret or "00000000000000",
            ape=ape or "0000Z",
            adresse=adresse or "N/A",
            date_creation=date_creation,
            owner=user,  # propriétaire de son propre cabinet
            nom_gerant=nom_gerant,
        )

        print(f"👑 Propriétaire '{email}' créé avec son entreprise '{entreprise.nom}'")

        # Import du PGC une seule fois pour cette entreprise
        importer_pgc_pour_entreprise(entreprise)

        return user, entreprise

    # 🧱 Cas 2️⃣ : Création d’un gérant pour une entreprise (lié à l’OWNER)
    if owner is None:
        try:
            owner = User.objects.get(role="OWNER")
        except User.DoesNotExist:
            raise ValueError("Aucun propriétaire (OWNER) n’est défini dans la base.")

    # Créer le gérant
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "nom_gerant": nom_gerant,
            "role": "GERANT",
        },
    )

    if created:
        user.set_password(password)
        user.save()
        print(f"👤 Gérant créé : {email}")
    else:
        print(f"⚠️ Gérant déjà existant : {email}")

    # Créer son entreprise
    entreprise = Entreprise.objects.create(
        nom=nom,
        siret=siret,
        ape=ape,
        adresse=adresse,
        date_creation=date_creation,
        owner=owner,
        nom_gerant=nom_gerant,
    )

    print(f"🏢 Entreprise '{entreprise.nom}' créée avec succès (gérée par {user.email}).")

    # Importer le PGC spécifique à cette entreprise
    importer_pgc_pour_entreprise(entreprise)

    return user, entreprise
"""
