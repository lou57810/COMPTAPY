import pandas as pd
from django.core.management.base import BaseCommand
from api.models import CompteComptable
from pathlib import Path


class Command(BaseCommand):
    help = "Importe le plan comptable général (PGC) depuis un fichier Excel"

    def add_arguments(self, parser):
        parser.add_argument(
            '--fichier',
            type=str,
            default="data/PGC.xlsx",  # valeur par défaut
            help="Chemin du fichier Excel (ex: data/PGC.xlsx)"
        )

    def handle(self, *args, **options):
        fichier = options['fichier']
        fichier_path = Path(fichier)

        if not fichier_path.exists():
            self.stderr.write(self.style.ERROR(f"❌ Fichier introuvable: {fichier_path.resolve()}"))
            return

        try:
            df = pd.read_excel(fichier_path, header=None)
            df.columns = ['numero', 'libelle']
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erreur lors de la lecture du fichier Excel : {e}"))
            return

        nb_crees, nb_mis_a_jour = 0, 0
        for _, row in df.iterrows():
            numero = str(row['numero']).strip()
            libelle = str(row['libelle']).strip()

            if not numero or not libelle or not numero.isdigit():
                continue  # Ignore les lignes invalides

            compte, created = CompteComptable.objects.update_or_create(
                numero=numero,
                defaults={
                    'nom': libelle,
                    'origine': 'pgc',
                    'type_compte': self.infer_type(numero)
                }
            )
            if created:
                nb_crees += 1
            else:
                nb_mis_a_jour += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Import terminé: {nb_crees} comptes créés, {nb_mis_a_jour} mis à jour."
        ))

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
