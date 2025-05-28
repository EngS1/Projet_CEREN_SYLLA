import unittest
import pytest
import json
import os
from src.main import main_function, display_clients, load_data

"""Test suite for the main application."""
clients = []


class TestMain(unittest.TestCase):
    def test_main_function(self):
        """Test the main function."""
        result = main_function()
        self.assertIsNotNone(result)
        self.assertEqual(result, "Application started")


def test_load_data():
    """Test the load_data function."""
    global clients, rooms, bookings, client_id_counter
    test_file = "test_data.json"
    test_data = {
        "clients": [{"nom": "John", "prenom": "Doe"}],
        "rooms": [],
        "bookings": [],
        "client_id_counter": 1,
    }

    with open(test_file, "w") as f:
        json.dump(test_data, f)

    load_data(test_file)

    assert clients == test_data["clients"]
    assert rooms == test_data["rooms"]
    assert bookings == test_data["bookings"]
    assert client_id_counter == test_data["client_id_counter"]

    os.remove(test_file)


def test_display_clients():
    """Test the display_clients function."""
    global clients
    clients = [
        {"id": "1", "nom": "John", "prenom": "Doe", "email": "doe@gmail.com"},
        {"id": "2", "nom": "Jane", "prenom": "Smith", "email": "aaaa@gmail.com"},
    ]
    result = display_clients()
    assert result == [("John", "Doe"), ("Jane", "Smith")]


if __name__ == "__main__":
    unittest.main()
    pytest.main(["-v", __file__])
