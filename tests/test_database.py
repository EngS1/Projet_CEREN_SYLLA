import unittest
from src.database import get_clients  # Exemple de fonction à tester


class TestDatabase(unittest.TestCase):
    def test_get_clients(self):
        """Test the function that retrieves clients from the database."""
        clients = get_clients()
        self.assertIsInstance(
            clients, list
        )  # Vérifiez que la fonction retourne une liste
        self.assertGreater(len(clients), 0)  # Vérifiez que la liste n'est pas vide


if __name__ == "__main__":
    unittest.main()
