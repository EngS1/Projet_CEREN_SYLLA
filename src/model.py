import json

FILE_DATA = "data.json"


def load_data():
    """Load data from the JSON file."""
    with open(FILE_DATA, "r") as f:
        return json.load(f)


def save_data(data):
    """Save data to the JSON file."""
    with open(FILE_DATA, "w") as f:
        json.dump(data, f, indent=4)


def add_client(prenom, nom, email):
    """Add a new client to the database."""
    data = load_data()
    client_id = data["client_id_counter"] + 1
    nouveau_client = {"id": client_id, "prenom": prenom, "nom": nom, "email": email}
    data["clients"].append(nouveau_client)
    data["client_id_counter"] = client_id
    save_data(data)
    return nouveau_client


class Client:
    """Represents a client in the system."""

    def __init__(self, id: int, nom: str, prenom: str, email: str):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
