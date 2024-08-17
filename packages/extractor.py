import requests
from bs4 import BeautifulSoup
from packages.converter import convert_rating
from settings import logging, display_default_error_message

class Extractor:
    @staticmethod
    def extract_title(soup):
        # Extraction du titre du produit
        try:
            return soup.title.text.split(" |")[0].strip()
        except:
            logging.error("Impossible de récupérer le titre du livre.")

    @staticmethod
    def extract_image_url(soup, title):
        # Extraction de l'url de l'image du produit
        try:
            return soup.find("img", alt=title)["src"].replace("../../", "https://books.toscrape.com/")
        except:
            logging.error("Impossible de récupérer l'url de l'image du livre.")


    @staticmethod
    def extract_category(soup):
        # Extraction de la catégorie du produit
        try:
            return soup.find("ul", class_="breadcrumb").find_all("li")[-2].find("a").string
        except:
            logging.error("Impossible de récupérer le catégorie du livre.")

    @staticmethod
    def extract_rating(soup):
        # Extraction de la note du produit
        try:
            main_div = soup.find("div", class_="product_main") # Extraction du div principal qui contient la note du produit
            rating_text = main_div.find("p", class_="star-rating").get("class")[1] # Extraction de la note en format texte
            return convert_rating(rating_text) # Retourne la note au format numérique
        except:
            logging.error("Impossible de récupérer la note du livre.")

    @staticmethod
    def extract_description(soup):
        # Extraction de la description du produit
        try:
            return soup.find(id="product_description").find_next("p").string
        except:
            logging.error("Impossible de récupérer la description du livre.")

    @staticmethod
    def extract_informations(soup):
        # Extraction des informations sur le produit (UPC, Prix avec et sans taxe, Stock disponible)
        try:
            table_rows = soup.find("table").find_all("tr") # Extraction de toutes les lignes du tableau contenant les informations sur le produit
            product_informations = {} # Initialisation du dictionnaire qui va contenir les informations nécessaires
            required_informations = ["UPC", "Price (incl. tax)", "Price (excl. tax)", "Availability"] # Informations à récupérer

            for row in table_rows:
                information = row.find("th").text # Extraction du titre de l'information
                if information not in required_informations: # Si l'information n'est pas nécessaire, on passe à la suivante
                    continue
                value = row.find("td").text # Extraction du contenu de la valeur de l'information
                if information == "Availability":
                    value = int(value.split("(")[1].split(" available")[0]) # Récupération de la valeur numérique du stock disponible
                product_informations[information] = value # Ajout dans le dictionnaire (Clé: Nom de l'information, Valeur: Valeur de l'information)
            return product_informations # Retour le dictionnaire contenant l'UPC, les prix et le stock disponible
        except:
            logging.error("Impossible de récupérer l'upc, les prix et la disponibilité du livre.")

    @staticmethod
    def get_html_content(url):
        try:
            # Requête HTTP pour récupérer le contenu de la page
            page = requests.get(url)
            page.raise_for_status()  # Cela déclenchera une erreur si le statut HTTP est différent de 200
            # Parser la page
            soup = BeautifulSoup(page.content, "html.parser")
            return soup
        except requests.exceptions.RequestException as e:
            logging.error(f"Une erreur a été détecté pendant la requête HTTP!\n{e}")
            logging.info("Le programme va s'arrêter.")
            display_default_error_message()

        return None