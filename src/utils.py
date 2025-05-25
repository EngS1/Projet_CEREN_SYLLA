from datetime import datetime
import json


# Validation des données
def valider_date(date_str):
    """
    Valide si une chaîne de caractères est au format YYYY-MM-DDTHH:MM:SS.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False


# Recherche d'entités
def trouver_client_par_id(client_id, clients):
    """
    Recherche un client par son identifiant.
    """
    for client in clients:
        if client["id"] == int(client_id):
            return client
    return None


def trouver_salle_par_id(salle_id, rooms):
    """
    Recherche une salle par son identifiant.
    """
    for salle in rooms:
        if salle["id"] == salle_id:
            return salle
    return None


# Génération d'identifiants uniques
def generer_id_unique(liste, champ_id="id"):
    """
    Génère un identifiant unique basé sur les éléments existants dans une liste.
    """
    if not liste:
        return 0
    return max(item[champ_id] for item in liste) + 1


# Gestion des fichiers JSON
def charger_fichier_json(fichier):
    """
    Charge les données depuis un fichier JSON.
    """
    try:
        with open(fichier, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def sauvegarder_fichier_json(fichier, donnees):
    """
    Sauvegarde les données dans un fichier JSON.
    """
    with open(fichier, "w") as f:
        json.dump(donnees, f, indent=4)


# Vérification de disponibilité
def verifier_disponibilite_salle(salle_id, date_debut, date_fin, bookings):
    """
    Vérifie si une salle est disponible pour un créneau donné.
    """
    for res in bookings:
        if res["salle_id"] == salle_id and not (
            date_fin <= res["date_debut"] or date_debut >= res["date_fin"]
        ):
            return False
    return True


def load_data(fichier):
    try:
        with open(fichier, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"clients": [], "rooms": [], "bookings": []}


def save_data(fichier, donnees):
    with open(fichier, "w") as f:
        json.dump(donnees, f, indent=4)
