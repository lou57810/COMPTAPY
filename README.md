# Essai création application comptable.
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
#### Et enfin pour lancer l'application:
#### ``python manage.py runserver``

### Facultatif: créér un compte superutilisateur
#### Avec git bash: ``winpty python manage.py createsuperuser``

### Préparation pour un déploiement:
### Création d'un fichier .env
### Exemple (env_template):
#### DB_USER = 
#### DB_PASSWORD = 
#### DB_HOST = (ex: 127.0.0.1)
#### DB_PORT =  (ex: pour postgres: 5432)
#### DB_NAME = (ex: ma_db) Celle créée avec PgAdmin.
#### SECRET_KEY = (ex: dans settings.py 'django-insecure.....' crée quand le projet a été créé)
#### DATABASE_URL = "postgresql://postgres:postgres@localhost:5431/base_de_données"
#### Ce fichier ne doit être accessible qu'à l'auteur du projet créé, et contient des données personnalisées.

### Récupération du plan comptable pour postgresql:
#### Le PGC est issu d'un fichier pgc.xlsx mais vous pouvez adapter 'import_pgc.py'
#### pour un plan comptable différent.
#### Ici, dans comptes/management/commands: python ``import_pgc.py``


            
