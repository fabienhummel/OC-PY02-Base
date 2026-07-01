"""
scraper_functions.py

Ce fichier contient les fonctions utilisées par scraper_books.py.

Organisation :

1. Imports

2. Constantes

3. Fonctions outils
   - extract_text()
   - extract_table_value()
   - sanitize_filename()

4. Extraction des liens
   - extract_category_links()
   - extract_book_links()
   - extract_all_book_links_from_category()

5. Extraction des informations des livres
   - extract_book_data()
   - extract_all_books_data()

6. Sauvegarde CSV
   - sauvegarder_infos_livres_csv()

7. Téléchargement des images
   - telecharger_image()
   - telecharger_images_categorie()

8. Export complet
   - sauvegarder_csv_et_images_par_categorie()
"""




# =============================================================================
# 1 IMPORTS
# =============================================================================

import csv
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# =============================================================================
# 2. CONSTANTES
# =============================================================================

# Conversion des notes textuelles du site en valeurs numériques
RATING_CONVERSION = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
}

# En-têtes utilisés pour créer les fichiers CSV
CSV_HEADERS = [
    "product_page_url",
    "universal_product_code",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url",
]



# =============================================================================
# 3. FONCTIONS OUTILS
# =============================================================================

# -----------------------------------------------------------------------------
def extract_text(element):
    """
    Extrait le texte d'un élément HTML.

    Args:
        element (bs4.element.Tag | None): Élément HTML à lire.

    Returns:
        str: Texte nettoyé de l'élément, ou chaîne vide si l'élément est absent.
    """

    if element:
        return element.get_text(strip=True)

    return ""

# -----------------------------------------------------------------------------
def extract_table_value(soup, label):
    """
    Extrait une valeur du tableau "Product Information" d'une page livre.

    La fonction recherche un libellé dans une balise <th>, puis récupère
    la valeur située dans la cellule <td> associée.

    Args:
        soup (BeautifulSoup): Contenu HTML analysé de la page.
        label (str): Nom du champ recherché dans le tableau.

    Returns:
        str: Valeur trouvée dans le tableau, ou chaîne vide si le champ est absent.
    """

    label_cell = soup.find("th", string=label)

    if label_cell:
        value_cell = label_cell.find_next_sibling("td")

        if value_cell:
            return value_cell.get_text(strip=True)

    return ""

# -----------------------------------------------------------------------------
def sanitize_filename(text):
    """
    Nettoie un texte pour l'utiliser comme nom de dossier ou de fichier.

    La fonction met le texte en minuscules, remplace les espaces par des
    underscores et supprime les caractères non adaptés à un nom de fichier.

    Args:
        text (str): Texte à nettoyer.

    Returns:
        str: Texte nettoyé utilisable comme nom de fichier ou de dossier.
    """

    text = text.lower()
    text = text.replace(" ", "_")

    valid_characters = []

    for character in text:
        if character.isalnum() or character in ["_", "-"]:
            valid_characters.append(character)

    return "".join(valid_characters)


# =============================================================================
# 4. EXTRACTION DES LIENS
# =============================================================================

# -----------------------------------------------------------------------------
def extract_category_links(base_url):
    """
    Extrait les liens de toutes les catégories depuis la page d'accueil.

    Args:
        base_url (str): URL de la page d'accueil du site Books to Scrape.

    Returns:
        list: Liste des URL complètes des pages de catégories.
    """

    category_links = []

    try:
        home_page = requests.get(base_url)
        home_page.raise_for_status()

        soup = BeautifulSoup(home_page.text, "html.parser")

        
        categories = soup.select("div.side_categories ul li ul li a") # Sélection des liens des catégories dans le menu latéral gauche
        for category in categories:
            relative_link = category.get("href")
            
            full_link = urljoin(base_url, relative_link) # Transformation du lien relatif en URL complète
            category_links.append(full_link)

    except requests.exceptions.RequestException as error:
        print(f"Erreur lors de la récupération des catégories : {error}")
        
    return category_links

