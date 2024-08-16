from packages.conversion import convert_rating

def extract_title(soup):
    # Extraction du titre du produit
    return soup.title.text.split(" |")[0].strip()

def extract_image_url(soup, title):
    # Extraction de l'url de l'image du produit
    return soup.find("img", alt=title)["src"].replace("../../", "https://books.toscrape.com/")

def extract_category(soup):
    # Extraction de la catégorie du produit
    return soup.find("ul", class_="breadcrumb").find_all("li")[-2].find("a").string

def extract_rating(soup):
    # Extraction de la note du produit
    main_div = soup.find("div", class_="product_main") # Extraction du div principal qui contient la note du produit
    rating_text = main_div.find("p", class_="star-rating").get("class")[1] # Extraction de la note en format texte
    return convert_rating(rating_text) # Retourner la note au format numérique

def extract_description(soup):
    # Extraction de la description du produit
    return soup.find(id="product_description").find_next("p").string

def extract_informations(soup):
    # Extraction des informations sur le produit (UPC, Type du produit, Prix avec et sans taxe, Stock disponible)
    table_rows = soup.find("table").find_all("tr") # Extraire toutes les lignes du tableau contenant les informations sur le produit
    product_informations = {} # Initialisation du dictionnaire qui va contenir les informations nécessaires
    required_informations = ["UPC", "Price (incl. tax)", "Price (excl. tax)", "Availability"] # Informations à récupérer

    for row in table_rows:
        information = row.find("th").text # Extraction du titre de l'information
        if information not in required_informations: # Si l'information n'est pas nécessaire, on passe à la suivante
            continue
        value = row.find("td").text # Extraction du contenu de la valeur de l'information
        if information == "Availability":
            value = int(value.split("(")[1].split(" available")[0]) # Récupération de la valeur numérique du stock disponible
        product_informations[information] = value # Ajout dans le dictionnaire (Clé: Titre de l'information, Valeur: Valeur de l'information)
    return product_informations