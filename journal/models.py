from django.db import models


JOURNAL_TYPES = [
    ('1', 'Journal Achats'),
    ('2', 'Journal Ventes'),
    ('3', 'Journal OD'),
    ('4', 'Report à Nouveau'),
]


class Compte(models.Model):
    numero = models.CharField(max_length=10)
    nom = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.numero} - {self.nom}"

class Journal(models.Model):
    code = models.CharField(max_length=5)
    libelle = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=JOURNAL_TYPES)


class EcritureJournal(models.Model):
    date = models.DateField()
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    nom = models.CharField(max_length=20)
    libelle = models.CharField(max_length=255)
    quantite = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taux = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    journal = models.CharField(max_length=10)
