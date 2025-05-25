import uuid
import json
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


"""Database managment"""
clients = []
rooms = []
bookings = []
client_id_counter = 0


"""Initialisation de la base de données"""


def add_client(nom, prenom, email) -> dict:
    """Add a client to the database."""
    global clients, client_id_counter
    client_id = client_id_counter  # Utilise le compteur actuel comme ID
    client = {"id": client_id, "nom": nom, "prenom": prenom, "email": email}
    clients.append(client)
    client_id_counter += 1  # Incrémente le compteur
    return client


"""Add a room to the database"""


def add_room(nom_salle, type_salle, capacite) -> dict:
    nouvelle_salle = {
        "id": nom_salle,  # L'ID est identique au nom
        "nom": nom_salle,
        "type": type_salle,
        "capacite": capacite,
    }
    rooms.append(nouvelle_salle)
    return nouvelle_salle


"""Show available rooms"""


def show_available_rooms():
    return [salle for salle in rooms]


"""Reserve a room for a client"""


def book_room(client_id, salle_id, date_debut, date_fin) -> dict:
    reservation_id = str(uuid.uuid4())
    reservation = {
        "id": reservation_id,
        "client_id": client_id,
        "salle_id": salle_id,
        "date_debut": date_debut,
        "date_fin": date_fin,
    }
    bookings.append(reservation)
    return reservation


"""Show all bookings"""


def show_clients_bookings(client_id) -> list:
    return [res for res in bookings if res["client_id"] == client_id]


"""Show all bookings for a room"""


def verifier_disponibilite_salle(salle_id, date_debut, date_fin) -> bool:
    """Check if a room is available for a given time slot."""
    for res in bookings:
        if res["salle_id"] == salle_id and not (
            date_fin <= res["date_debut"] or date_debut >= res["date_fin"]
        ):
            return False
    return True


"""Show available rooms for a specific time slot"""


def show_available_rooms_for_niche(date_debut, date_fin) -> list:
    """Return a list of available rooms for a specific time slot."""
    rooms_disponibles = []
    for salle in rooms:
        if verifier_disponibilite_salle(salle["id"], date_debut, date_fin):
            rooms_disponibles.append(salle)
    return rooms_disponibles


"""Delete a reservation"""


def supprimer_client(client_id) -> str:
    global clients, bookings
    clients = [client for client in clients if client["id"] != client_id]
    bookings = [res for res in bookings if res["client_id"] != client_id]
    return f"Client {client_id} et ses réservations associées ont été supprimés."


"""Delete a room and its associated bookings"""


def supprimer_salle(salle_id) -> str:
    global rooms, bookings
    rooms = [salle for salle in rooms if salle["id"] != salle_id]
    bookings = [res for res in bookings if res["salle_id"] != salle_id]
    return f"Salle {salle_id} et ses réservations associées ont été supprimées."


"""Display all registered clients"""


def show_clients() -> list:
    """Return a list of all registered clients."""
    return [(client["nom"], client["prenom"]) for client in clients]


"""Display all registered rooms"""


def load_data(fichier) -> None:
    """Load data from a JSON file."""
    global clients, rooms, bookings, client_id_counter
    try:
        with open(fichier, "r") as f:
            data = json.load(f)
            clients = data.get("clients", [])
            rooms = data.get("rooms", [])
            bookings = data.get("bookings", [])
            client_id_counter = data.get("client_id_counter", 0)
    except FileNotFoundError:
        clients, rooms, bookings = [], [], []
        client_id_counter = 0


"""Save data to a JSON file."""


def save_data(fichier):
    data = {
        "client_id_counter": client_id_counter,
        "clients": clients,
        "rooms": rooms,
        "bookings": bookings,
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


def check_email(email):
    try:
        """Validate and normalize an email address."""
        v = validate_email(email)
        return True, v.email
    except EmailNotValidError:
        return False, "Email non valide"
