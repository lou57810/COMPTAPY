# Étape 1 — Image de base
FROM python:3.12-slim

# Étape 2 — Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Étape 3 — Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Étape 4 — Création du répertoire de travail
WORKDIR /app

# Étape 5 — Installation des dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Étape 6 — Copie du code source
COPY . /app/

# Étape 7 — Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Étape 8 — Commande par défaut
CMD ["gunicorn", "comptapi.wsgi:application", "--bind", "0.0.0.0:8000"]
