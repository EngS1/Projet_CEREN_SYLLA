import uuid
import json
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


"""Database managment"""
clients = []
salles = []
reservations = []
client_id_counter = 0


"""Initialisation de la base de données"""


def ajouter_client(nom, prenom, email) -> dict:
    """Add a client to the database."""
    global clients, client_id_counter
    client_id = client_id_counter  # Utilise le compteur actuel comme ID
    client = {"id": client_id, "nom": nom, "prenom": prenom, "email": email}
    clients.append(client)
    client_id_counter += 1  # Incrémente le compteur
    return client


"""Add a room to the database"""


def ajouter_salle(nom_salle, type_salle, capacite) -> dict:
    nouvelle_salle = {
        "id": nom_salle,  # L'ID est identique au nom
        "nom": nom_salle,
        "type": type_salle,
        "capacite": capacite,
    }
    salles.append(nouvelle_salle)
    return nouvelle_salle


"""Show available rooms"""


def afficher_salles_disponibles():
    return [salle for salle in salles]


"""Reserve a room for a client"""


def reserver_salle(client_id, salle_id, date_debut, date_fin) -> dict:
    reservation_id = str(uuid.uuid4())
    reservation = {
        "id": reservation_id,
        "client_id": client_id,
        "salle_id": salle_id,
        "date_debut": date_debut,
        "date_fin": date_fin,
    }
    reservations.append(reservation)
    return reservation


"""Show all reservations"""


def afficher_reservations_client(client_id) -> list:
    return [res for res in reservations if res["client_id"] == client_id]


"""Show all reservations for a room"""


def verifier_disponibilite_salle(salle_id, date_debut, date_fin) -> bool:
    """Check if a room is available for a given time slot."""
    for res in reservations:
        if res["salle_id"] == salle_id and not (
            date_fin <= res["date_debut"] or date_debut >= res["date_fin"]
        ):
            return False
    return True


"""Show available rooms for a specific time slot"""


def afficher_salles_disponibles_pour_creneau(date_debut, date_fin) -> list:
    """Return a list of available rooms for a specific time slot."""
    salles_disponibles = []
    for salle in salles:
        if verifier_disponibilite_salle(salle["id"], date_debut, date_fin):
            salles_disponibles.append(salle)
    return salles_disponibles


"""Delete a reservation"""


def supprimer_client(client_id) -> str:
    global clients, reservations
    clients = [client for client in clients if client["id"] != client_id]
    reservations = [res for res in reservations if res["client_id"] != client_id]
    return f"Client {client_id} et ses réservations associées ont été supprimés."


"""Delete a room and its associated reservations"""


def supprimer_salle(salle_id) -> str:
    global salles, reservations
    salles = [salle for salle in salles if salle["id"] != salle_id]
    reservations = [res for res in reservations if res["salle_id"] != salle_id]
    return f"Salle {salle_id} et ses réservations associées ont été supprimées."


"""Display all registered clients"""


def afficher_clients() -> list:
    """Return a list of all registered clients."""
    return [(client["nom"], client["prenom"]) for client in clients]


"""Display all registered rooms"""


def charger_donnees(fichier) -> None:
    """Load data from a JSON file."""
    global clients, salles, reservations, client_id_counter
    try:
        with open(fichier, "r") as f:
            data = json.load(f)
            clients = data.get("clients", [])
            salles = data.get("salles", [])
            reservations = data.get("reservations", [])
            client_id_counter = data.get("client_id_counter", 0)
    except FileNotFoundError:
        clients, salles, reservations = [], [], []
        client_id_counter = 0


"""Save data to a JSON file."""


def sauvegarder_donnees(fichier):
    data = {
        "client_id_counter": client_id_counter,
        "clients": clients,
        "salles": salles,
        "reservations": reservations,
    }
    with open(fichier, "w") as f:
        json.dump(data, f, indent=4)


"""Validate start and end dates for a reservation"""


def valider_donnees(date_debut, date_fin) -> tuple:
    """Check if the start date is before the end date."""
    try:
        debut = datetime.strptime(date_debut, "%Y-%m-%dT%H:%M:%S")
        fin = datetime.strptime(date_fin, "%Y-%m-%dT%H:%M:%S")
        if debut >= fin:
            return False, "La date de début doit être antérieure à la date de fin."
        return True, None
    except ValueError:
        return False, "Format de date invalide. Utilisez le format YYYY-MM-DD HH:MM:SS."


"""Validate and normalize an email address"""


def verifier_email(email):
    try:
        """Validate and normalize an email address."""
        v = validate_email(email)
        return True, v.email
    except EmailNotValidError:
        return False, "Email non valide"
