#!/bin/bash
echo "==========================================="
echo "   Lancement du projet Django (Linux)"
echo "==========================================="

# Vérifier si venv existe
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour pip et installer les dépendances
echo "Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Lancer le serveur Django
echo "==========================================="
echo "   Serveur en cours de lancement sur"
echo "   http://127.0.0.1:8000/"
echo "==========================================="
python manage.py runserver
