import csv
from settings import logging, os

class FileCreator:
    # Fichier
    FILE = "data.csv"
    # En-tête
    HEADER = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", 
            "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
            "image_url"
            ]

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
        """Crée un fichier data.csv s'il n'existe pas
        """
        # Vérifier si le fichier existe
        if not os.path.exists(FileCreator.FILE):
            # Si data.csv n'existe pas, création du fichier avec l'en-tête
            with open(FileCreator.FILE, "w", encoding="utf-8", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(FileCreator.HEADER)  # Écrire l'en-tête si le fichier n'existe pas
                return
            
        # Si le fichier n'existe pas
        logging.warning("Le fichier data.csv existe déjà !")

    @staticmethod
    def update_csv(product_datas):
        """Ajoute les données d'un produit dans un fichier CSV (data.csv).

        Args:
            datas (List): Liste des données du produit à intégrer au CSV.
        """
        book_title = product_datas[2]
        # Vérifier si le fichier existe
        if os.path.exists(FileCreator.FILE):
            upcs = FileCreator.load_upcs()  # Chargement des UPC depuis le fichier
            # Vérifier si l'UPC du produit est déjà présent
            if product_datas[1] in upcs:
                logging.warning(f"Le livre {book_title} est déjà présent dans le fichier data.csv.")
                return # Arrêter la fonction si le produit existe déjà
        else:
            # Si data.csv n'existe pas, création du fichier avec l'en-tête
            FileCreator.create_csv()

        # Ajouter les données du produit au fichier
        with open(FileCreator.FILE, "a", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(product_datas)  # Écrire les données du produit

        logging.info(f"Le livre {book_title} a été ajouté au fichier data.csv.")
        print(f"Enregistrement des données du livre {book_title} réussi !")