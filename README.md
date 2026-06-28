# OC-PY02-Base - Scraper Books to Scrape

Projet réalisé dans le cadre du parcours OpenClassrooms **Développeur Python**.

L'objectif du projet est de créer un script Python capable d'extraire les informations des livres du site [Books to Scrape](https://books.toscrape.com/), puis de sauvegarder les données dans des fichiers CSV organisés par catégorie.

## Fonctionnalités

Le script permet de :

- récupérer toutes les catégories de livres ;
- parcourir toutes les pages d'une catégorie, y compris la pagination ;
- récupérer tous les liens des pages de livres ;
- extraire les informations détaillées de chaque livre ;
- créer un fichier CSV par catégorie ;
- télécharger les images des livres dans un dossier dédié à chaque catégorie ;
- choisir le dossier d'export avec une option de ligne de commande.

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
OC-PY02-Base/
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

## Exécution du script

Lancer le script principal :

```bash
python scraper_books.py
```

Le programme extrait les données du site, crée les fichiers CSV et télécharge les images.

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

## Options disponibles

### Choisir le dossier d'export

Par défaut, les fichiers générés sont enregistrés dans le dossier `export/`.

Il est possible de choisir un autre dossier d'export avec l'option `--dossier-export`.

Exemple :

```bash
python scraper_books.py --dossier-export export_test
```

Dans ce cas, les données seront enregistrées dans le dossier `export_test/`.

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

## Dépendances

Les principales bibliothèques utilisées sont :

- `requests` : récupération des pages HTML et téléchargement des images ;
- `beautifulsoup4` : analyse du HTML et extraction des données.

Les autres modules utilisés, comme `csv`, `pathlib`, `datetime`, `argparse` ou `urllib.parse`, font partie de la bibliothèque standard de Python.

## Données non versionnées

Les fichiers générés par le script ne sont pas stockés dans le dépôt GitHub.

Le fichier `.gitignore` ignore le contenu du dossier `export/`, tout en conservant le dossier grâce au fichier `.gitkeep`.

## Logique ETL

Même si le code n'est pas découpé explicitement en modules nommés `Extract`, `Transform` et `Load`, son fonctionnement suit une logique ETL simple :

- **Extract** : récupération des pages HTML, des catégories, des liens des livres et des images depuis Books to Scrape ;
- **Transform** : nettoyage des liens, des noms de fichiers, des catégories et des données extraites ;
- **Load** : sauvegarde des données dans des fichiers CSV et enregistrement des images dans des dossiers locaux.

## Améliorations possibles

Cette version du projet répond au cahier des charges demandé pour la version bêta. Certaines fonctionnalités présentes dans une version plus complète du projet pourraient être réintégrées dans une évolution future :

- ajouter un **mode interactif** permettant de choisir les catégories à extraire depuis un menu dans le terminal ;
- ajouter davantage d'**options en ligne de commande** pour piloter l'exécution du programme ;
- permettre l'extraction de **toutes les catégories** ou seulement de certaines catégories sélectionnées ;
- permettre de choisir plus finement le **dossier de sortie** ;
- ajouter un **mode silencieux** pour limiter l'affichage dans le terminal pendant l'exécution ;
- ajouter une commande pour **lister les catégories disponibles** ;
- ajouter une commande pour **lister les livres** d'une ou plusieurs catégories ;
- ajouter une commande pour **afficher le détail d'un ou plusieurs livres** ;
- ajouter un **fichier de log** pour conserver l'historique des actions réalisées et des erreurs rencontrées ;
- améliorer la gestion des erreurs avec une poursuite de l'extraction lorsqu'une catégorie ou un livre ne peut pas être traité.

## Auteur

Fabien Hummel