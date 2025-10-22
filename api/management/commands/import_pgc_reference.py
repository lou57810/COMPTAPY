import json
from django.core.management.base import BaseCommand
from api.models import CompteComptableReference

class Command(BaseCommand):
    help = "Importe le plan comptable général (PGC) dans CompteComptableReference"

    def handle(self, *args, **options):
        with open("pgc.json", encoding="utf-8") as f:
            data = json.load(f)

        count = 0
        for entry in data:
            fields = entry.get("fields", {})
            numero = fields.get("numero")
            libelle = fields.get("nom") or fields.get("libelle")

            if not numero:
                continue

            obj, created = CompteComptableReference.objects.get_or_create(
                numero=numero,
                defaults={
                    "libelle": libelle or "",
                    "type_compte": fields.get("type_compte", ""),
                    "origine": fields.get("origine", "pgc"),
                },
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} comptes importés dans le PGC de référence."))
