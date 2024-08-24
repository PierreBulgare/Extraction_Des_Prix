import math
from settings import logging, display_default_error_message
from packages.extractor import Extractor
from books import Book

class Category:
    def __init__(self, url):
        self.current_page = 1
        self.url = url
        self.soup = Extractor.get_html_content(self.url)
        if self.soup is not None:
            self.name = self.get_category_name()
            self.pages_number = self.get_page_total()
            self.books = self.get_books()
        else:
            self.name = None
            self.pages_number = None
            self.books = None

    def set_next_page(self):
        """Change de page"""
        self.pages_number -= 1
        if self.pages_number > 0:
            next_page = self.current_page + 1
            self.url = f"https://{'/'.join(self.url.split('/')[2:-1])}/page-{next_page}.html" # Mise à jour de l'url
            self.soup = Extractor.get_html_content(self.url) # Mise à jour du contenu html
            self.current_page = next_page # Mise à jour de la page active

    def get_category_name(self)-> str|None:
        """Retourne le nom de la catégorie"""
        try:
            return self.soup.find("div", class_="page-header").find("h1").string
        except Exception as e:
            logging.error("Impossible de récupérer le nom de la catégorie !")
            display_default_error_message()
            return None
    
    def get_page_total(self)-> int:
        """Retourne le nombre de pages en fonction du nombre de livres trouvés dans la catégorie"""
        return math.ceil(int(self.soup.find("form", class_="form-horizontal").find_next("strong").string)/20)
    
    def get_books(self)-> list:
        """Retourne la liste des livres de la catégorie"""
        logging.info(f"Extraction des livres de la catégorie [{self.name}]")
        books = []
        while self.pages_number > 0:
            # Parcourt toutes les pages de la catégorie et ajoute les livres à la liste [books]
            all_h3 = self.soup.find_all("h3") # Extrait toutes les balises <h3> contenant les balises <a>
            for book in all_h3:
                # Ajoute une instance de la classe Book à la liste [books]
                books.append(Book(book.find("a")["href"].replace("../../../", "https://books.toscrape.com/catalogue/")))
            # Changer de page
            self.set_next_page()
        return books

    def add_books_to_csv(self):
        """Ajout les données des livres dans un fichier CSV"""
        for book in self.books:
            book.add_to_csv()