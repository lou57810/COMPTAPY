# scripts/convert_pgc_to_fixture.py
import pandas as pd
import json

INPUT = "data/PGC.xlsx"
OUTPUT = "pgc.json"

df = pd.read_excel(INPUT, header=None)
df.columns = ["numero", "libelle"]

records = []
seen_numeros = set()  # pour éviter les doublons

for _, row in df.iterrows():
    numero = str(row["numero"]).strip()
    libelle = str(row["libelle"]).strip()

    # Nettoyage : supprime les espaces multiples et caractères invisibles
    libelle = " ".join(libelle.split())

    if not numero.isdigit():
        continue

    # Ignorer les doublons
    if numero in seen_numeros:
        continue
    seen_numeros.add(numero)

    # Objet JSON compatible avec Django fixtures
    records.append({
        "model": "api.comptecomptable",  # app_label.ModelName
        "pk": int(numero),  # on peut utiliser le numéro comme PK
        "fields": {
            "numero": numero,
            "nom": libelle,
            "origine": "pgc",
            "type_compte": (
                "classe1" if numero.startswith("1") else
                "classe2" if numero.startswith("2") else
                "classe3" if numero.startswith("3") else
                "classe4" if numero.startswith("4") else
                "classe5" if numero.startswith("5") else
                "classe6" if numero.startswith("6") else
                "classe7" if numero.startswith("7") else
                "perso"
            )
        }
    })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"✅ Fixture générée : {OUTPUT}")
