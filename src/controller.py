from model import ajouter_client


def valider_et_ajouter_client(prenom, nom, email):
    """Valide les données et ajoute un client."""
    if not prenom.isalpha():
        return "Erreur : Le prénom doit contenir uniquement des lettres."
    if not nom.isalpha():
        return "Erreur : Le nom doit contenir uniquement des lettres."
    if "@" not in email or "." not in email:
        return "Erreur : Adresse email incorrecte."

    # Ajouter le client via le modèle
    client = ajouter_client(prenom, nom, email)
    return f"Client ajouté avec succès : {client}"
