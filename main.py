from settings import logging
from categories import Category
from products import Product

data_to_extract = None
url = None

while data_to_extract is None and url is None:
    data_to_extract = int(input("Que voulez-vous extraire sur Books to Scrape ?\n1. Les données d'un livre\n2. Les données de tous les livres d'une catégorie\n"))
    
    if data_to_extract == 1 or data_to_extract == 2:
        complement = "du livre" if data_to_extract == 1 else "de la catégorie"
        
        while url is None:
            url = input(f"Copiez l'url de la page {complement} de votre choix et appuyez sur entrée: ")
            # Ajout de https si non présent dans l'url
            if "https:" not in url.split("/")[0]:
                url = "https://" + url
            # Vérifier que l'url est bien celle de Books to Scrape
            if "books.toscrape.com" not in url:
                print("Cette URL n'appartient pas à Books to Scrape. Recommencez!")
                url = None
            # Si Catégorie a été choisi, vérifier que l'url pointe bien vers une catégorie
            elif data_to_extract == 2 and "https://books.toscrape.com/catalogue/category/books/" not in url:
                print("L'URL de la catégorie n'est pas correcte. Recommencez !")
                url = None
    else:
        print("Vous n'avez pas entré un choix correct. Recommencez !")
        data_to_extract = None

# Extrait et enregistre les données d'un seul produit
if data_to_extract == 1:
    print("Extraction des données en cours ...")
    product = Product(url)  # Création d'une instance de la classe Produit à partir de l'url fournie par l'utilisateur
    # Enregistre les données du produit dans un fichier CSV si les données ont bien été extraites
    if product.data_list:
        product.add_to_csv()

# Extrait et enregistre les données de tous les produits d'une catégorie
elif data_to_extract == 2:
    print("Extraction des données en cours ...")
    category = Category(url)  # Création d'une instance de la classe Category à partir de l'url fournie par l'utilisateur
    # Enregistre les données de tous les produits dans un fichier CSV si les livres ont bien été trouvés
    if category.books is not None:
        category.add_books_to_csv()