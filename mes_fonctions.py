"""
mes_fonctions.py

Ce fichier contient les fonctions utilisées par scraper_books.py.

Organisation :

1. Imports

2. Constantes

3. Fonctions outils
   - extraire_texte()
   - extraire_valeur_tableau()
   - nettoyer_nom_fichier()

4. Extraction des liens
   - extraire_liens_categories()
   - extraire_liens_livres()
   - passer_toutes_les_pages_dune_categorie()

5. Extraction des informations des livres
   - extraire_infos_livre()
   - extraire_infos_tous_livres()

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

CONVERSION_NOTES = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
}

ENTETES_CSV = [
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
def extraire_texte(element):
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
def extraire_valeur_tableau(soup, libelle):
    """
    Extrait une valeur du tableau "Product Information" d'une page livre.

    La fonction recherche un libellé dans une balise <th>, puis récupère
    la valeur située dans la cellule <td> associée.

    Args:
        soup (BeautifulSoup): Contenu HTML analysé de la page.
        libelle (str): Nom du champ recherché dans le tableau.

    Returns:
        str: Valeur trouvée dans le tableau, ou chaîne vide si le champ est absent.
    """

    cellule_libelle = soup.find("th", string=libelle)

    if cellule_libelle:
        cellule_valeur = cellule_libelle.find_next_sibling("td")

        if cellule_valeur:
            return cellule_valeur.get_text(strip=True)

    return ""

# -----------------------------------------------------------------------------
def nettoyer_nom_fichier(texte):
    """
    Nettoie un texte pour l'utiliser comme nom de dossier ou de fichier.

    La fonction met le texte en minuscules, remplace les espaces par des
    underscores et supprime les caractères non adaptés à un nom de fichier.

    Args:
        texte (str): Texte à nettoyer.

    Returns:
        str: Texte nettoyé utilisable comme nom de fichier ou de dossier.
    """

    texte = texte.lower()
    texte = texte.replace(" ", "_")

    caracteres_valides = []

    for caractere in texte:
        if caractere.isalnum() or caractere in ["_", "-"]:
            caracteres_valides.append(caractere)

    return "".join(caracteres_valides)


# =============================================================================
# 4. EXTRACTION DES LIENS
# =============================================================================

# -----------------------------------------------------------------------------
def extraire_liens_categories(base_url):
    """
    Extrait les liens de toutes les catégories depuis la page d'accueil.

    Args:
        base_url (str): URL de la page d'accueil du site Books to Scrape.

    Returns:
        list: Liste des URL complètes des pages de catégories.
    """

    liens_categories = []

    try:
        page_accueil = requests.get(base_url)
        page_accueil.raise_for_status()

        soup = BeautifulSoup(page_accueil.text, "html.parser")

        categories = soup.select("div.side_categories ul li ul li a")
        for categorie in categories:
            lien_relatif = categorie.get("href")
            lien_complet = urljoin(base_url, lien_relatif)
            liens_categories.append(lien_complet)

    except requests.exceptions.RequestException as erreur:
        print(f"Erreur lors de la récupération des catégories : {erreur}")
        
    return liens_categories

# -----------------------------------------------------------------------------
def extraire_liens_livres(page_a_traiter):
    """
    Extrait les liens des livres présents sur une page de catégorie.

    La fonction traite uniquement la page reçue en paramètre. Elle ne gère
    pas directement la pagination.

    Args:
        page_a_traiter (str): URL de la page de catégorie à analyser.

    Returns:
        list: Liste des URL complètes des livres présents sur cette page.
    """

    liens_livres = []

    try:
        page = requests.get(page_a_traiter)
        page.raise_for_status()

        soup = BeautifulSoup(page.text, "html.parser")

        liens = soup.select("article.product_pod h3 a")

        for lien in liens:
            lien_relatif = lien.get("href")

            if lien_relatif:
                lien_complet = urljoin(page_a_traiter, lien_relatif)
                liens_livres.append(lien_complet)

    except requests.exceptions.RequestException as erreur:
        print(f"Erreur lors de la récupération des liens des livres : {erreur}")

    return liens_livres

# -----------------------------------------------------------------------------
def passer_toutes_les_pages_dune_categorie(lien_categorie):
    """
    Parcourt toutes les pages d'une catégorie et récupère les liens des livres.

    La fonction commence par la première page de la catégorie, extrait les
    liens des livres, puis continue tant qu'un lien "next" est présent.

    Args:
        lien_categorie (str): URL de la première page de la catégorie.

    Returns:
        list: Liste des URL complètes de tous les livres de la catégorie.
    """


    liens_livres_dune_categorie = []
    page_courante = lien_categorie

    while page_courante:
        liens_livres_page = extraire_liens_livres(page_courante)
        liens_livres_dune_categorie.extend(liens_livres_page)

        try:
            page = requests.get(page_courante)
            page.raise_for_status()

            soup = BeautifulSoup(page.text, "html.parser")

            lien_next = soup.select_one("li.next a")

            if lien_next:
                lien_relatif_next = lien_next.get("href")
                page_courante = urljoin(page_courante, lien_relatif_next)
            else:
                page_courante = None

        except requests.exceptions.RequestException as erreur:
            print(f"Erreur lors du passage à la page suivante : {erreur}")
            page_courante = None

    return liens_livres_dune_categorie

# =============================================================================
# 5. EXTRACTION DES INFORMATIONS DES LIVRES
# =============================================================================

# -----------------------------------------------------------------------------
def extraire_infos_livre(lien_livre):
    """
    Extrait les informations détaillées d'un livre depuis sa page produit.

    La fonction ouvre la page du livre, analyse son contenu HTML et récupère
    les champs nécessaires pour alimenter le fichier CSV.

    Args:
        lien_livre (str): URL de la page produit du livre.

    Returns:
        dict | None: Dictionnaire contenant les informations du livre,
        ou None si la page n'a pas pu être récupérée.
    """

    try:
        page = requests.get(lien_livre)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, "html.parser")

        upc = extraire_valeur_tableau(soup, "UPC")
        prix_ttc = extraire_valeur_tableau(soup, "Price (incl. tax)")
        prix_ht = extraire_valeur_tableau(soup, "Price (excl. tax)")
        disponibilite = extraire_valeur_tableau(soup, "Availability")

        titre = extraire_texte(soup.select_one("h1"))
        description = extraire_texte(soup.select_one("#product_description ~ p"))

        nombre_disponible = "".join(filter(str.isdigit, disponibilite))

        fil_ariane = soup.select("ul.breadcrumb li a")

        if len(fil_ariane) >= 3:
            categorie = fil_ariane[-1].get_text(strip=True)
        else:
            categorie = ""

        bloc_note = soup.select_one(".star-rating")

        if bloc_note:
            classes_note = bloc_note.get("class", [])
            note_texte = classes_note[1]
            note = CONVERSION_NOTES.get(note_texte, "")
        else:
            note = ""

        image = soup.select_one(".carousel-inner img")

        if image:
            image_relative = image.get("src")
            image_url = urljoin(lien_livre, image_relative)
        else:
            image_url = ""

        return {
            "product_page_url": lien_livre,
            "universal_product_code": upc,
            "title": titre,
            "price_including_tax": prix_ttc,
            "price_excluding_tax": prix_ht,
            "number_available": nombre_disponible,
            "product_description": description,
            "category": categorie,
            "review_rating": note,
            "image_url": image_url,
        }

    except requests.exceptions.RequestException as erreur:
        print(f"Erreur lors de la récupération du livre : {erreur}")
        return None

# -----------------------------------------------------------------------------
def extraire_infos_tous_livres(liens_livres_toutes_categories):
    """
    Extrait les informations détaillées de plusieurs livres.

    La fonction parcourt une liste d'URL de livres et appelle
    extraire_infos_livre() pour chaque livre.

    Args:
        liens_livres_toutes_categories (list): Liste des URL des pages de livres.

    Returns:
        list: Liste de dictionnaires contenant les informations des livres.
    """

    infos_livres = []

    for lien_livre in liens_livres_toutes_categories:
        infos_livre = extraire_infos_livre(lien_livre)

        if infos_livre:
            infos_livres.append(infos_livre)

    return infos_livres

# =============================================================================
# 6. SAUVEGARDE CSV
# =============================================================================

# -----------------------------------------------------------------------------
def sauvegarder_infos_livres_csv(infos_livres, dossier_export, nom_fichier):
    """
    Sauvegarde les informations des livres dans un fichier CSV.

    La fonction crée le dossier de destination si nécessaire, ajoute
    l'extension .csv au nom du fichier si elle est absente, puis écrit
    les données avec les en-têtes définis dans ENTETES_CSV.

    Args:
        infos_livres (list): Liste de dictionnaires contenant les informations des livres.
        dossier_export (str | Path): Dossier où enregistrer le fichier CSV.
        nom_fichier (str): Nom du fichier CSV à créer.

    Returns:
        Path | None: Chemin du fichier CSV créé, ou None si aucune donnée n'est fournie.
    """

    if not infos_livres:
        print("Aucune information de livre à sauvegarder.")
        return None

    chemin_dossier = Path(dossier_export)
    chemin_dossier.mkdir(parents=True, exist_ok=True)

    if not nom_fichier.endswith(".csv"):
        nom_fichier = nom_fichier + ".csv"

    chemin_fichier = chemin_dossier / nom_fichier

    with open(chemin_fichier, "w", newline="", encoding="utf-8-sig") as fichier_csv:
        writer = csv.DictWriter(
            fichier_csv, 
            fieldnames=ENTETES_CSV, 
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
        dossier_images.mkdir(parents=True, exist_ok=True)

        chemin_image = dossier_images / nom_image

        reponse = requests.get(image_url)
        reponse.raise_for_status()

        with open(chemin_image, "wb") as fichier_image:
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
    dossier_images = dossier_categorie / "images"

    for livre in infos_livres:
        image_url = livre["image_url"]
        upc = livre["universal_product_code"]

        extension = Path(urlparse(image_url).path).suffix
        nom_image = upc + extension

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

    date_heure = datetime.now().strftime("%Y%m%d_%H%M%S")

    dossier_export_racine = Path(dossier_export)
    dossier_export_date = dossier_export_racine / f"export_{date_heure}"

    for lien_categorie in liens_categories:
        liens_livres_dune_categorie = passer_toutes_les_pages_dune_categorie(lien_categorie)

        infos_livres = extraire_infos_tous_livres(liens_livres_dune_categorie)

        if infos_livres:
            nom_categorie = infos_livres[0]["category"]
            nom_categorie_nettoye = nettoyer_nom_fichier(nom_categorie)

            dossier_categorie = dossier_export_date / nom_categorie_nettoye
            nom_fichier_csv = nom_categorie_nettoye + ".csv"

            chemin_csv = sauvegarder_infos_livres_csv(
                infos_livres,
                dossier_categorie,
                nom_fichier_csv
            )

            telecharger_images_categorie(infos_livres, dossier_categorie)

            fichiers_csv_crees.append(chemin_csv)

    return fichiers_csv_crees













# =============================================================================
# Fonctions orphelines (non utilisées dans le code principal)
# =============================================================================




# -----------------------------------------------------------------------------
# def passer_toutes_les_categories(liens_categories):
#     """
#     Parcourt toutes les catégories et récupère tous les liens des livres.

#     Args:
#         liens_categories (list): Liste des URL des catégories.

#     Returns:
#         list: Liste des URL complètes de tous les livres de toutes les catégories.
#     """
#     liens_livres_toutes_categories = []

#     for lien_categorie in liens_categories:
#         liens_livres_dune_categorie = passer_toutes_les_pages_dune_categorie(lien_categorie)
#         liens_livres_toutes_categories.extend(liens_livres_dune_categorie)

#     return liens_livres_toutes_categories






