# -----------------------------------------------------------------------------
def extract_book_links(page_to_process):
    """
    Extrait les liens des livres présents sur une page de catégorie.

    La fonction traite uniquement la page reçue en paramètre. Elle ne gère
    pas directement la pagination.

    Args:
        page_to_process (str): URL de la page de catégorie à analyser.

    Returns:
        list: Liste des URL complètes des livres présents sur cette page.
    """

    book_links = []

    try:
        response = requests.get(page_to_process)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.select("article.product_pod h3 a") # Chaque livre est contenu dans un bloc article.product_pod

        for link in links:
            relative_link = link.get("href")

            # Sécurité : on vérifie que le lien existe avant de construire l'URL complète
            if relative_link:
                full_link = urljoin(page_to_process, relative_link)
                book_links.append(full_link)

    except requests.exceptions.RequestException as error:
        print(f"Erreur lors de la récupération des liens des livres : {error}")

    return book_links

# -----------------------------------------------------------------------------
def extract_all_book_links_from_category(category_link):
    """
    Parcourt toutes les pages d'une catégorie et récupère les liens des livres.

    La fonction commence par la première page de la catégorie, extrait les
    liens des livres, puis continue tant qu'un lien "next" est présent.

    Args:
        category_link (str): URL de la première page de la catégorie.

    Returns:
        list: Liste des URL complètes de tous les livres de la catégorie.
    """


    category_book_links = []
    current_page = category_link # La première page à traiter est la page de la catégorie

    while current_page: # Tant qu'une page courante existe, on continue à parcourir la catégorie
        page_book_links = extract_book_links(current_page) # Extraction des liens des livres présents sur la page courante
        category_book_links.extend(page_book_links) # Ajout des liens de la page courante à la liste complète de la catégorie

        try:
            response = requests.get(current_page)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            next_link = soup.select_one("li.next a")

            if next_link:
                relative_next_link = next_link.get("href")
                current_page = urljoin(current_page, relative_next_link)
            else:
                current_page = None # S'il n'y a plus de page suivante, la boucle s'arrête

        except requests.exceptions.RequestException as error:
            print(f"Erreur lors du passage à la page suivante : {error}")
            current_page = None

    return category_book_links

# =============================================================================
# 5. EXTRACTION DES INFORMATIONS DES LIVRES
# =============================================================================

