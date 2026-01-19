from django.db import models
from django.utils import timezone

"""
DEFAULT_JOURNAL_TYPES = [
    ('1', 'Journal Achats'),
    ('2', 'Journal Ventes'),
    ('3', 'Journal OD'),
    ('4', 'Banque'),
    ('5', 'Caisse'),
    ('6', 'Compte chèques postaux'),
    ('7', 'Effets à payer'),
    ('8', 'Effets à recevoir'),
    ('9', 'Reports à Nouveau'),
    ('10', 'Journal de clôture'),
    ('11', 'Journal expert OD'),
    ('12', 'Journal de réouverture'),
    ]
"""


# Définition unique des types de journaux
DEFAULT_JOURNAL_TYPES = [
    ("achats", "AC", "Journal des achats"),
    ("ventes", "VT", "Journal des ventes"),
    ("banque", "BQ", "Journal de banque"),
    ("caisse", "CS", "Journal de caisse"),
    ("od", "OD", "Opérations diverses"),
    ("compte chèques postaux", "CCP", "Journal comptes chèques postaux"),
    ("effets a payer", "EP", "Journal effets payer"),
    ("effets a recevoir", "ER", "Journal effets recevoir"),
    ("reports a nouveau", "RE", "Journal reports nouveau"),
    ("journal de cloture", "JC", "Journal de cloture"),
    ("journal expert OD", "EOD", "Journal expert OD"),
    ("journal de reouverture", "JR", "Journal de réouverture"),
]

# Définition unique des journaux par défaut
JOURNAL_TYPES = [
    ("achats","Journal des achats"),
    ("ventes", "Journal des ventes"),
    ("banque", "Journal de banque"),
    ("caisse", "Journal de caisse"),
    ("od", "Opérations diverses"),
    ("compte chèques postaux", "Journal comptes chèques postaux"),
    ("effets a payer", "Journal effets payer"),
    ("effets a recevoir", "Journal effets recevoir"),
    ("reports a nouveau", "Journal reports nouveau"),
    ("journal de cloture", "Journal de cloture"),
    ("journal expert OD", "Journal expert OD"),
    ("journal de reouverture", "Journal de réouverture"),
]



class Entreprise(models.Model):
    owner = models.ForeignKey(
        "authentication.User",                # référence différée : évite les imports circulaires
        on_delete=models.CASCADE,             # si le propriétaire est supprimé, on supprime ses entreprises
        related_name="entreprises",           # owner.entreprises.all() => liste des entreprises gérées par le comptable
        limit_choices_to={"role": "OWNER"},   # sécurité : seuls les OWNER peuvent être propriétaires
        null=True,
        blank=True,
    )

    gerant = models.OneToOneField(
        "authentication.User",
        on_delete=models.SET_NULL,            # si le gérant est supprimé, on garde l’entreprise
        related_name="entreprise_gerant",
        null=True,
        blank=True,
        limit_choices_to={"role": "GERANT"},  # seuls les utilisateurs avec rôle GERANT peuvent être assignés
    )

    nom = models.CharField(max_length=255)
    siret = models.CharField(max_length=14, blank=True, null=True)
    ape = models.CharField(max_length=10, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    date_creation = models.DateField(blank=True, null=True)
    nom_gerant = models.CharField(max_length=255, blank=True, null=True)  # info redondante pour affichage

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} ({self.nom_gerant or 'sans gérant'})"

    @property
    def nom_contact(self):
        if self.gerant:
            return self.gerant.nom_gerant or self.gerant.get_full_name()
        return None


# Il n’y a pas 'entreprise' ici : c’est une table de référence globale.
class CompteComptableReference(models.Model):
    numero = models.CharField(max_length=20)
    libelle = models.CharField(max_length=255)
    type_compte = models.CharField(max_length=50, blank=True, null=True)
    origine = models.CharField(max_length=50, default="pgc")

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return f"{self.numero} - {self.libelle}"


# Comptes comptables réels d’une entreprise. Chaque entreprise possède sa propre copie de ces comptes,
# importée depuis CompteComptableReference à sa création.
# Ici, chaque ligne correspond à un compte propre à une entreprise.
# C’est dans cette table que sont créés les comptes personnalisés (401X, 512X, etc.).
class CompteComptable(models.Model):
    numero = models.CharField(max_length=100)  # Exemple : '401', '512'
    nom = models.CharField(max_length=255)  # Exemple : 'Fournisseurs', 'Banque'
    libelle = models.CharField(max_length=255, default="N/A")   # Non attribué, à completer dans le champ.
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_saisie = models.DateTimeField(default=timezone.now)
    # rendre entreprise facultative
    entreprise = models.ForeignKey(
        "api.Entreprise", on_delete=models.CASCADE, related_name="comptes"
    )
    type_compte = models.CharField(
        max_length=20,
        choices=[
            ('classe1', 'Comptes de capitaux'),
            ('classe2', 'Immobilisations'),
            ('classe3', 'Stocks'),
            ('classe4', 'Tiers'),
            ('classe5', 'Financiers'),
            ('classe6', 'Charges'),
            ('classe7', 'Produits'),
            ('perso', 'Personnalisé'),
        ],
        default='perso',
    )
    origine = models.CharField(max_length=20, choices=[('pgc', 'PCG'), ('user', 'Utilisateur')], default='pgc')

    class Meta:
        unique_together = ("numero", "entreprise") # Les numéros du PGC sont uniques mais à chaques entreprises)
        ordering = ["numero"]
        # D'ou, lever la contrainte d'unicité sur numero et la remplacer par une contrainte d'unicité composite (numero, entreprise)

    def __str__(self):
        return f"{self.numero} - {self.nom} ({self.entreprise.nom})"


"""
class Journal(models.Model):
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=JOURNAL_TYPES)
"""


class Journal(models.Model):
    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='journaux'
    )
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=255)
    type = models.CharField(max_length=100, choices=JOURNAL_TYPES)

    # sens débit/crédit
    sens = models.CharField(
        max_length=20,
        choices=[
            ("achats", "Achats"),
            ("ventes", "Ventes"),
            ("banque", "Banque"),
            ("caisse", "Caisse"),
            ("od", "Opérations diverses"),
        ],
        default="od",
    )

    compte_tva = models.ForeignKey(CompteComptable, on_delete=models.PROTECT, related_name="journal_tva", blank=True, null=True)
    compte_ventilation = models.ForeignKey(CompteComptable, on_delete=models.PROTECT,
                                           related_name="journal_ventilation", blank=True, null=True)
    dernier_numero_piece = models.IntegerField(default=0)

    class Meta:
        unique_together = ('entreprise', 'type')

    def __str__(self):
        return f"{self.entreprise} – {self.libelle} - {self.type} - {self.code}"


class EcritureJournal(models.Model):
    date = models.DateField()
    entreprise = models.ForeignKey('Entreprise', on_delete=models.CASCADE, related_name='ecritures')
    # A tester: date = models.DateTimeField(auto_now_add = True)
    compte = models.ForeignKey(CompteComptable, on_delete=models.CASCADE)  # N° compte
    nom = models.CharField(max_length=100, null=True, blank=True)
    numero_piece = models.CharField(max_length=50, blank=True, null=True)
    libelle = models.CharField(max_length=255, null=True, blank=True)
    pu_ht = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantite = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taux = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
