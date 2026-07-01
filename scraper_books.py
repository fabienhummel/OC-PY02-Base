"""
scraper_books.py

Script principal du projet OC-PY02-Base.

Ce fichier lance l'extraction complète des données depuis Books to Scrape.
Il utilise les fonctions définies dans scraper_functions.py pour :

1. récupérer les catégories ;
2. parcourir les livres de chaque catégorie ;
3. extraire les informations des livres ;
4. créer un fichier CSV par catégorie ;
5. télécharger les images associées.
"""

import argparse

from scraper_functions import extract_category_links
from scraper_functions import sauvegarder_csv_et_images_par_categorie


# =============================================================================
# CONSTANTES
# =============================================================================

BASE_URL = "https://books.toscrape.com/"
DOSSIER_EXPORT_PAR_DEFAUT = "export"


# =============================================================================
# ARGUMENTS DE LA LIGNE DE COMMANDE
# =============================================================================

def creer_parseur_arguments():
    """
    Crée le parseur d'arguments de la ligne de commande.

    Returns:
        argparse.ArgumentParser: Parseur contenant les options disponibles.
    """
    parseur = argparse.ArgumentParser(
        description="Scraper Books to Scrape et générer un CSV par catégorie avec les images."
    )

    parseur.add_argument(
        "--dossier-export",
        default=DOSSIER_EXPORT_PAR_DEFAUT,
        help="Dossier racine où enregistrer les exports. Par défaut : export."
    )

    return parseur


# =============================================================================
# PROGRAMME PRINCIPAL
# =============================================================================

def main():
    """
    Lance l'extraction complète des données.

    La fonction récupère les catégories du site, génère un fichier CSV par
    catégorie et télécharge les images correspondantes.
    """
    parseur = creer_parseur_arguments()
    arguments = parseur.parse_args()

    # Récupération des liens de toutes les catégories
    liens_categories = extract_category_links(BASE_URL)

    # Création des CSV et téléchargement des images
    fichiers_csv = sauvegarder_csv_et_images_par_categorie(
        liens_categories,
        arguments.dossier_export
    )

    # Affichage des fichiers CSV créés
    for fichier_csv in fichiers_csv:
        print(f"CSV créé : {fichier_csv}")

    print(f"Nombre de fichiers CSV créés : {len(fichiers_csv)}")


# =============================================================================
# POINT D'ENTRÉE DU SCRIPT
# =============================================================================

if __name__ == "__main__":
    main()