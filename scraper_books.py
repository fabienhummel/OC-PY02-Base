from mes_fonctions import extraire_liens_categories
from mes_fonctions import sauvegarder_csv_par_categorie


BASE_URL = "https://books.toscrape.com/"


liens_categories = extraire_liens_categories(BASE_URL)

fichiers_csv = sauvegarder_csv_par_categorie(liens_categories, "export")

for fichier_csv in fichiers_csv:
    print(f"CSV créé : {fichier_csv}")

print(f"Nombre de fichiers CSV créés : {len(fichiers_csv)}")
