from django.db import models



class CompteComptable(models.Model):
    numero = models.CharField(max_length=10, unique=True)  # Exemple : '401', '512'
    nom = models.CharField(max_length=255)  # Exemple : 'Fournisseurs', 'Banque'
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
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

    # def __str__(self):
        # return f"{self.numero} - {self.nom}"
