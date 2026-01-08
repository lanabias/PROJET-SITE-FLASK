1) Taper à la racine de votre dossier d'application la commande : git clone https://github.com/lanabias/PROJET-SITE-FLASK.git
2) La commande créé le dossier d'application
3) Assurez-vous que python est bien installé en regardant la version : python3 --version, la version doit être à 3.12.3. Si python3 n'est pas reconnu, installez-le :
Pour installer-python-3

    Lancez un terminal (allez dans le menu Applications, puis tapez Terminal, et cliquez sur l’icone)
   
    Dans le terminal, tapez sudo apt update pour voir si des mises à jour sont disponibles
   
    Dans le terminal, tapez sudo apt upgrade
   
    Dans le terminal, tapez : sudo apt-get install python3
   
    Entrez votre mot de passe, puis tapez Y pour lancer l’installation (NdT : ou sudo apt-get -y install python3 pour éviter de taper Y à chaque fois). Notez qu’il est fort probable que Python soit déjà installé (NdT: la commande dpkg -l python3 permet de savoir si Python 3 est déjà installé).
   
    Il pourrait être interessant d'installer vim s'il n'est pas en place. Pour cela, exécuter sudo apt install vim
   
4 ) Installer les modules pip et virtualenv : exécuter sudo apt install python3-pip et sudo apt install virtualenv

5) Entrer dans le répertoire de l'application
   
7) Vous notez l'existence d'un répertoire documentation qui contient les explications du contexte du projet et le modèle de la base de données. Ce répertoire n'est pas utilisé par l'application.
   
9) Création de l'environnement virtuel : exécuter la commande virtualenv env -p python3
    
11) Le fichier de la base de données en .sqlite se trouve à la racine de l'application, au même niveau que le fichier run.py : ne pas le modifier.
    
13) Créer le ficheir .env à côté du fichier run.py en faisant touch .env au niveau de la racine de l'application. Insérer dans ce fichier les variables décrites dans le fichier README ci-dessous.
    
6) Activer l'environnement virtuel en exécutant source env/bin/activate
   
8) Charger tous les modules compris dans le fichier requirements.txT en exécutant pip install -r requirements.txt
   
7) Lancer python3 run.py
   
9) Dans le navigateur, exécuter l'url 127.0.0.1:5000


Description des variables à entrer dans le fichier .env : 

DEBUG=TRUE

SQLALCHEMY_DATABASE_URI=sqlite:////chemin_absolu_vers_racine_application_meme_niveau_fichier_app/noblesse.sqlite

PER_PAGE=15

WTF_CSRF_ENABLE=TRUE

SECRET_KEY à définir






