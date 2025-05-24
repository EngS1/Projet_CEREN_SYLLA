import json

FICHIER_DONNEES = "data.json"


def charger_donnees():
    """Load data from the JSON file."""
    with open(FICHIER_DONNEES, "r") as f:
        return json.load(f)


def sauvegarder_donnees(data):
    """Save data to the JSON file."""
    with open(FICHIER_DONNEES, "w") as f:
        json.dump(data, f, indent=4)


def ajouter_client(prenom, nom, email):
    """Add a new client to the database."""
    data = charger_donnees()
    client_id = data["client_id_counter"] + 1
    nouveau_client = {"id": client_id, "prenom": prenom, "nom": nom, "email": email}
    data["clients"].append(nouveau_client)
    data["client_id_counter"] = client_id
    sauvegarder_donnees(data)
    return nouveau_client
