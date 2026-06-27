from mes_fonctions import extraire_liens_categories
from mes_fonctions import passer_toutes_les_categories

BASE_URL = "https://books.toscrape.com/"

liens_categories = extraire_liens_categories(BASE_URL)

liens_livres_toutes_categories = passer_toutes_les_categories(liens_categories)

for lien_livre in liens_livres_toutes_categories:
    print(lien_livre)

print(f"Nombre total de livres trouvés : {len(liens_livres_toutes_categories)}")