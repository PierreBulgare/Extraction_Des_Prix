# Extraction des prix (Books to Scrape)

## Informations sur la version
Version 0.2.1\
Date: 17/08/2024\
Auteur: Pierre BULGARE

## Description
Ce programme, dans sa version actuelle, permet d'extraire les données d'un livre ou tous les livres d'une catégorie prédéfinie sur le site [Books To Scrap](https://books.toscrape.com).\
Les données sont ensuite enregistrées dans un fichier CSV généré par le script.

## Mode d'emploi
* **Prérequis**
    - Python 3.7 ou une version supérieure [Téléchargements](https://www.python.org/downloads/).
    - Packages:
        * `beautifulsoup4` 4.12.3
        * `requests` 2.32.3
    
* **Utilisation du script**\
Pour utiliser le programme, lancez le fichier `launch.bat`. Ce fichier vérifiera les packages et les installera automatiquement si nécessaire, puis il exécutera le script `main.py`. ***\
Vous aurez le choix entre deux options:
    1. Extraire et enregistrer les données d'un livre
    2. Extraire et enregistrer les données de tous les livres d'une catégorie

* **Charge les données dans Excel**\
Pour charger les données du fichier CSV:
    * Ouvrez un nouveau fichier Excel
    * Cliquez sur l'onglet "Données", puis "À partir d'un fichier text/csv"
    * Vérifiez que les données s'affichent sous forme de tableau, puis cliquez sur "Charger"

* **Données extraites par le programme**
    * L'URL du produit
    * Le numéro UPC
    * Le titre du livre
    * Le prix avec et sans taxe
    * La quantité disponible
    * La description du produit
    * La catégorie du produit
    * La note du produit
    * L'URL de l'image du livre

## Contacts
Si vous avez le moindre doute ou rencontrez une erreur lors de l'exécution du programme, n'hésitez pas à me contacter.


---
\
\***_Si vous ne pouvez pas utiliser le fichier `launch.bat`, vous pouvez installer manuellement les prérequis en exécutant la commande suivante dans votre terminal : `pip install -r requirements.txt` puis en lançant le programme avec la commande `python main.py`.\
Vérifiez que vous êtes bien dans le répertoire où se trouve `requirements.txt` et `main.py`._