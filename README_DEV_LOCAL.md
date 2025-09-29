# Essai création application comptable en mode développement.
### Pour le moment cette application est en construction et non opérationnelle.

### L'application utilise une base de donnée postgresql, le langage de programmation python ainsi que Django.
### Nécessite l'installation de python, PostgreSQL ainsi que PgAdmin, et la création d'une base de donnée avec PgAdmin (ex: ma_db).

#### Initialisation de git en local, puis copie du code version https:
#### Lancer la commande ``git clone adresse https copiée``
#### Création d'un environnement virtuel 'venv' ou nommé comme vous le souhaitez:
#### ``python  -m venv venv``
#### Puis, Win (avec console git bash): ``source venv/Scripts/activate``
####       ou Debian (terminal):   ``source venv/bin/activate``
#### Installation des dépendances modules:
#### ``pip install -r requirements.txt``


### Préparation pour un déploiement.
#### Selon le modèle 'env_template', création d'un fichier .env
#### DB_USER = 
#### DB_PASSWORD = 
#### DB_HOST = (ex: 127.0.0.1)
#### DB_PORT =  (ex: pour postgres: 5432)
#### DB_NAME = (ex: ma_db) Celle créée avec PgAdmin.
#### SECRET_KEY = (ex: dans settings.py 'django-insecure.....' crée quand le projet a été créé)
#### DATABASE_URL = "postgresql://postgres:postgres@localhost:5431/ma_db"
#### Ce fichier ne doit être accessible qu'à l'auteur du projet créé, et contient des données personnalisées.

### Exécuter les migrations:
#### ``python manage.py makemigrations``
#### ``python manage.py migrate``

### Récupération du plan comptable pour postgresql:
#### Le PGC est issu d'un fichier 'PGC.xlsx' situé dans le répertoire data.
#### En exécutant: ``python scripts/convert_pgc_to_fixture.py``
#### Nous obtenons un fichier 'pgc.json' à la base du projet.
### Si 'pgc.json' a été créé auparavant il faut le supprimer avant de lancer la commande suivante.
#### Django permet d’initialiser la base avec : ``python manage.py loaddata pgc.json``
#### Ajoutons ce fichier dans le repo (api/fixtures/pgc.json) pour qu’il soit disponible aussi sur Render.

### Facultatif: créér un compte superutilisateur
#### Avec git bash: ``python manage.py createsuperuser``
#### ou:            ``winpty python manage.py createsuperuser``

#### Et enfin pour tester l'application en local:
#### ``python manage.py runserver``


            
