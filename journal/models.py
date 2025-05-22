from django.db import models


class Compte(models.Model):
    numero = models.CharField(max_length=10)
    nom = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.numero} - {self.nom}"


class EcritureJournal(models.Model):
    date = models.DateField()
    libelle = models.CharField(max_length=255)
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)
    taux = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    journal = models.CharField(max_length=10)
