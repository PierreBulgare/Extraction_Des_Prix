from settings import BTS_URL, dots_animation, stop_event, animation_thread
from packages.extractor import Extractor
from packages.file_creator import FileCreator
from categories import Category
from books import Book
from concurrent.futures import ThreadPoolExecutor, as_completed

# Récupère le mode d'extraction (Un livre, Une catégorie ou Toutes les catégories)
extraction_mode = Extractor.get_extraction_method()

# Extrait et enregistre les données d'un seul produit
if extraction_mode["Mode"] == "One Book":
    print("Extraction des données en cours ...")

    book = Book(extraction_mode["URL"])  # Création d'une instance de la classe Book à partir de l'URL fournie par l'utilisateur
    # Enregistre les données du produit dans un fichier CSV si les données ont bien été extraites
    if book.data_list:
        FileCreator.name_file(book.name,"Livre")
        book.add_to_csv()

# Extrait et enregistre les données de tous les produits d'une catégorie
elif extraction_mode["Mode"] == "One Category":
    print("Extraction des données en cours ...")

    # Démarre l'animation d'affichage des points
    dots_animation(start=True, thread=animation_thread)
    
    category = Category(extraction_mode["URL"])  # Création d'une instance de la classe Category à partir de l'URL fournie par l'utilisateur
    # Enregistre les données de tous les produits dans un fichier CSV si les livres ont bien été trouvés
    if category.books is not None:
        FileCreator.name_file(category.name,"Categorie")
        category.add_books_to_csv()

    # Arrête l'animation d'affichage des points
    dots_animation(stop=True, thread=animation_thread, stop_event=stop_event)

# Extrait et enregistre les données de tous les produits de toutes les catégories du site
elif extraction_mode["Mode"] == "All Categories":
    print("Extraction des données de toutes les catégories en cours...")

    # Démarre l'animation d'affichage des points
    dots_animation(start=True, thread=animation_thread)

    # Extrait toutes les URLs de toutes les catégories à partir de la page d'accueil du site
    categories = Extractor.extract_all_categories_url(Extractor.get_html_content(extraction_mode["URL"]))
    # Si l'extraction des URLs a réussi
    if categories:
        # Création d'un ThreadPoolExecutor avec un maximum de 5 threads pour gérer les tâches en parallèle
        # pour accélérer le processus d'extraction des données de chaque catégorie
        with ThreadPoolExecutor(max_workers=5) as executor:  # 5 Threads
            # Pour chaque URL, une tâche est soumise pour créer une instance de la classe Category
            future_to_category = {executor.submit(Category, category): category for category in categories} # Dictionnaire des tâches en cours
            # Traite les résultats au fur et à mesure que chaque tâche se termine
            for future in as_completed(future_to_category):
                category_obj = future.result() # L'objet Category de la tâche terminée
                # Nomme le fichier CSV correspondant à la catégorie
                FileCreator.name_file(category_obj.name,"Categorie")
                # Ajoute les livres de la catégorie au fichier CSV
                category_obj.add_books_to_csv()

    # Arrête l'animation d'affichage des points
    dots_animation(stop=True, thread=animation_thread, stop_event=stop_event)

print("Extraction terminée !")