from pprint import pprint

from mes_fonctions import extraire_liens_categories
from mes_fonctions import passer_toutes_les_categories
from mes_fonctions import extraire_infos_tous_livres
from mes_fonctions import sauvegarder_infos_livres_csv


BASE_URL = "https://books.toscrape.com/"


liens_categories = extraire_liens_categories(BASE_URL)

liens_livres_toutes_categories = passer_toutes_les_categories(liens_categories)

infos_livres = extraire_infos_tous_livres(liens_livres_toutes_categories[:3])

chemin_csv = sauvegarder_infos_livres_csv(
    infos_livres,
    "export",
    "livres.csv"
)

print(f"Fichier CSV créé : {chemin_csv}")

for infos_livre in infos_livres:
    pprint(infos_livre)
    print("-" * 80)

print(f"Nombre de livres testés : {len(infos_livres)}")
