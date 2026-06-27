from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup




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
