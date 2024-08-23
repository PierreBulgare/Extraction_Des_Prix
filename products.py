from settings import logging, display_default_error_message
from packages.extractor import Extractor
from packages.file_creator import FileCreator


class Product:
    def __init__(self, url):
        self.url = url
        self.soup = Extractor.get_html_content(url)
        self.data_list = self.get_data_list()
        if self.data_list is not None:
            self.name = self.data_list[2]

    def get_data_list(self):
        """Récupération des données du produit

        Args:
            soup (BeautifulSoup): Contenu HTML du Produit

        Returns:
            List: Retourne une liste contenant les données du produit (URL, UPC, Titre, Prix, Stock disponible, description, catégorie, note, URL de l'image)
        """
        # Si la requête HTTP n'a pas fonctionné
        if self.soup is None:
            return
        
        # Si la requête HTTP a fonctionné
        try:
            # Extraction du titre du produit
            title = Extractor.extract_title(self.soup)
            logging.info(f"Extraction des données du livre [{title}]")

            # Extraction de l'url de l'image du produit
            image_url = Extractor.extract_image_url(self.soup, title)

            # Extraction de la catégorie du produit
            category = Extractor.extract_category(self.soup)

            # Extraction de la note du produit
            rating = Extractor.extract_rating(self.soup)

            # Extraction de la description du produit
            description = Extractor.extract_description(self.soup)

            # Extraction des informations sur le produit (UPC, Type du produit, Prix avec et sans taxe, Stock)
            product_informations = Extractor.extract_informations(self.soup)

            upc = product_informations["UPC"]
            price_including_tax = product_informations["Price (incl. tax)"]
            price_excluding_tax = product_informations["Price (excl. tax)"]
            number_available = product_informations["Availability"]

            # Regroupement des données du produit
            data_list = [self.url, upc, title, price_including_tax, price_excluding_tax, number_available, description, category, rating, image_url]
            return data_list
        except Exception as e:
            logging.error(f"Erreur lors de l'extration des données du livre.\n{e}")
            display_default_error_message()
            return None
    
    def add_to_csv(self):
        FileCreator.update_csv(self.data_list)