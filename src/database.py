from utils import load_data, save_data

"""Managment of the database for the reservation system."""
FICHIER_BDD = "data/database.json"


def lire_bdd() -> dict:
    """Reads the database from the JSON file."""
    return load_data(FICHIER_BDD)


def ecrire_bdd(donnees) -> None:
    """Writes the database to the JSON file."""
    save_data(FICHIER_BDD, donnees)
