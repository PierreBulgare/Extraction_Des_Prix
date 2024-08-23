# Extraction des prix (Books to Scrape)

## Informations sur la version
**Version** : 0.3.0  
**Date** : 23/08/2024  
**Auteur** : Pierre BULGARE

## Description
Ce programme, dans sa version actuelle, permet d'extraire les données d'un livre, des livres d'une catégorie prédéfinie ou des livres de toutes les catégories du site [Books To Scrape](https://books.toscrape.com).  
Les données du livre ou de chaque catégorie sont ensuite enregistrées dans un fichier CSV généré par le script.

## Prérequis
- **Python 3.7 ou une version supérieure** : [Téléchargements](https://www.python.org/downloads/).
- **Packages requis :**
    * `beautifulsoup4` 4.12.3
    * `requests` 2.32.3

## Mode d'emploi : Exécution du script
Pour utiliser le programme, lancez le fichier `launch.bat` si vous êtes sur Windows ou le fichier `launch.sh` si vous êtes sur Mac OS/Linux. Ce fichier vérifiera si les packages requis sont installés et les installera automatiquement si nécessaire, puis il exécutera le script `main.py`.

Vous aurez le choix entre trois options :
1. Extraire et enregistrer les données d'un livre
2. Extraire et enregistrer les données des livres d'une catégorie
3. Extraire et enregistrer les données des livres de toutes les catégories

***Remarque : Assurez-vous d'exécuter les fichiers de lancement à partir du répertoire où se trouvent `main.py` et `requirements.txt`.***

Le programme créera les fichiers CSV dans le répertoire `/Donnees/Par_Livre/(Date de l'extraction)/` pour les données d'un seul livre ou dans le répertoire `/Donnees/Par_Categorie/(Date de l'extraction)/` pour les données des livres par catégories.

### Chargement des données dans Excel
Pour charger les données d'un fichier CSV :
1. Ouvrez un nouveau fichier Excel.
2. Cliquez sur l'onglet "Données", puis "À partir d'un fichier text/csv".
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

***Si vous ne pouvez pas utiliser les fichiers de lancement `launch.bat` ou `launch.sh`, vous pouvez installer manuellement les prérequis en exécutant la commande suivante dans votre terminal : `pip install -r requirements.txt` puis en lançant le programme avec la commande `python main.py`. Vérifiez que vous êtes bien dans le répertoire où se trouve `requirements.txt` et `main.py`.***