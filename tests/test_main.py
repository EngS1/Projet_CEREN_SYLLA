import unittest
from src.main import (
    main_function,
)  # Remplacez par la fonction principale de votre application


class TestMain(unittest.TestCase):
    def test_main_function(self):
        """Test the main function."""
        result = main_function()
        self.assertIsNotNone(
            result
        )  # Vérifiez que la fonction retourne un résultat valide


if __name__ == "__main__":
    unittest.main()
