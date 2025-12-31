from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Entreprise, Journal, DEFAULT_JOURNAL_TYPES

"""
@receiver(post_save, sender=Entreprise)
def creer_journaux_par_defaut(sender, instance, created, **kwargs):
    if not created:
        return

    for code, libelle in DEFAULT_JOURNAL_TYPES:
        Journal.objects.create(
            entreprise=instance,
            code=code,
            type=code,
            libelle=libelle
        )
"""


@receiver(post_save, sender=Entreprise)
def creer_journaux_par_defaut(sender, instance, created, **kwargs):
    if not created:
        return

    for type_journal, code, libelle in DEFAULT_JOURNAL_TYPES:
        Journal.objects.create(
            entreprise=instance,
            type=type_journal,
            code=code,
            libelle=libelle
        )
