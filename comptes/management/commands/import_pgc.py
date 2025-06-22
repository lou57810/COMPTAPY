# comptes/management/commands/import_pgc.py

import pandas as pd
from django.core.management.base import BaseCommand
from comptes.models import CompteComptable

class Command(BaseCommand):
    help = "Importe le plan comptable général (PGC) depuis un fichier Excel"

    def add_arguments(self, parser):
        # parser.add_argument('fichier', type=str, help="Chemin du fichier Excel (ex: data/pgc.xlsx)")
        parser.add_argument('fichier', type=str, help="data/pgc.xlsx)")

    def handle(self, *args, **options):
        fichier = options['fichier']

        try:
            df = pd.read_excel(fichier, header=None)
            df.columns = ['numero', 'libelle']
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erreur lors de la lecture du fichier Excel : {e}"))
            return

        nb_importés = 0
        for index, row in df.iterrows():
            numero = str(row['numero']).strip()
            libelle = str(row['libelle']).strip()

            if not numero or not libelle or not numero.isdigit():
                continue  # Ignore les lignes vides ou invalides

            compte, created = CompteComptable.objects.get_or_create(
                numero=numero,
                defaults={
                    'nom': libelle,
                    'origine': 'pgc',
                    'type_compte': self.infer_type(numero)
                }
            )
            if created:
                nb_importés += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {nb_importés} comptes importés depuis {fichier}"))

    def infer_type(self, numero):
        if numero.startswith('1'):
            return 'classe1'
        elif numero.startswith('2'):
            return 'classe2'
        elif numero.startswith('3'):
            return 'classe3'
        elif numero.startswith('4'):
            return 'classe4'
        elif numero.startswith('5'):
            return 'classe5'
        elif numero.startswith('6'):
            return 'classe6'
        elif numero.startswith('7'):
            return 'classe7'
        return 'perso'