# -----------------------------------------------------------------------------
def extract_book_data(book_url):
    """
    Extrait les informations détaillées d'un livre depuis sa page produit.

    La fonction ouvre la page du livre, analyse son contenu HTML et récupère
    les champs nécessaires pour alimenter le fichier CSV.

    Args:
        book_url (str): URL de la page produit du livre.

    Returns:
        dict | None: Dictionnaire contenant les informations du livre,
        ou None si la page n'a pas pu être récupérée.
    """

    try:
        # Récupération et analyse de la page produit
        response = requests.get(book_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extraction des informations présentes dans le tableau Product Information
        upc = extract_table_value(soup, "UPC")
        price_including_tax = extract_table_value(soup, "Price (incl. tax)")
        price_excluding_tax = extract_table_value(soup, "Price (excl. tax)")
        availability = extract_table_value(soup, "Availability")

        title = extract_text(soup.select_one("h1"))
        description = extract_text(soup.select_one("#product_description ~ p"))
        
        # Nettoyage de la disponibilité pour ne garder que le nombre d'exemplaires
        number_available = "".join(filter(str.isdigit, availability))
        
        # La catégorie est récupérée depuis le fil d'Ariane (breadcrumb)
        breadcrumb = soup.select("ul.breadcrumb li a")

        if len(breadcrumb) >= 3:
            category = breadcrumb[-1].get_text(strip=True)
        else:
            category = ""
        
        # La note est stockée dans une classe CSS, puis convertie en nombre
        rating_block = soup.select_one(".star-rating")

        if rating_block:
            rating_classes = rating_block.get("class", [])

            if len(rating_classes) > 1:
                rating_text = rating_classes[1]
                rating = RATING_CONVERSION.get(rating_text, "")
            else:
                rating = ""
        else:
            rating = ""

        image_tag = soup.select_one(".carousel-inner img")

        if image_tag:
            relative_image = image_tag.get("src")
            image_url = urljoin(book_url, relative_image) # Conversion de l'URL relative de l'image en URL complète
        else:
            image_url = ""

        return {
            "product_page_url": book_url,
            "universal_product_code": upc,
            "title": title,
            "price_including_tax": price_including_tax,
            "price_excluding_tax": price_excluding_tax,
            "number_available": number_available,
            "product_description": description,
            "category": category,
            "review_rating": rating,
            "image_url": image_url,
        }

    except requests.exceptions.RequestException as error:
        print(f"Erreur lors de la récupération du livre : {error}")
        return None

# -----------------------------------------------------------------------------
def extract_all_books_data(all_book_links):
    """
    Extrait les informations détaillées de plusieurs livres.

    La fonction parcourt une liste d'URL de livres et appelle
    extract_book_data() pour chaque livre.

    Args:
        all_book_links (list): Liste des URL des pages de livres.

    Returns:
        list: Liste de dictionnaires contenant les informations des livres.
    """

    books_data = []

    for book_url in all_book_links:
        book_data = extract_book_data(book_url)

        if book_data:
            books_data.append(book_data)

    return books_data

# =============================================================================
# 6. SAUVEGARDE CSV
# =============================================================================

# -----------------------------------------------------------------------------
def sauvegarder_infos_livres_csv(infos_livres, dossier_export, nom_fichier):
    """
    Sauvegarde les informations des livres dans un fichier CSV.

    La fonction crée le dossier de destination si nécessaire, ajoute
    l'extension .csv au nom du fichier si elle est absente, puis écrit
    les données avec les en-têtes définis dans CSV_HEADERS.

    Args:
        infos_livres (list): Liste de dictionnaires contenant les informations des livres.
        dossier_export (str | Path): Dossier où enregistrer le fichier CSV.
        nom_fichier (str): Nom du fichier CSV à créer.

    Returns:
        Path | None: Chemin du fichier CSV créé, ou None si aucune donnée n'est fournie.
    """
    
    # Aucun fichier CSV n'est créé si la liste de livres est vide
    if not infos_livres:
        print("Aucune information de livre à sauvegarder.")
        return None

    chemin_dossier = Path(dossier_export)
    chemin_dossier.mkdir(parents=True, exist_ok=True) # Création du dossier de destination si nécessaire
    
    # Ajout automatique de l'extension .csv si elle n'est pas fournie
    if not nom_fichier.endswith(".csv"):
        nom_fichier = nom_fichier + ".csv"

    chemin_fichier = chemin_dossier / nom_fichier

    with open(chemin_fichier, "w", newline="", encoding="utf-8-sig") as fichier_csv:
        # Écriture du fichier CSV avec les en-têtes définis dans la constante CSV_HEADERS
        writer = csv.DictWriter(
            fichier_csv, 
            fieldnames=CSV_HEADERS,
            delimiter=","
            )
        writer.writeheader()
        writer.writerows(infos_livres)

    return chemin_fichier


# =============================================================================
# 7. TÉLÉCHARGEMENT DES IMAGES
# =============================================================================

# -----------------------------------------------------------------------------
def telecharger_image(image_url, dossier_images, nom_image):
    """
    Télécharge une image depuis son URL et l'enregistre localement.

    La fonction crée le dossier de destination si nécessaire.

    Args:
        image_url (str): URL complète de l'image à télécharger.
        dossier_images (Path): Dossier où enregistrer l'image.
        nom_image (str): Nom du fichier image à créer.

    Returns:
        Path | None: Chemin de l'image téléchargée, ou None en cas d'erreur.
    """

    try:
        dossier_images.mkdir(parents=True, exist_ok=True) # Création du dossier images si nécessaire

        chemin_image = dossier_images / nom_image

        reponse = requests.get(image_url)
        reponse.raise_for_status()

        with open(chemin_image, "wb") as fichier_image: # Ouverture du fichier en mode binaire pour écrire le contenu de l'image
            fichier_image.write(reponse.content)

        return chemin_image

    except requests.exceptions.RequestException as erreur:
        print(f"Erreur lors du téléchargement de l'image : {erreur}")
        return None
    
# -----------------------------------------------------------------------------
def telecharger_images_categorie(infos_livres, dossier_categorie):
    """
    Télécharge les images de tous les livres d'une catégorie.

    La fonction utilise les informations déjà extraites des livres,
    notamment l'URL de l'image et l'UPC, pour enregistrer chaque image
    dans un dossier images.

    Args:
        infos_livres (list): Liste de dictionnaires contenant les informations des livres.
        dossier_categorie (Path): Dossier local de la catégorie.

    Returns:
        list: Liste des chemins des images téléchargées.
    """

    images_telechargees = []
    dossier_images = dossier_categorie / "images" # Les images d'une catégorie sont stockées dans un sous-dossier images

    for livre in infos_livres:
        image_url = livre["image_url"]
        upc = livre["universal_product_code"]

        extension = Path(urlparse(image_url).path).suffix
        nom_image = upc + extension # L'UPC est utilisé comme nom de fichier car il est unique pour chaque livre

        chemin_image = telecharger_image(image_url, dossier_images, nom_image)

        if chemin_image:
            images_telechargees.append(chemin_image)

    return images_telechargees


# =============================================================================
# 8. EXPORT COMPLET
# =============================================================================

# -----------------------------------------------------------------------------
def sauvegarder_csv_et_images_par_categorie(liens_categories, dossier_export="export"):
    """
    Génère les exports CSV et images pour toutes les catégories.

    Pour chaque catégorie, la fonction récupère les liens des livres,
    extrait les informations détaillées, crée un dossier de catégorie,
    enregistre un fichier CSV et télécharge les images associées.

    La structure générée est :
    export/export_YYYYMMDD_HHMMSS/nom_categorie/nom_categorie.csv
    export/export_YYYYMMDD_HHMMSS/nom_categorie/images/

    Args:
        liens_categories (list): Liste des URL des catégories.
        dossier_export (str): Dossier racine des exports.

    Returns:
        list: Liste des chemins des fichiers CSV créés.
    """

    fichiers_csv_crees = []

    # Création d'un dossier d'export daté pour chaque exécution du script
    date_heure = datetime.now().strftime("%Y%m%d_%H%M%S")

    dossier_export_racine = Path(dossier_export)
    dossier_export_date = dossier_export_racine / f"export_{date_heure}" # Création du chemin export/export_YYYYMMDD_HHMMSS

    # Traitement d'une catégorie complète : liens, infos, CSV et images
    for lien_categorie in liens_categories:
        liens_livres_dune_categorie = extract_all_book_links_from_category(lien_categorie)

        infos_livres = extract_all_books_data(liens_livres_dune_categorie)

        if infos_livres:
            nom_categorie = infos_livres[0]["category"] # Le nom de la catégorie sert à créer le dossier et le fichier CSV
            nom_categorie_nettoye = sanitize_filename(nom_categorie)

            dossier_categorie = dossier_export_date / nom_categorie_nettoye
            nom_fichier_csv = nom_categorie_nettoye + ".csv"

            # Sauvegarde du CSV de la catégorie
            chemin_csv = sauvegarder_infos_livres_csv(
                infos_livres,
                dossier_categorie,
                nom_fichier_csv
            )

            telecharger_images_categorie(infos_livres, dossier_categorie) # Téléchargement des images correspondant aux livres du CSV

            fichiers_csv_crees.append(chemin_csv)

    return fichiers_csv_crees

