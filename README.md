# OC-PY02-Base - Scraper Books to Scrape

Projet réalisé dans le cadre du parcours OpenClassrooms **Développeur Python**.

L'objectif du projet est de créer un script Python capable d'extraire les informations des livres du site [Books to Scrape](https://books.toscrape.com/), puis de sauvegarder les données dans des fichiers CSV organisés par catégorie.

Le programme télécharge également les images associées aux livres et les range dans des dossiers dédiés.

---

## Fonctionnalités

Le script permet de :

- récupérer toutes les catégories de livres ;
- parcourir toutes les pages d'une catégorie, y compris la pagination ;
- récupérer tous les liens des pages de livres ;
- extraire les informations détaillées de chaque livre ;
- créer un fichier CSV par catégorie ;
- télécharger les images des livres dans un dossier dédié à chaque catégorie ;
- choisir le dossier d'export avec une option de ligne de commande.

---

## Données extraites

Pour chaque livre, le script extrait les informations suivantes :

```text
product_page_url
universal_product_code
title
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url
```

Ces champs sont utilisés comme en-têtes dans les fichiers CSV générés.

---

## Structure du projet

```text
OC-PY02-Base/
├── export/
│   └── .gitkeep
├── scraper_books.py
├── scraper_functions.py
├── requirements.txt
├── .gitignore
└── README.md
```

Le dossier `export/` est présent dans le projet grâce au fichier `.gitkeep`.

Le contenu généré dans `export/` est ignoré par Git afin d'éviter de versionner les fichiers CSV et les images téléchargées.

---

## Rôle des fichiers principaux

### `scraper_books.py`

Fichier principal du projet.

Il permet de :

- définir l'URL de base du site ;
- gérer les arguments de ligne de commande avec `argparse` ;
- lancer l'extraction complète ;
- afficher les fichiers CSV générés.

### `scraper_functions.py`

Fichier contenant les fonctions utilisées par le script principal.

Il contient notamment les fonctions permettant de :

- récupérer les liens des catégories ;
- récupérer les liens des livres ;
- gérer la pagination ;
- extraire les données d'une page produit ;
- sauvegarder les données dans des fichiers CSV ;
- télécharger les images ;
- organiser l'export par catégorie.

### `requirements.txt`

Fichier contenant les dépendances Python nécessaires au projet.

---

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/fabienhummel/OC-PY02-Base.git
```

Entrer dans le dossier du projet :

```bash
cd OC-PY02-Base
```

Créer un environnement virtuel :

```bash
python3 -m venv .venv
```

Activer l'environnement virtuel sur macOS ou Linux :

```bash
source .venv/bin/activate
```

Activer l'environnement virtuel sur Windows :

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## Exécution du script

Lancer le script principal avec le dossier d'export par défaut :

```bash
python scraper_books.py
```

Par défaut, les données générées sont enregistrées dans le dossier :

```text
export/
```

---

## Aide en ligne de commande

Le script utilise `argparse` pour gérer les options de ligne de commande.

Afficher l'aide :

```bash
python scraper_books.py --help
```

ou :

```bash
python scraper_books.py -h
```

---

## Options disponibles

### Choisir le dossier d'export

L'option principale est :

```bash
--export-folder
```

Exemple :

```bash
python scraper_books.py --export-folder export_test
```

Dans ce cas, les données seront enregistrées dans le dossier :

```text
export_test/
```

L'ancien nom d'option est encore accepté pour compatibilité :

```bash
python scraper_books.py --dossier-export export_test
```

Cependant, l'option recommandée est maintenant :

```bash
--export-folder
```

---

## Résultat généré

À chaque exécution, le script crée un dossier d'export daté dans le dossier d'export choisi.

Exemple avec le dossier par défaut `export/` :

```text
export/
└── export_20260627_193000/
    ├── travel/
    │   ├── travel.csv
    │   └── images/
    │       ├── a897fe39b1053632.jpg
    │       └── ...
    ├── mystery/
    │   ├── mystery.csv
    │   └── images/
    └── historical_fiction/
        ├── historical_fiction.csv
        └── images/
```

Chaque catégorie possède son propre dossier contenant :

- un fichier CSV avec les informations des livres ;
- un dossier `images/` contenant les images des livres de la catégorie.

---

## Dépendances

Les principales bibliothèques utilisées sont :

- `requests` : récupération des pages HTML et téléchargement des images ;
- `beautifulsoup4` : analyse du HTML et extraction des données.

Les autres modules utilisés font partie de la bibliothèque standard de Python :

- `argparse` ;
- `csv` ;
- `datetime` ;
- `pathlib` ;
- `urllib.parse`.

---

## Données non versionnées

Les fichiers générés par le script ne sont pas stockés dans le dépôt GitHub.

Le fichier `.gitignore` ignore le contenu généré du dossier `export/`, tout en conservant le dossier grâce au fichier `.gitkeep`.

Le dossier de configuration PyCharm `.idea/` est également ignoré.

---

## Logique ETL

Le fonctionnement du programme suit une logique ETL : **Extract, Transform, Load**.

### Extract

Le programme récupère les données depuis le site Books to Scrape :

- les catégories ;
- les pages de catégories ;
- les liens des livres ;
- les informations détaillées de chaque livre ;
- les images associées aux livres.

### Transform

Le programme transforme certaines données avant de les sauvegarder :

- conversion des liens relatifs en liens absolus ;
- nettoyage des noms de catégories pour créer des noms de dossiers et de fichiers valides ;
- extraction du nombre disponible à partir du texte de disponibilité ;
- conversion des notes textuelles en valeurs numériques ;
- organisation des données dans des dictionnaires Python.

### Load

Le programme enregistre les données localement :

- création d'un dossier d'export daté ;
- création d'un dossier par catégorie ;
- création d'un fichier CSV par catégorie ;
- téléchargement des images dans un dossier `images/`.

---

## Convention de nommage du code

Les noms de fonctions, variables et constantes sont écrits en anglais afin de respecter les conventions courantes de développement Python.

Exemples :

```python
extract_category_links()
extract_book_data()
save_books_data_to_csv()
download_category_images()
save_csv_and_images_by_category()
```

Les commentaires et la documentation restent en français afin de faciliter la compréhension du projet.

---

## Améliorations possibles

Cette version du projet répond au cahier des charges demandé pour la version bêta.

Certaines améliorations pourraient être ajoutées dans une version future :

- ajouter un mode interactif permettant de choisir les catégories à extraire depuis un menu dans le terminal ;
- ajouter davantage d'options en ligne de commande pour piloter l'exécution du programme ;
- permettre l'extraction de toutes les catégories ou seulement de certaines catégories sélectionnées ;
- ajouter un mode silencieux pour limiter l'affichage dans le terminal pendant l'exécution ;
- ajouter une commande pour lister les catégories disponibles ;
- ajouter une commande pour lister les livres d'une ou plusieurs catégories ;
- ajouter une commande pour afficher le détail d'un ou plusieurs livres ;
- ajouter un fichier de log pour conserver l'historique des actions réalisées et des erreurs rencontrées ;
- améliorer la gestion des erreurs avec une poursuite de l'extraction lorsqu'une catégorie ou un livre ne peut pas être traité.

---

## Auteur

Fabien Hummel