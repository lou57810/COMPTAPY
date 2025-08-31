#!/bin/bash
set -e  # stoppe le script en cas d'erreur

echo "🧹 Nettoyage des anciens containers, images, volumes..."
docker-compose down -v
docker container prune -f
docker image prune -a -f
docker volume prune -f
docker builder prune -a -f

echo "📦 Build de l'image Docker..."
docker build -t lou57810/comptapy-docker-build:latest .

echo "🚀 Lancement des containers (en arrière-plan)..."
docker-compose up --build -d

echo "📤 Push de l'image sur Docker Hub..."
docker push lou57810/comptapy-docker-build:latest

echo "✅ Déploiement local terminé. Pour suivre les logs du container Django :"
echo "docker logs -f django_app"
