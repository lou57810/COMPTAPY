# api/utils.py

from django.db import transaction
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .models import Entreprise, CompteComptable, CompteComptableReference

User = get_user_model()


def importer_pgc_pour_entreprise(entreprise):
    # Crée une copie du PGC de référence pour une entreprise donnée.
    references = CompteComptableReference.objects.all()
    comptes = [
        CompteComptable(
            entreprise=entreprise,
            numero=ref.numero,
            libelle=ref.libelle,
            type_compte=ref.type_compte,
            origine='pgc',
        )
        for ref in references
    ]
    CompteComptable.objects.bulk_create(comptes)
    print(f"✅ {len(comptes)} comptes importés pour {entreprise.nom}")
"""
def importer_pgc_pour_entreprise(entreprise):
    # Importe le plan comptable général (pgc.json) pour une entreprise donnée.
    with open("pgc.json", encoding="utf-8") as f:
        data = json.load(f)

    comptes = []
    for entry in data:
        fields = entry["fields"]
        comptes.append(
            CompteComptable(
                numero=fields["numero"],
                nom=fields["nom"],
                origine=fields.get("origine", "pgc"),
                type_compte=fields.get("type_compte", ""),
                entreprise=entreprise,
            )
        )

    CompteComptable.objects.bulk_create(comptes)
    print(f"✅ {len(comptes)} comptes importés pour {entreprise.nom}")
"""

def get_accessible_entreprises(user):
    """
    Retourne un queryset d'entreprises que l'utilisateur peut voir.
    """
    if user.role == "OWNER":
        return Entreprise.objects.all()
    if user.entreprise:
        return Entreprise.objects.filter(pk=user.entreprise.pk)
    return Entreprise.objects.none()


@transaction.atomic
def create_user_and_entreprise(email, password, role, nom=None, siret=None, ape=None, adresse=None, date_creation=None, owner=None):
    """
    Crée un utilisateur et une entreprise.
    - Si role == 'OWNER' → le propriétaire du logiciel
    - Si role == 'GERANT' → gérant d’une entreprise (lié au propriétaire)
    """

    print("➡️ Création de l’utilisateur et de l’entreprise :", email, role)

    user = User.objects.create_user(
        email=email,
        password=password,
        role=role,
    )
    # Création de l’entreprise
    entreprise = Entreprise.objects.create(
        nom=nom,
        siret=siret,
        ape=ape,
        adresse=adresse,
        date_creation=date_creation,
    )
    # 🔹 Cas 1 : création du propriétaire (comptable)
    if role == "OWNER":
        entreprise.owner = user
        entreprise.save(update_fields=["owner"])
        print(f"👤 Propriétaire créé : {user.email}")

    # 🔹 Cas 2 : création d’un gérant par le propriétaire
    elif role == "GERANT":
        entreprise.gerant = user
        if owner:
            entreprise.owner = owner  # rattachement au propriétaire
        entreprise.save(update_fields=["owner", "gerant"])
        print(f"👔 Gérant créé : {user.email}")

    # 3️⃣ Import du plan comptable de référence
    references = CompteComptableReference.objects.all()
    comptes = [
        CompteComptable(
            entreprise=entreprise,
            numero=ref.numero,
            libelle=ref.libelle,
            type_compte=ref.type_compte,
            origine='pgc',
        )
        for ref in references
    ]
    CompteComptable.objects.bulk_create(comptes)
    print(f"🏢 Entreprise '{entreprise.nom}' créée avec succès.")
    print(f"✅ PGC importé pour {entreprise.nom} ({len(comptes)} comptes).")

    return user, entreprise

