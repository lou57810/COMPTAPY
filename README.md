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
### Exécuter les migrations:
#### ``python manage.py makemigrations``
#### ``python manage.py migrate``


### Facultatif: créér un compte superutilisateur
#### Avec git bash: ``python manage.py createsuperuser``
#### ou:            ``winpty python manage.py createsuperuser``

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

### Récupération du plan comptable pour postgresql:
#### Le PGC est issu d'un fichier pgc.xlsx mais vous pouvez adapter 'import_pgc.py'
#### pour un fichier différent '***.xlsx'
#### Placer le fichier dans repertoire 'data' créé à la racine du projet.(data/***.xlsx)
#### Pour ceci modifier le fichier 'import_pgc.py'
#### import_pgc.py se trouve dans l'application: 'api/management/commands/import_pgc.py'.
#### Les dossiers 'management' et 'commands' doivent impérativement contenir les fichiers '__init__.py'.
#### Pour convertir et insérer le PGC dans la base de données lancer la commande:
#### ``python manage.py import_pgc.py data/PGC.xlsx``
#### Il est possible de vérifier si la commande est bien fonctionnelle avec la commande:
#### ``python manage.py help | findstr pgc``

#### Et enfin pour tester l'application:
#### ``python manage.py runserver``


            
