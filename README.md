# OC-PY02-Bis - Scraper Books to Scrape

Projet réalisé dans le cadre du parcours OpenClassrooms **Développeur Python**.

L'objectif du projet est de créer un script Python capable d'extraire les informations des livres du site [Books to Scrape](https://books.toscrape.com/), puis de sauvegarder les données dans des fichiers CSV organisés par catégorie.

## Fonctionnalités

Le script permet de :

- récupérer toutes les catégories de livres ;
- parcourir toutes les pages d'une catégorie, y compris la pagination ;
- récupérer tous les liens des pages de livres ;
- extraire les informations détaillées de chaque livre ;
- créer un fichier CSV par catégorie ;
- télécharger les images des livres dans un dossier dédié à chaque catégorie.

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

## Structure du projet

```text
OC-PY02-Bis/
├── export/
│   └── .gitkeep
├── mes_fonctions.py
├── scraper_books.py
├── requirements.txt
├── .gitignore
└── README.md
```

Le dossier `export/` est présent dans le projet, mais son contenu généré est ignoré par Git.

## Installation

Cloner le dépôt :

```bash
git clone https://github.com/fabienhummel/OC-PY02-Bis.git
```

Entrer dans le dossier du projet :

```bash
cd OC-PY02-Bis
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

## Exécution du script

Lancer le script principal :

```bash
python scraper_books.py
```

Le programme extrait les données du site, crée les fichiers CSV et télécharge les images.

## Résultat généré

À chaque exécution, le script crée un dossier d'export daté dans le dossier `export/`.

Exemple :

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

## Dépendances

Les principales bibliothèques utilisées sont :

- `requests` : récupération des pages HTML et téléchargement des images ;
- `beautifulsoup4` : analyse du HTML et extraction des données.

Les autres modules utilisés, comme `csv`, `pathlib`, `datetime` ou `urllib.parse`, font partie de la bibliothèque standard de Python.

## Données non versionnées

Les fichiers générés par le script ne sont pas stockés dans le dépôt GitHub.

Le fichier `.gitignore` ignore le contenu du dossier `export/`, tout en conservant le dossier grâce au fichier `.gitkeep`.

## Logique ETL

Le programme suit une logique ETL simple :

- **Extract** : récupération des pages HTML et des images depuis Books to Scrape ;
- **Transform** : nettoyage des liens, des noms de fichiers, des catégories et des données extraites ;
- **Load** : sauvegarde des données dans des fichiers CSV et enregistrement des images dans des dossiers locaux.

## Auteur

Fabien Hummel