from django.db import models

# Create your models here.

class Compte(models.Model):
    numero = models.CharField(max_length=10)
    libelle = models.CharField(max_length=255)


    # def __str__(self):
        # return f"{self.numero} - {self.libelle}"


class CreationCompte(models.Model):  # Comptes Clients ou Fournisseurs
    date = models.DateField()
    compte = models.ForeignKey(Compte, on_delete=models.CASCADE)  # N° compte
    numero = models.CharField(max_length=20)
    libelle = models.CharField(max_length=255)
