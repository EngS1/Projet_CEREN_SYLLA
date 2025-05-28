import unittest
from src.controller import load_available_rooms  # Exemple de fonction à tester


class TestController(unittest.TestCase):
    def test_load_available_rooms(self):
        """Test the function that loads available rooms."""
        start_date = "2025-05-28 10:00:00"
        end_date = "2025-05-28 12:00:00"
        rooms = load_available_rooms(start_date, end_date)
        self.assertIsInstance(
            rooms, list
        )  # Vérifiez que la fonction retourne une liste


if __name__ == "__main__":
    unittest.main()
