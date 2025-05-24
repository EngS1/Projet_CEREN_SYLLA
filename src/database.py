from utils import charger_donnees, sauvegarder_donnees

"""Managment of the database for the reservation system."""
FICHIER_BDD = "data/database.json"


def lire_bdd() -> dict:
    """Reads the database from the JSON file."""
    return charger_donnees(FICHIER_BDD)


def ecrire_bdd(donnees) -> None:
    """Writes the database to the JSON file."""
    sauvegarder_donnees(FICHIER_BDD, donnees)
