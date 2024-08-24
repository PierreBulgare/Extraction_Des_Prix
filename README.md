# Extraction des prix (Books to Scrape)

## Informations sur la version
**Version** : 0.4.0  
**Date** : 24/08/2024  
**Auteur** : Pierre BULGARE

## Description
Ce programme a pour objectif d'automatiser l'extraction des données et images de livres disponibles sur le site [Books To Scrape](https://books.toscrape.com) et de les enregistrer dans des fichiers CSV. Le programme permet d'extraire les données d'un livre, des livres d'une catégorie prédéfinie ou des livres de toutes les catégories.

## Prérequis
- **Python 3.7 ou une version supérieure** : [Téléchargements](https://www.python.org/downloads/).

_Si Python est déjà installé sur votre système, vous pouvez vérifier la version en tapant dans votre terminal : `python --version` pour Windows et `python3 --version` pour Mac OS/Linux._
- **Packages requis :**
  * `requests` 2.32.3 - Pour effectuer des requêtes HTTP.
  * `beautifulsoup4` 4.12.3 - Pour l'analyse et l'extraction des données HTML.

## Mode d'emploi
### Installation de l'environnement Python virtuel
Pour utiliser le programme, vous devez d'abord installer un environnement Python et installer les prérequis :

**Windows**
- Lancez le fichier `launch.bat`

**Mac OS/Linux**
- Lancez le fichier `launch.sh`

Ce fichier vérifiera si Python et Pip sont installés sur votre système, puis créera un environnement virtuel s'il n'existe pas déjà. Ensuite, il s'assurera que les packages requis sont installés dans cet environnement et les installera automatiquement si nécessaire. Enfin, il exécutera le script `main.py`. ***

### Exécution du programme
Vous aurez le choix entre trois options :
1. Extraire et enregistrer les données d'un livre
2. Extraire et enregistrer les données des livres d'une catégorie
3. Extraire et enregistrer les données des livres de toutes les catégories

Le programme créera les fichiers CSV dans les répertoires `/Donnees/Par_Livre/(Date de l'extraction)/` pour les données d'un seul livre ou `/Donnees/Par_Categorie/(Date de l'extraction)/` pour les données des livres par catégorie.

### Chargement des données dans Excel
Pour charger les données d'un fichier CSV :
1. Ouvrez un nouveau fichier Excel.
2. Cliquez sur l'onglet "Données", puis "À partir d'un fichier texte/csv".
3. Vérifiez que les données s'affichent sous forme de tableau, puis cliquez sur "Charger".

### Données d'un livre extraites par le programme
- L'URL du produit
- Le numéro UPC
- Le titre du livre
- Le prix avec et sans taxe
- La quantité disponible
- La description du produit
- La catégorie du produit
- La note du produit
- L'URL de l'image du livre

## Contacts
Si vous avez le moindre doute ou si vous rencontrez une erreur lors de l'exécution du programme, n'hésitez pas à me contacter.

---

*** Si vous ne pouvez pas utiliser les fichiers de lancement `launch.bat` ou `launch.sh`, vous pouvez installer manuellement l'environnement Python et les prérequis en exécutant les commandes suivantes dans votre terminal :

_Vérifiez que vous êtes bien dans le répertoire où se trouvent `requirements.txt` et `main.py` avant de lancer les commandes ci-dessous._

**Windows**
1. Créez l'environnement virtuel : `python -m venv venv`
2. Activez l'environnement : `venv\Scripts\activate`
3. Installez les prérequis : `pip install -r requirements.txt`
4. Exécutez le programme : `python main.py`

**Mac OS/Linux**
1. Créez l'environnement virtuel : `python3 -m venv venv`
2. Activez l'environnement : `source venv/bin/activate`
3. Installez les prérequis : `pip3 install -r requirements.txt`
4. Exécutez le programme : `python3 main.py`
