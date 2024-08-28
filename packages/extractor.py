import requests
from bs4 import BeautifulSoup
from packages.file_creator import FileCreator
from packages.converter import convert_rating
from settings import logging, display_default_error_message, BTS_URL
from urllib.parse import urlparse

class Extractor:
    @staticmethod
    def get_extraction_method()-> dict:
        """
            Retourne le mode d'extraction sélectionné

            1. Extraction d'un livre (One Book)
            2. Les données de tous les livres d'une catégorie (One Category)
            3. Les données de toutes les catégories de livres (All Categories)
        
        """
        url = None

        def validate_url(url, choice) -> str|None:
            """Valide et retourne l'URL si elle est correcte, sinon retourne None"""
            parsed_url = urlparse(url) # Retourne les composants de l'URL
            
            # Si le schéma de l'URL est vide (Absence de http ou https)
            if not parsed_url.scheme:
                url = "https://" + url # Ajoute le préfixe https:// devant l'URL

            # Si l'URL ne provient pas du site Books to Scrape
            if "books.toscrape.com" != parsed_url.netloc:
                print("Cette URL n'appartient pas à Books to Scrape. Recommencez!")
                return None
            
            # Si la méthode choisi est 1 (Données d'un livre) et que l'URL appartient à une catégorie
            if choice == 1 and "/catalogue/category/books/" in parsed_url.path:
                print("Cet URL appartient à une catégorie, vous devez entrer une URL appartenant à un livre.")
            
            # Si la méthode choisi est 2 (Données des livre d'une catégorie) et que l'URL n'appartient pas à une catégorie
            if choice == 2 and "/catalogue/category/books/" not in parsed_url.path:
                print("L'URL de la catégorie n'est pas correcte. Recommencez !")
                return None
            
            return url # Retourne l'URL si elle est correcte
            

        # Boucle principale pour sélectionner le mode d'extraction
        while True:
            try:
                # Demande de choisir le mode d'extraction
                choice = int(input("""
                Que voulez-vous extraire sur Books to Scrape ?
                    1. Les données d'un livre
                    2. Les données de tous les livres d'une catégorie
                    3. Les données de toutes les catégories de livres
                    4. Quitter le programme
                """))
                
                # Si le choix est "4. Quitter le programme"
                if choice == 4:
                    quit() # Quitter le programme
                
                # Si le choix est dans la rangée des choix autorisées (Entre 1 et 3)
                if 1 <= choice <= 3:
                    # Si le choix est "3. Les données de toutes les catégories de livres"
                    if choice == 3:
                        return {"Mode": "All Categories", "URL": BTS_URL}
                    # Sinon, si le choix est "1. Les données d'un livre ou 2. Les données de tous les livres d'une catégorie"
                    else:
                        complement = "du livre" if choice == 1 else "de la catégorie" # Formatage du texte de url_input

                        # Boucle de vérification de l'URL fournie
                        while url is None:
                            # Choix de l'URL (Livre ou Catégorie)
                            url_input = input(f"Copiez l'URL de la page {complement} de votre choix ou tapez ANNULER pour retourner au menu principal et appuyez sur entrée: ")
                            
                            # Retour au menu principal en cas d'annulation
                            if url_input.upper() == "ANNULER":
                                break

                            if url_input:
                                url = validate_url(url_input, choice)
                            else:
                                print("Vous n'avez pas entré d'URL.")
                        if url is not None:
                            return {"Mode": "One Book" if choice == 1 else "One Category", "URL": url}
                else:
                    print("Vous n'avez pas entré un choix correct. Recommencez !")

            except ValueError:
                print("Veuillez entrer un choix valide ...")
            
    @staticmethod
    def extract_title(soup)-> str:
        # Extraction du titre du produit
        try:
            return soup.title.text.split(" |")[0].strip()
        except:
            logging.error("Impossible de récupérer le titre du livre.")
            return "Titre inconnu"

    @staticmethod
    def extract_image_url(soup, title)-> str:
        # Extraction de l'url de l'image du produit
        try:
            return soup.find("img", alt=title)["src"].replace("../../", BTS_URL)
        except:
            logging.error("Impossible de récupérer l'url de l'image du livre.")
            return "Url inconnu"

    @staticmethod
    def download_image(book_name: str, image_url: str):
        """Télécharge la couverture d'un livre à partir de son url"""
        image = requests.get(image_url) # Requête à partir de l'url de l'image
        # Si la requête a réussi
        if image.status_code == 200:
            extension = image_url.split(".")[-1] # Récupère l'extension de l'image
            # Enregistre l'image
            FileCreator.save_image("Donnees/Images/", f"{FileCreator.format_name(book_name)}.{extension}", image.content)

    @staticmethod
    def extract_category(soup)-> str:
        # Extraction de la catégorie du produit
        try:
            return soup.find("ul", class_="breadcrumb").find_all("li")[-2].find("a").string
        except:
            logging.error("Impossible de récupérer le catégorie du livre.")
            return "Catégorie inconnue"

    def extract_all_categories_url(soup)-> list:
        # Extraction des url de toutes les catégories du site
        urls = []
        try:
            all_li = soup.find("div", class_="side_categories").find_next("li").find("ul").find_all("li")
            for li in all_li:
                urls.append(f"{BTS_URL}{li.find('a')['href']}")
            return urls
        except:
            logging.error("Impossible de récupérer les urls des catégories du site.")

    @staticmethod
    def extract_rating(soup)-> int:
        # Extraction de la note du produit
        try:
            main_div = soup.find("div", class_="product_main") # Extraction du div principal qui contient la note du produit
            rating_text = main_div.find("p", class_="star-rating").get("class")[1] # Extraction de la note en format texte
            return convert_rating(rating_text) # Retourne la note au format numérique
        except:
            logging.error("Impossible de récupérer la note du livre.")
            return 0

    @staticmethod
    def extract_description(soup)-> str:
        # Extraction de la description du produit
        try:
            return soup.find(id="product_description").find_next("p").string
        except:
            logging.error("Impossible de récupérer la description du livre.")
            return "Pas de description"

    @staticmethod
    def extract_informations(soup)-> dict:
        # Extraction des informations sur le produit (UPC, Prix avec et sans taxe, Stock disponible)
        try:
            table_rows = soup.find("table").find_all("tr") # Extraction de toutes les lignes du tableau contenant les informations sur le produit
            book_informations = {} # Initialisation du dictionnaire qui va contenir les informations nécessaires
            required_informations = ["UPC", "Price (incl. tax)", "Price (excl. tax)", "Availability"] # Informations à récupérer

            for row in table_rows:
                information = row.find("th").text # Extraction du titre de l'information
                if information not in required_informations: # Si l'information n'est pas nécessaire, on passe à la suivante
                    continue
                value = row.find("td").text # Extraction du contenu de la valeur de l'information
                if information == "Availability":
                    value = int(value.split("(")[1].split(" available")[0]) # Récupération de la valeur numérique du stock disponible
                book_informations[information] = value # Ajout dans le dictionnaire (Clé: Nom de l'information, Valeur: Valeur de l'information)
            return book_informations # Retour le dictionnaire contenant l'UPC, les prix et le stock disponible
        except:
            logging.error("Impossible de récupérer l'upc, les prix et la disponibilité du livre.")

    @staticmethod
    def get_html_content(url)-> str|None:
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