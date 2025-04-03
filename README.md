
1) Créer un dossier destiné à stocker l'application : mkdir nom_du_projet
2) Taper dans ce répertoire utilisateur la commande : git clone https://github.com/lanabias/PROJET-SITE-FLASK.git
3) Assurez-vous que python est bien installé en regardant la version : python3 --version. Si python3 n'est pas reconnu, installez-le :
Pour installer-python-3
    Lancez un terminal (allez dans le menu Applications, puis tapez Terminal, et cliquez sur l’icone)
    Dans le terminal, tapez : sudo apt-get install python3
    Entrez votre mot de passe, puis tapez Y pour lancer l’installation (NdT : ou sudo apt-get -y install python3 pour éviter d’avoir à taper Y à chaque fois). Notez qu’il est fort probable que Python soit déjà installé (NdT: la commande dpkg -l python3 permet de savoir si Python 3 est déjà installé).

4) Installer les modules pip et virtualenv : exécuter sudo apt install python3-pip et sudo apt install virtualenv

5) Création de l'environnement virtuel : exécuter la commande virtualenv env -p python3
6) INstaller la base de données en .sqlite au même niveau que le fichier run.py
7) Créer le ficheir .env à côté du fichier run.py et insérer les variables décrites dans le fichier README ci-dessous.
6) Activer l'environnement virtuel en exécutant source env/bin/activate
7) Charger tous les modules compris dans le fichier requirements.txT en exécutant pip install -r requirements.txt
7) Lancer python3 run.py
8) Dans le navigateur, exécuter l'url 127.0.0.1:5000


Description des variables à entrer dans le fichier .env : 

DEBUG=TRUE

SQLALCHEMY_DATABASE_URI=sqlite:////home/lnabias/Documents/projet_python/noblesse.sqlite

PER_PAGE=15

WTF_CSRF_ENABLE=TRUE

SECRET_KEY à définir
