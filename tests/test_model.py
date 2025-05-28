import pytest
import unittest
from src.model import Client  # Exemple de classe à tester


class TestModel(unittest.TestCase):
    def test_client_creation(self):
        """Test the creation of a Client object."""
        client = Client(id=1, nom="John", prenom="Doe", email="john.doe@example.com")
        self.assertEqual(client.nom, "John")
        self.assertEqual(client.prenom, "Doe")
        self.assertEqual(client.email, "john.doe@example.com")


if __name__ == "__main__":
    unittest.main()
