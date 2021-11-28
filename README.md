# Projet9: Développez une application Web en utilisant Django

Le projet9: C'est une application contruite avec Django et SQLite, 

## Les fonctionalités principales attendues:

- Demander des critiques de livres ou d’articles, en créant un ticket
- Publier des critiques de livres ou d’articles
 
Pour des informations complèmentaires, consultez les fichiers 
 
- LITReview - Wireframes - FR.pd
- LITReview - cahier des charges.pdf

## Installation

### Récupérer les sources du projet  

Tapez les commandes suivantes: 

`$ git clone https://github.com/ML-coder-60/projet9.git`

`$ cd  projet9`

### Installation/initialisation de l'envirronnemt virtuel
 
Lancez les commandes suivantes:  

`$ virtualenv venv -p python3`

`$ source venv/bin/activate`


### Installation de Django 

Tappez les commandes suivantes:

`(venv) $ pip install --upgrade pip`

`(venv) $ pip install -r requirements.txt`

`(venv) $ python -m django --version`


### Executer Django 

Lancez la commande suivante: 

`(venv)  python manage.py runserver`

L'application est accessible depuis url http://127.0.0.1:8000/.

Depuis la page d'accueil un utilisateur peut 

1. S'enregister/se connecter
2. L'authentification est obligatoire pour accèder aux fonctionalités du programme 


## Rapport Flake8 du projet au format Html 

Un rapport de conformité est disponible dans le répertoire "flake8_report".
Pour visualiser le rapport ouvrir le fichier index.html situé dans ce répertoire.

