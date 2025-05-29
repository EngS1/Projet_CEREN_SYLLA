import unittest
from src.database import get_clients


class TestDatabase(unittest.TestCase):
    def test_get_clients(self):
        """Test the function that retrieves clients from the database."""
        clients = get_clients()
        self.assertIsInstance(clients, list)
        self.assertGreaterEqual(len(clients), 0)


if __name__ == "__main__":
    unittest.main()
