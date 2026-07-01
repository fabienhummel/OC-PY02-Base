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
from scraper_functions import save_csv_and_images_by_category


# =============================================================================
# CONSTANTES
# =============================================================================

BASE_URL = "https://books.toscrape.com/"
DEFAULT_EXPORT_FOLDER = "export"


# =============================================================================
# ARGUMENTS DE LA LIGNE DE COMMANDE
# =============================================================================

def create_argument_parser():
    """
    Crée le parseur d'arguments de la ligne de commande.

    Returns:
        argparse.ArgumentParser: Parseur contenant les options disponibles.
    """
    parser = argparse.ArgumentParser(
        description="Scraper Books to Scrape et générer un CSV par catégorie avec les images."
    )

    parser.add_argument(
        "--export-folder",
        "--dossier-export",
        dest="export_folder",
        default=DEFAULT_EXPORT_FOLDER,
        help="Dossier racine où enregistrer les exports. Par défaut : export."
    )

    return parser


# =============================================================================
# PROGRAMME PRINCIPAL
# =============================================================================

def main():
    """
    Lance l'extraction complète des données.

    La fonction récupère les catégories du site, génère un fichier CSV par
    catégorie et télécharge les images correspondantes.
    """
    parser = create_argument_parser()
    args = parser.parse_args()

    # Récupération des liens de toutes les catégories
    category_links = extract_category_links(BASE_URL)

    # Création des CSV et téléchargement des images
    csv_files = save_csv_and_images_by_category(
        category_links,
        args.export_folder
    )

    # Affichage des fichiers CSV créés
    for csv_file in csv_files:
        print(f"CSV créé : {csv_file}")

    print(f"Nombre de fichiers CSV créés : {len(csv_files)}")


# =============================================================================
# POINT D'ENTRÉE DU SCRIPT
# =============================================================================

if __name__ == "__main__":
    main()