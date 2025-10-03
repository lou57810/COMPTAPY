@echo off
echo ===========================================
echo   Lancement du projet Django
echo ===========================================

:: Vérifier si le dossier venv existe
if not exist venv (
    echo Creation de l'environnement virtuel...
    python -m venv venv
)

:: Activer l'environnement virtuel
call venv\Scripts\activate

:: Mettre à jour pip et installer les dependances
echo Installation des dependances...
pip install --upgrade pip
pip install -r requirements.txt

:: Lancer le serveur Django
echo ===========================================
echo   Serveur en cours de lancement sur
echo   http://127.0.0.1:8000/
echo ===========================================
python manage.py runserver

:: Garder la fenêtre ouverte après l'arrêt du serveur
pause
