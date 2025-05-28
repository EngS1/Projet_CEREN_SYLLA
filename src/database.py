from src.utils import load_data, save_data

"""Managment of the database for the reservation system."""
FICHIER_BDD = "data.json"


def lire_bdd() -> dict:
    """Reads the database from the JSON file."""
    return load_data(FICHIER_BDD)


def ecrire_bdd(donnees: dict) -> None:
    """Writes the database to the JSON file."""
    save_data(FICHIER_BDD, donnees)


def get_clients() -> list:
    """Retrieve the list of clients from the database."""
    data = lire_bdd()  # Utilise la fonction `lire_bdd` pour lire les données
    return data.get("clients", [])
