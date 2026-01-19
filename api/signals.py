from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Entreprise, Journal, CompteComptable, DEFAULT_JOURNAL_TYPES


@receiver(post_save, sender=Entreprise)
def creer_journaux(sender, instance, created, **kwargs):
    if not created:
        return

    for type_journal, code, libelle in DEFAULT_JOURNAL_TYPES:
        Journal.objects.create(
            entreprise=instance,
            type=type_journal,
            code=code,
            libelle=libelle
        )


@receiver(post_save, sender=CompteComptable)
def parametrer_journaux_automatiquement(sender, instance, created, **kwargs):
    entreprise = instance.entreprise

    # On tente de récupérer les comptes nécessaires
    try:
        tva_achats = CompteComptable.objects.get(numero="445660", entreprise=entreprise)
        tva_ventes = CompteComptable.objects.get(numero="445700", entreprise=entreprise)
        charges = CompteComptable.objects.get(numero="606100", entreprise=entreprise)
        produits = CompteComptable.objects.get(numero="706000", entreprise=entreprise)
    except CompteComptable.DoesNotExist:
        # Le PGC n'est pas encore complet → on attend
        return

    # Si on arrive ici, tous les comptes existent → paramétrage automatique
    for journal in entreprise.journaux.all():

        if journal.type == "achats":
            journal.compte_tva = tva_achats
            journal.compte_ventilation = charges
            journal.sens = "achats"

        elif journal.type == "ventes":
            journal.compte_tva = tva_ventes
            journal.compte_ventilation = produits
            journal.sens = "ventes"

        elif journal.type == "banque":
            journal.sens = "banque"

        elif journal.type == "caisse":
            journal.sens = "caisse"

        else:
            journal.sens = "od"

        journal.save()

"""
@receiver(post_save, sender=Entreprise)
def creer_et_parametrer_journaux(sender, instance, created, **kwargs):
    if not created:
        return

    # 1) Création des journaux (comme avant)
    for type_journal, code, libelle in DEFAULT_JOURNAL_TYPES:
        Journal.objects.create(
            entreprise=instance,
            type=type_journal,
            code=code,
            libelle=libelle
        )

    # 2) Tentative de récupération des comptes standards
    try:
        compte_tva_achats = CompteComptable.objects.get(numero="445660", entreprise=instance)
        compte_tva_ventes = CompteComptable.objects.get(numero="445700", entreprise=instance)
        compte_charges = CompteComptable.objects.get(numero="606100", entreprise=instance)
        compte_produits = CompteComptable.objects.get(numero="707000", entreprise=instance)
    except CompteComptable.DoesNotExist:
        # Le PGC n'est pas encore créé → on ne paramètre rien
        return

    # 3) Paramétrage automatique des journaux
    for journal in instance.journaux.all():

        if journal.type == "achats":
            journal.sens = "achats"
            journal.compte_tva = compte_tva_achats
            journal.compte_ventilation = compte_charges

        elif journal.type == "ventes":
            journal.sens = "ventes"
            journal.compte_tva = compte_tva_ventes
            journal.compte_ventilation = compte_produits

        elif journal.type == "banque":
            journal.sens = "banque"

        elif journal.type == "caisse":
            journal.sens = "caisse"

        else:
            journal.sens = "od"

        journal.save()
"""
