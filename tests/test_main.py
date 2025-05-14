import pytest
from main import ajouter_client, ajouter_salle, reserver_salle, verifier_disponibilite_salle

def test_ajouter_client():
    client = ajouter_client("Jean Dupont", "jean.dupont@example.com")
    assert client["nom"] == "Jean Dupont"
    assert client["email"] == "jean.dupont@example.com"

def test_ajouter_salle():
    salle = ajouter_salle("Salle A", "standard", 4)
    assert salle["nom"] == "Salle A"
    assert salle["type"] == "standard"
    assert salle["capacite"] == 4

def test_verifier_disponibilite_salle():
    salle_id = "1"
    reserver_salle("client1", salle_id, "2025-05-01T10:00:00", "2025-05-01T12:00:00")
    assert not verifier_disponibilite_salle(salle_id, "2025-05-01T11:00:00", "2025-05-01T13:00:00")
    assert verifier_disponibilite_salle(salle_id, "2025-05-01T12:00:00", "2025-05-01T14:00:00")
