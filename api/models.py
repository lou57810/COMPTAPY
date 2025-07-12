from django.db import models
from django.utils import timezone


class ComptePgc(models.Model):
    numero = models.CharField(max_length=10, unique=True)  # Exemple : '401', '512'
    nom = models.CharField(max_length=255)  # Exemple : 'Fournisseurs', 'Banque'

    def __str__(self):
        return f"{self.numero} - {self.nom}"



class CompteComptable(models.Model):
    numero = models.CharField(max_length=10, unique=True)  # Exemple : '401', '512'
    nom = models.CharField(max_length=255)  # Exemple : 'Fournisseurs', 'Banque'
    libelle = models.CharField(max_length=255, default="N/A")   # Non attribué, à completer dans le champ.
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    date_saisie = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.numero} - {self.nom}"




JOURNAL_TYPES = [
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


class Journal(models.Model):
    code = models.CharField(max_length=5)
    libelle = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=JOURNAL_TYPES)


class EcritureJournal(models.Model):
    date = models.DateField()
    # A tester: date = models.DateTimeField(auto_now_add = True)
    compte = models.ForeignKey(CompteComptable, on_delete=models.CASCADE)  # N° compte
    nom = models.CharField(max_length=20, null=True, blank=True)
    libelle = models.CharField(max_length=255, null=True, blank=True)
    pu_ht = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantite = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taux = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    journal = models.CharField(max_length=10)

