from settings import logging, math, display_default_error_message
from packages.extractor import Extractor
from products import Product

class Category:
    def __init__(self, url):
        self.current_page = 1
        self.url = url
        self.soup = Extractor.get_html_content(self.url)
        if self.soup is not None:
            self.name = self.get_category_name()
            self.pages = self.get_page_total()
            self.books = self.get_books()
        else:
            self.name = None
            self.pages = None
            self.books = None

    def set_next_page(self):
        # Changer de page
        self.pages -= 1
        if self.pages > 0:
            next_page = self.current_page + 1
            self.url = f"https://{'/'.join(self.url.split('/')[2:-1])}/page-{next_page}.html" # Mise à jour de l'url
            self.soup = Extractor.get_html_content(self.url) # Mise à jour du contenu html
            self.current_page = next_page # Mise à jour de la page active

    def get_category_name(self):
        # Récupération du nom de la catégorie
        try:
            return self.soup.find("div", class_="page-header").find("h1").string
        except Exception as e:
            logging.error("Impossible de récupérer le nom de la catégorie !")
            display_default_error_message()
            return None
    
    def get_page_total(self):
        # Obtention du nombre de pages de la catégorie en fonction du nombre de livres trouvés
        return math.ceil(int(self.soup.find("form", class_="form-horizontal").find_next("strong").string)/20)
    
    def get_books(self):
        logging.info(f"Extraction des livres de la catégorie [{self.name}]")
        books = []
        while self.pages > 0:
            # Parcourir outes les pages de la catégories et ajouter les livres à la liste books
            all_h3 = self.soup.find_all("h3") # Extraire toutes les balises h3 contenant les balises <a>
            for book in all_h3:
                books.append(Product(book.find("a")["href"].replace("../../../", "https://books.toscrape.com/catalogue/"))) # Ajouter une instance de la classe Product à books
            # Changer de page
            self.set_next_page()
        return books

    def add_books_to_csv(self):
        # Ajouter tous les livres à data.csv
        for book in self.books:
            book.add_to_csv()