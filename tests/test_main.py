import pytest
from main import add_client, add_room, book_room, check_room_availability


def test_add_client():
    client = add_client("Jean Dupont", "jean.dupont@example.com")
    assert client["nom"] == "Jean Dupont"
    assert client["email"] == "jean.dupont@example.com"


def test_add_room():
    salle = add_room("Salle A", "standard", 4)
    assert salle["nom"] == "Salle A"
    assert salle["type"] == "standard"
    assert salle["capacite"] == 4


def test_check_room_availability():
    salle_id = "1"
    book_room("client1", salle_id, "2025-05-01T10:00:00", "2025-05-01T12:00:00")
    assert not check_room_availability(
        salle_id, "2025-05-01T11:00:00", "2025-05-01T13:00:00"
    )
    assert check_room_availability(
        salle_id, "2025-05-01T12:00:00", "2025-05-01T14:00:00"
    )
