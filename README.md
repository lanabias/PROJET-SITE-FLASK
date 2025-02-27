Le fichier .env doit contenir les paramètres suivants :

DEBUG=TRUE

SQLALCHEMY_DATABASE_URI=sqlite:////home/escriptorium/Documents/projet_python/noblesse.sqlite

1) Création de l'environnement virtuel et charger tous les modules compris dans le fichier requirements.txT
2) Activer l'environnement virtuel en exécutant source env/bin/activate
3) Lancer python3 run.py
4) Dans le navigateur, exécuter l'url 127.0.0.1/all_carrieres : j'ai l'erreur :
NoForeignKeysError

sqlalchemy.exc.NoForeignKeysError: Could not determine join condition between parent/child tables on relationship CrrCarriere.Individu_source - there are no foreign keys linking these tables.  Ensure that referencing columns are associated with a ForeignKey or ForeignKeyConstraint, or specify a 'primaryjoin' expression.


