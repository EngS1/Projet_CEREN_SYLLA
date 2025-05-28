from model import add_client

"""Controller for managing clients in the application."""


def valider_et_add_client(prenom, nom, email) -> str:
    """Validate the client data and add the client."""
    if not prenom.isalpha():
        return "Erreur : Le prénom doit contenir uniquement des lettres."
    if not nom.isalpha():
        return "Erreur : Le nom doit contenir uniquement des lettres."
    if "@" not in email or "." not in email:
        return "Erreur : Adresse email incorrecte."

    """Add a new client to the database."""
    client = add_client(prenom, nom, email)
    return f"Client ajouté avec succès : {client}"


"""Load available rooms based on the given date range."""


def load_available_rooms(start_date: str, end_date: str) -> list:
    """Load available rooms based on the given date range."""
    """Return a list of available rooms for the specified date range."""
    rooms = [
        {"id": "Room1", "type": "Standard", "capacite": 4},
        {"id": "Room2", "type": "Conférence", "capacite": 12},
    ]

    return rooms
