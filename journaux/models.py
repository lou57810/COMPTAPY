from django.db import models
from comptes.models import CompteComptable

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
    libelle = models.CharField(max_length=255)
    quantite = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taux = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    journal = models.CharField(max_length=10)
