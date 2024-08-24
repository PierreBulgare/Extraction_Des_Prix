from settings import logging, display_default_error_message
from packages.extractor import Extractor
from packages.file_creator import FileCreator

class Book:
    def __init__(self, url):
        self.url = url
        self.soup = Extractor.get_html_content(url)
        self.data_list = self.get_data_list()
        # Si l'extraction des données du livre a réussi
        if self.data_list is not None:
            self.name = self.data_list[2] # Titre du livre

    def get_data_list(self)-> list|None:
        """Extrait et retourne les données du livre sous forme de liste

        Args:
            soup (BeautifulSoup): Contenu HTML du livre

        Returns:
            list: Retourne une liste contenant les données du livre (URL, UPC, Titre, Prix, Stock disponible, description, catégorie, note, URL de l'image)
        """
        # Si la requête HTTP n'a pas fonctionné
        if self.soup is None:
            return
        
        # Si la requête HTTP a fonctionné
        try:
            # Extraction du titre du livre
            title = Extractor.extract_title(self.soup)
            logging.info(f"Extraction des données du livre [{title}]")

            # Extraction de l'url de l'image du livre
            image_url = Extractor.extract_image_url(self.soup, title)
            # Télécharger l'image localement
            logging.info("Téléchargement de l'image de couverture")
            Extractor.download_image(title, image_url)

            # Extraction de la catégorie du livre
            category = Extractor.extract_category(self.soup)

            # Extraction de la note du livre
            rating = Extractor.extract_rating(self.soup)

            # Extraction de la description du livre
            description = Extractor.extract_description(self.soup)

            # Extraction des informations sur le livre (UPC, Type du livre, Prix avec et sans taxe, Stock)
            book_informations = Extractor.extract_informations(self.soup)
            upc = book_informations["UPC"]
            price_including_tax = book_informations["Price (incl. tax)"]
            price_excluding_tax = book_informations["Price (excl. tax)"]
            number_available = book_informations["Availability"]

            # Retourne les données du livre
            return [self.url, upc, title, price_including_tax, price_excluding_tax, number_available, description, category, rating, image_url]
        except Exception as e:
            logging.error(f"Erreur lors de l'extration des données du livre.\n{e}")
            display_default_error_message()
            return None
    
    def add_to_csv(self):
        """Ajoute les données du livre au fichier CSV de sa catégorie"""
        FileCreator.update_csv(self.data_list)