import csv
from settings import logging, os, re, datetime

class FileCreator:
    # Fichier
    FILE = ""
    # En-tête
    HEADER = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", 
            "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
            "image_url"
            ]
    
    @staticmethod
    def name_file(name):
        name = re.sub(r"[ ',]", "_", name)
        name = re.sub(r"[:.?!]", "", name)
        date_time = datetime.now().strftime("%d-%m-%Y_%Hh-%M-")
        FileCreator.FILE = f"{name}--BooksToScrape_datas--{date_time}.csv"

    @staticmethod
    def load_upcs():
        """Chargement de tous les UPC (Qui sont uniques pour chaque produit)

        Returns:
            set: Set de tous les UPC précent dans le fichier csv
        """
        upcs = set()
        if os.path.isfile(FileCreator.FILE):
            with open(FileCreator.FILE, "r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    upcs.add(row["universal_ product_code (upc)"])
        return upcs

    @staticmethod
    def create_csv():
        """Crée un fichier csv s'il n'existe pas
        """
        # Vérifier si le fichier existe
        if not os.path.exists(FileCreator.FILE):
            # Si le fichier csv n'existe pas, création du fichier avec l'en-tête
            with open(FileCreator.FILE, "w", encoding="utf-8", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(FileCreator.HEADER)  # Écrire l'en-tête si le fichier n'existe pas
                return
            
        # Si le fichier n'existe pas
        logging.warning(f"Le fichier {FileCreator.FILE} existe déjà !")

    @staticmethod
    def update_csv(product_datas):
        """Ajoute les données d'un produit dans un fichier CSV.

        Args:
            datas (List): Liste des données du produit à intégrer au CSV.
        """
        book_title = product_datas[2]
        # Vérifier si le fichier existe
        if os.path.exists(FileCreator.FILE):
            upcs = FileCreator.load_upcs()  # Chargement des UPC depuis le fichier
            # Vérifier si l'UPC du produit est déjà présent
            if product_datas[1] in upcs:
                logging.warning(f"Le livre {book_title} est déjà présent dans le fichier {FileCreator.FILE}")
                return # Arrêter la fonction si le produit existe déjà
        else:
            # Si le fichier csv n'existe pas, création du fichier avec l'en-tête
            FileCreator.create_csv()

        # Ajouter les données du produit au fichier
        with open(FileCreator.FILE, "a", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(product_datas)  # Écrire les données du produit

        logging.info(f"Le livre {book_title} a été ajouté au fichier {FileCreator.FILE}")
        print(f"Enregistrement des données du livre {book_title} réussi !")