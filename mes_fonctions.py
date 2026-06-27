from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import csv
from pathlib import Path




########################################################################################
def extraire_liens_categories(BASE_URL):
    """
    Extrait tous les liens des catégories depuis la page d'accueil.

    Args:
        base_url (str): URL de la page d'accueil du site.

    Returns:
        list: Liste des URL complètes des catégories.
    """
    liens_categories = []

    try:
        page_accueil = requests.get(BASE_URL)
        page_accueil.raise_for_status()

        soup = BeautifulSoup(page_accueil.text, "html.parser")

        categories = soup.select("div.side_categories ul li ul li a")
        for categorie in categories:
            lien_relatif = categorie.get("href")
            lien_complet = urljoin(BASE_URL, lien_relatif)
            liens_categories.append(lien_complet)

    except requests.exceptions.RequestException as erreur:
        print(f"Erreur lors de la récupération des catégories : {erreur}")
        
    return liens_categories

#######################################################################################
def passer_toutes_les_categories(liens_categories):
    """
    Parcourt toutes les catégories et récupère tous les liens des livres.

    Args:
        liens_categories (list): Liste des URL des catégories.

    Returns:
        list: Liste des URL complètes de tous les livres de toutes les catégories.
    """
    liens_livres_toutes_categories = []

    for lien_categorie in liens_categories:
        liens_livres_dune_categorie = passer_toutes_les_pages_dune_categorie(lien_categorie)
        liens_livres_toutes_categories.extend(liens_livres_dune_categorie)

    return liens_livres_toutes_categories



######################################################################################
def extraire_liens_livres(page_a_traiter):
    """
    Extrait tous les liens des livres depuis une page donnée.

    Args:
        page_a_traiter (str): URL de la page à traiter.

    Returns:
        list: Liste des URL complètes des livres présents sur la page.
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

#######################################################################################
def passer_toutes_les_pages_dune_categorie(lien_categorie):
    """
    Parcourt toutes les pages d'une catégorie et récupère tous les liens des livres.

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

########################################################################################
def extraire_infos_livre(lien_livre):
    """
    Extrait les informations d'un livre depuis l'URL de sa page.

    Args:
        lien_livre (str): URL de la page du livre.

    Returns:
        dict: Dictionnaire contenant les informations du livre.
    """
    try:
        page = requests.get(lien_livre)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, "html.parser")

        upc = soup.select_one('th:-soup-contains("UPC") + td').text
        titre = soup.select_one("h1").text
        prix_ttc = soup.select_one('th:-soup-contains("Price (incl. tax)") + td').text
        prix_ht = soup.select_one('th:-soup-contains("Price (excl. tax)") + td').text
        disponibilite = soup.select_one('th:-soup-contains("Availability") + td').text
        nombre_disponible = "".join(filter(str.isdigit, disponibilite))
        description = soup.select_one("#product_description ~ p").text
        categorie = soup.select("ul.breadcrumb li a")[-1].text
        
        conversion_notes = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }

        note_texte = soup.select_one(".star-rating")["class"][1]
        note = conversion_notes.get(note_texte)

        image_relative = soup.select_one(".carousel-inner img")["src"]
        image_url = urljoin(lien_livre, image_relative)

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

#########################################################################################
def extraire_infos_tous_livres(liens_livres_toutes_categories):
    """
    Extrait les informations de tous les livres à partir d'une liste d'URL.

    Args:
        liens_livres_toutes_categories (list): Liste des URL des pages de livres.

    Returns:
        list: Liste de dictionnaires contenant les informations de tous les livres.
    """
    infos_livres = []

    for lien_livre in liens_livres_toutes_categories:
        infos_livre = extraire_infos_livre(lien_livre)

        if infos_livre:
            infos_livres.append(infos_livre)

    return infos_livres

#########################################################################################
def sauvegarder_infos_livres_csv(infos_livres, dossier_export, nom_fichier):
    """
    Sauvegarde les informations des livres dans un fichier CSV.

    Args:
        infos_livres (list): Liste de dictionnaires contenant les informations des livres.
        dossier_export (str): Nom du dossier où enregistrer le fichier CSV.
        nom_fichier (str): Nom du fichier CSV à créer.

    Returns:
        Path: Chemin du fichier CSV créé.
    """
    chemin_dossier = Path(dossier_export)
    chemin_dossier.mkdir(parents=True, exist_ok=True)

    chemin_fichier = chemin_dossier / nom_fichier

    entetes = [
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

    with open(chemin_fichier, "w", newline="", encoding="utf-8-sig") as fichier_csv:
        writer = csv.DictWriter(fichier_csv, fieldnames=entetes)
        writer.writeheader()
        writer.writerows(infos_livres)

    return chemin_fichier
