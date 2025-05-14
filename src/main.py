import uuid
import json
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


# Gestion des données
clients = []
salles = []
reservations = []
client_id_counter = 0  # Nouveau compteur pour les identifiants des clients

# Ajouter un client
def ajouter_client(nom, email):
    global clients, client_id_counter
    client_id = client_id_counter  # Utilise le compteur actuel comme ID
    client = {"id": client_id, "nom": nom, "email": email}
    clients.append(client)
    client_id_counter += 1  # Incrémente le compteur
    return client

# Ajouter une salle
def ajouter_salle(nom, type_salle, capacite):
    salle_id = str(uuid.uuid4())
    salle = {"id": salle_id, "nom": nom, "type": type_salle, "capacite": capacite}
    salles.append(salle)
    return salle

# Afficher les salles disponibles
def afficher_salles_disponibles():
    return [salle for salle in salles]

# Réserver une salle
def reserver_salle(client_id, salle_id, date_debut, date_fin):
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

# Afficher les réservations d'un client
def afficher_reservations_client(client_id):
    return [res for res in reservations if res["client_id"] == client_id]

# Vérifier la disponibilité d'une salle
def verifier_disponibilite_salle(salle_id, date_debut, date_fin):
    for res in reservations:
        if res["salle_id"] == salle_id and not (
            date_fin <= res["date_debut"] or date_debut >= res["date_fin"]
        ):
            return False
    return True

# Afficher les salles disponibles pour un créneau
def afficher_salles_disponibles_pour_creneau(date_debut, date_fin):
    salles_disponibles = []
    for salle in salles:
        if verifier_disponibilite_salle(salle["id"], date_debut, date_fin):
            salles_disponibles.append(salle)
    return salles_disponibles

# Supprimer un client
def supprimer_client(client_id):
    global clients, reservations
    clients = [client for client in clients if client["id"] != client_id]
    reservations = [res for res in reservations if res["client_id"] != client_id]
    return f"Client {client_id} et ses réservations associées ont été supprimés."

# Supprimer une salle
def supprimer_salle(salle_id):
    global salles, reservations
    salles = [salle for salle in salles if salle["id"] != salle_id]
    reservations = [res for res in reservations if res["salle_id"] != salle_id]
    return f"Salle {salle_id} et ses réservations associées ont été supprimées."

# Charger les données depuis un fichier JSON
def charger_donnees(fichier):
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

# Sauvegarder les données dans un fichier JSON
def sauvegarder_donnees(fichier):
    data = {
        "client_id_counter": client_id_counter,
        "clients": clients,
        "salles": salles,
        "reservations": reservations
    }
    with open(fichier, "w") as f:
        json.dump(data, f, indent=4)

# Valider les données d'entrée
def valider_donnees(date_debut, date_fin):
    try:
        debut = datetime.strptime(date_debut, "%Y-%m-%dT%H:%M:%S")
        fin = datetime.strptime(date_fin, "%Y-%m-%dT%H:%M:%S")
        if debut >= fin:
            return False, "La date de début doit être antérieure à la date de fin."
        return True, None
    except ValueError:
        return False, "Format de date invalide. Utilisez le format YYYY-MM-DD HH:MM:SS."

# Fonction pour vérifier la validité de l'email
def verifier_email(email):
    try:
        # Valider et normaliser l'email
        v = validate_email(email)
        return True, v.email  # Retourne True et l'email normalisé
    except EmailNotValidError:
        return False, "Email non valide"  # Retourne False et le message d'erreur

