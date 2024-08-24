import csv
import re
from datetime import datetime
from settings import logging, os

class FileCreator:
    # Variable qui va contenir le chemin du fichier CSV
    FILE = ""
    # Liste des champs de l'en-tête du fichier CSV
    HEADER = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", 
            "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
            "image_url"
            ]
    
    @staticmethod
    def create_folder(folder):
        """ Création de répertoire"""
        if not os.path.exists(folder):
            os.makedirs(folder)

    @staticmethod
    def format_name(name)-> str:
        """Supprime les caractères spéciaux et remplace les espaces, virgules et aspostrophes 
        en underscore dans le nom du fichier"""
        name = re.sub(r"[ ',/]", "_", name)
        name = re.sub(r"[*&]", "-", name)
        name = re.sub(r"[:.?!\"]", "", name)
        return name

    @staticmethod
    def name_file(name, folder):
        """Nommage des fichiers CSV"""
        date = datetime.now().strftime("%d-%m-%Y") # Date d'exécution du programme
        time = datetime.now().strftime("%H-%M") # Heure d'extraction du fichier CSV
        
        # Dossier de destination
        destination_folder = f"Donnees/Par_{folder}/{date}"

        # Création du dossier de destination s'il n'existe pas
        FileCreator.create_folder(destination_folder)

        FileCreator.FILE = f"{destination_folder}/{FileCreator.format_name(name)}--{time}.csv" # Assignation du nom final du fichier CSV à la variable FILE

    @staticmethod
    def load_upcs()-> set:
        """Charge tous les UPC (Qui sont uniques pour chaque produit)

        Returns:
            set: Set de tous les UPC précent dans le fichier CSV
        """
        upcs = set()
        if os.path.isfile(FileCreator.FILE):
            with open(FileCreator.FILE, "r", encoding="utf-8") as CSV_file:
                reader = csv.DictReader(CSV_file)
                for row in reader:
                    upcs.add(row["universal_ product_code (upc)"])
        return upcs
        
    
    @staticmethod
    def save_image(destination_folder, image_name, image_content):
        """Enregistre la couverture d'un livre localement"""
        # Création du dossier de destination s'il n'existe pas
        FileCreator.create_folder(destination_folder)
        try:
            with open(f"Donnees/Images/{image_name}", "wb") as image_file:
                image_file.write(image_content)
        except Exception as e:
            logging.error(e)

    @staticmethod
    def create_csv():
        """Crée un fichier CSV s'il n'existe pas
        """
        # Vérifie si le fichier existe
        if not os.path.exists(FileCreator.FILE):
            # Si le fichier CSV n'existe pas, création du fichier avec l'en-tête
            with open(FileCreator.FILE, "w", encoding="utf-8", newline="") as CSV_file:
                writer = csv.writer(CSV_file, delimiter=",")
                writer.writerow(FileCreator.HEADER)  # Écrire l'en-tête si le fichier n'existe pas
                return
            
        # Si le fichier n'existe pas
        logging.warning(f"Le fichier {FileCreator.FILE} existe déjà !")

    @staticmethod
    def update_csv(book_datas):
        """Ajoute les données d'un produit dans un fichier CSV.

        Args:
            datas (List): Liste des données du produit à intégrer au CSV.
        """
        book_title = book_datas[2]
        # Vérifier si le fichier existe
        if os.path.exists(FileCreator.FILE):
            upcs = FileCreator.load_upcs()  # Chargement des UPC depuis le fichier
            # Vérifier si l'UPC du produit est déjà présent
            if book_datas[1] in upcs:
                logging.warning(f"Le livre {book_title} est déjà présent dans le fichier {FileCreator.FILE}")
                return # Arrêter la fonction si le produit existe déjà
        else:
            # Si le fichier CSV n'existe pas, création du fichier avec l'en-tête
            FileCreator.create_csv()

        # Ajouter les données du produit au fichier
        with open(FileCreator.FILE, "a", encoding="utf-8", newline="") as CSV_file:
            writer = csv.writer(CSV_file, delimiter=",")
            writer.writerow(book_datas)  # Écrire les données du produit

        logging.info(f"Le livre {book_title} a été ajouté au fichier {FileCreator.FILE.replace("output/", "")}")