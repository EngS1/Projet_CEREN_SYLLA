import uuid
import json
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import re


clients = []
rooms = []
bookings = []
client_id_counter = 0


"""Add a client to the database"""


def add_client(nom, prenom, email) -> dict:
    """Add a client to the database."""
    global clients, client_id_counter
    client_id = client_id_counter
    client = {"id": client_id, "nom": nom, "prenom": prenom, "email": email}
    clients.append(client)
    client_id_counter += 1
    return client


"""Add a room to the database"""


def add_room(nom_salle, type_salle, capacite) -> dict:
    nouvelle_salle = {
        "id": nom_salle,
        "nom": nom_salle,
        "type": type_salle,
        "capacite": capacite,
    }
    rooms.append(nouvelle_salle)
    return nouvelle_salle


"""Show available rooms"""


def display_available_rooms():
    return [salle for salle in rooms]


"""Reserve a room for a client"""


def book_room(client_id, salle_id, start_date, end_date, duration) -> dict:
    reservation_id = str(uuid.uuid4())
    reservation = {
        "id": reservation_id,
        "client_id": client_id,
        "salle_id": salle_id,
        "start_date": start_date,
        "end_date": end_date,
        "duration": duration,
    }
    bookings.append(reservation)
    return reservation


"""Show all bookings"""


def display_clients_bookings(client_id) -> list:
    return [
        res for res in bookings
        if (res["client_id"].split("'id': ")[1].split(",")[0]) == client_id
    ]


"""Show all bookings for a room"""

def check_room_availability(salle_id, start_date, end_date) -> bool:
    for res in bookings:
        # Extract the ID
        booked_salle_id = res["salle_id"].split(" - ")[0]
        if booked_salle_id == salle_id:
            res_start = datetime.strptime(res["start_date"], "%Y-%m-%d %H:%M:%S")
            res_end = datetime.strptime(res["end_date"], "%Y-%m-%d %H:%M:%S")


            if not (end_date <= res_start or start_date >= res_end):
                return False
    return True



"""Show available rooms for a specific time slot"""


def display_available_rooms_for_niche(start_date, end_date) -> list:
    """Return a list of available rooms for a specific time slot."""
    rooms_available = []
    for salle in rooms:
        if check_room_availability(salle["id"], start_date, end_date):
            rooms_available.append(salle)
    return rooms_available



"""Parse room information from a string"""


def parse_salle_info(salle_str):
    try:
        salle = salle_str.split(" - ")[0]
        type_salle = salle_str.split(" - ")[1].split(" (")[0]
        capacite_match = re.search(r"Capacit(?:é|e): (\d+)", salle_str)
        capacite = capacite_match.group(1) if capacite_match else ""
    except Exception:
        salle = type_salle = capacite = ""
    return salle, type_salle, capacite


"""Delete a reservation"""


def remove_client(client_id) -> str:
    global clients, bookings
    clients = [client for client in clients if client["id"] != client_id]
    bookings = [res for res in bookings if res["client_id"] != client_id]
    return f"Client {client_id} et ses réservations associées ont été supprimés."


"""Delete a room and its associated bookings"""


def remove_room(salle_id) -> str:
    global rooms, bookings
    rooms = [salle for salle in rooms if salle["id"] != salle_id]
    bookings = [res for res in bookings if res["salle_id"] != salle_id]
    return f"Salle {salle_id} et ses réservations associées ont été supprimées."


"""Display all registered clients"""


def display_clients() -> list:
    """Returns the list of clients from the JSON file."""
    # with open("data.json", "r") as file:
    #     data = json.load(file)
    # return data.get("clients", [])
    return [client for client in clients]


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


def validate_data(start_date, end_date) -> tuple:
    """Check if the start date is before the end date."""
    try:
        debut = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        fin = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
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


def main_function():
    """Main function of the application."""
    return "Application started"
