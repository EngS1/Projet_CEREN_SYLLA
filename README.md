# MeetingPro — Gestion de réservations de salles

Application de bureau en **Python** (interface **tkinter**) pour gérer des clients, des salles et des réservations de salles de réunion. Interface en français, données stockées dans un fichier JSON, actions et erreurs journalisées avec le module `logging`.

Projet réalisé **en binôme** (Daouda SYLLA et CEREN).

**Technologies :** Python 3.10+, tkinter, tkcalendar, email-validator, JSON, logging, pytest.

## Fonctionnalités

**Clients**
- Ajout d'un client (nom, prénom, email) avec validation de l'adresse email.
- Affichage de la liste des clients enregistrés.

**Salles**
- Ajout d'une salle avec un **nom unique**, un **type** (Standard, Conférence, Informatique) et une **capacité**.
- Capacité maximale contrôlée selon le type : 4 personnes pour Standard et Informatique, 12 pour Conférence.
- Affichage de la liste des salles.

**Réservations**
- Réservation d'une salle pour un client sur un créneau précis (date et heure de début et de fin choisies avec un calendrier).
- Détection des chevauchements : une salle déjà réservée sur tout ou partie du créneau est refusée.
- Recherche des salles disponibles pour un créneau donné.
- Consultation des réservations d'un client (salle, type, capacité, début, fin, durée).

**Interface**
- Navigation par menu : Accueil, Ajouter, Réserver, Afficher.
- Messages d'erreur et de confirmation pour chaque action.

## Installation

Prérequis : **Python 3.10 ou supérieur** (tkinter est fourni avec Python).

```bash
git clone https://github.com/EngS1/Projet_CEREN_SYLLA.git
cd Projet_CEREN_SYLLA
pip install -r requirements.txt
```

## Lancement

Depuis la racine du dépôt (le fichier `data.json` est lu dans le dossier courant) :

```bash
python src/gui.py
```

Sous Windows, on peut aussi double-cliquer sur `lancer_application.bat`.

## Structure du projet

```
Projet_CEREN_SYLLA
├── src
│   ├── gui.py            Interface graphique tkinter (menus, formulaires, calendrier, tableaux)
│   ├── main.py           Logique métier : clients, salles, réservations, disponibilité, validation, sauvegarde JSON
│   ├── controller.py     Validation et ajout d'un client
│   ├── model.py          Structure d'un client et accès aux données JSON
│   ├── database.py       Lecture et écriture de data.json
│   └── utils.py          Fonctions de chargement et de sauvegarde JSON
├── tests                 Tests unitaires (unittest / pytest)
├── data.json             Données de démonstration (clients, salles, réservations)
├── requirements.txt      Dépendances
├── pyproject.toml        Configuration du projet
└── lancer_application.bat  Lanceur Windows
```

## Données

Les données sont enregistrées dans `data.json` : liste des clients (avec compteur d'identifiants), des salles et des réservations (identifiant unique, client, salle, début, fin, durée). Le fichier fourni contient des exemples fictifs pour tester l'application immédiatement.

## Journalisation

Les actions importantes (chargement des données, ajout d'un client ou d'une salle, réservation) et les erreurs de saisie sont tracées dans la console avec horodatage et niveau (`INFO`, `WARNING`, `ERROR`).

## Auteurs

**Daouda SYLLA** — [GitHub](https://github.com/EngS1) · [LinkedIn](https://linkedin.com/in/sylla-daouda)
et **CEREN**, en binôme.
