import sys
import os
import requests
import csv
from bs4 import BeautifulSoup
from packages.extract import *

def get_data_list(url, soup):
    """Récupération des données du produit

    Args:
        url (string): Url de la page du produit
        soup (BeautifulSoup): Classe BeautifulSoup (Html Parser)

    Returns:
        List: Retourne une liste contenant les données du produit
    """
    # Extraction du titre du produit
    title = extract_title(soup)
    print(f"Extraction des données du livre {title}")

    # Extraction de l'url de l'image du produit
    image_url = extract_image_url(soup, title)

    # Extraction de la catégorie du produit
    category = extract_category(soup)

    # Extraction de la note du produit
    rating = extract_rating(soup)

    # Extraction de la description du produit
    description = extract_description(soup)

    # Extraction des informations sur le produit (UPC, Type du produit, Prix avec et sans taxe, Stock)
    product_informations = extract_informations(soup)

    upc = product_informations["UPC"]
    price_including_tax = product_informations["Price (incl. tax)"]
    price_excluding_tax = product_informations["Price (excl. tax)"]
    number_available = product_informations["Availability"]

    # Regroupement des données du produit
    data_list = [url, upc, title, price_including_tax, price_excluding_tax, number_available, description, category, rating, image_url]
    return data_list

def load_upcs(file):
    """Chargement de tous les UPC (Qui sont uniques pour chaque produit)

    Args:
        file (csv_file): Fichier [data.csv]

    Returns:
        set: Set de tous les UPC précent dans le fichier csv
    """
    upcs = set()
    if os.path.isfile(file):
        with open(file, "r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                upcs.add(row["universal_ product_code (upc)"])
    return upcs

def create_csv(datas):
    """Ajoute les données d'un produit dans un fichier CSV (data.csv).

    Args:
        datas (List): Liste des données du produit à intégrer au CSV.
    """
    print("Création du fichier data.csv ...")
    # Fichier
    file = "data.csv"
    # En-tête
    header = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", 
            "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
            "image_url"
            ]
    
    # Vérifier si le fichier existe
    if os.path.exists(file):
        upcs = load_upcs(file)  # Chargement des UPC depuis le fichier
        # Vérifier si l'UPC du produit est déjà présent
        if datas[1] in upcs:
            print("Ce produit est déjà présent dans le fichier [data.csv].")
            return # Arrêter la fonction si le produit existe déjà
    else:
        # Si data.csv n'existe pas, création du fichier avec l'en-tête
        with open(file, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(header)  # Écrire l'en-tête si le fichier n'existe pas

    # Ajouter les données du produit au fichier
    with open(file, "a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(datas)  # Écrire les données du produit

    print("Le produit a été ajouté au fichier data.csv.")

# URL de la page produit
product_url = "https://books.toscrape.com/catalogue/it_330/index.html"



try:
    # Requête HTTP pour récupérer le contenu de la page
    page = requests.get(product_url)
    page.raise_for_status()  # Cela déclenchera une erreur si le statut HTTP est différent de 200
except requests.exceptions.RequestException as e:
    print(f"Une erreur a été détecté pendant la requête HTTP!/n{e}")
    print("Le programme va s'arrêter.")
    sys.exit(0)

# Parser la page
soup = BeautifulSoup(page.content, "html.parser")

# Récupération des données
data_list = get_data_list(product_url, soup)

# Création du fichier data.csv et écriture des données
create_csv(data_list)