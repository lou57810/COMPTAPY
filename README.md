## COMPTAPY (EN CONSTRUCTION Mode production)

---

#### *Essai Application de comptabilité personnalisée basée sur Django et PostgreSQL, conçue pour gérer plusieurs entreprises (dossiers comptables).*

---
### 🚀 Fonctionnalités principales

- Création d’une entreprise (nom, SIRET, APE, adresse, date de création).
- Création automatique d’un administrateur (is_owner) au moment de la configuration.
- Gestion des utilisateurs avec rôles (gérant, comptable, commercial, DRH, etc.).
- Plan Comptable Général (PGC) préchargé en base de données.
- Journaux comptables (achats, ventes, opérations diverses, etc.).
- Accès sécurisé via authentification.
---
### 📦 Installation locale
1. Cloner le dépôt  
``git clone https://github.com/ton-compte/comptapy.git``  
``cd comptapy``

2. Créer et configurer l’environnement
Créer un fichier .env.local à la racine :  
``DEBUG=True``  
``SECRET_KEY=une_cle_django_ultra_secrete``  
``DB_NAME=db_compta``  
``DB_USER=postgres``  
``DB_PASSWORD=motdepasse``  
``DB_HOST=127.0.0.1``  
``DB_PORT=5432``
3. Construire et lancer avec Docker  
``docker-compose down -v``  
``docker-compose up --build``  
⚠️ La première fois, il faudra appliquer les migrations et charger le PGC :  
``docker exec -it django_app python manage.py migrate``  
``docker exec -it django_app python manage.py loaddata api/fixtures/pgc.json``
---
### 🏗️ Création d’une entreprise
La première fois que vous lancez l’application :
1. Connectez-vous sur ``http://127.0.0.1:8000/setup/``
2. Remplissez :
- Nom de l’entreprise
- SIRET
- APE
- Adresse
- Date de création
- Email administrateur
- Mot de passe administrateur
3. L’entreprise est créée et l’utilisateur défini devient automatiquement owner (is_owner=True) avec tous les droits.

Une fois cette étape terminée, l’écran de login vous permet d’accéder à l’application.

### 👥 Gestion des utilisateurs et rôles  
Le propriétaire (owner) peut créer de nouveaux utilisateurs et leur attribuer un rôle :  
- OWNER : droits complets (équivalent administrateur de l’entreprise).
- GERANT : gestion juridique et globale.
- COMPTABLE : accès aux journaux comptables et au PGC.
- COMMERCIAL : accès aux données de vente.
- DRH : accès à la gestion des salaires.  

Les permissions sont centralisées dans authentication/permissions.py pour un contrôle fin de l’accès.

### 🌍 Déploiement sur Render
1. Ajouter les variables d’environnement
Dans ``.env.render :``
``DATABASE_URL=postgresql://user:password@host:5432/db_name``
``SECRET_KEY=une_cle_secrete``  
``DEBUG=False``

2. Construire et pousser l’image Docker  
``./deployDocker.sh``
