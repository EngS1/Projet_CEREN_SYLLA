import unittest
from tkinter import Tk
from src.gui import menu_principal


class TestGUI(unittest.TestCase):
    def setUp(self):
        """Set up the GUI for testing."""
        self.root = Tk()  # Initialisez root avant d'appeler menu_principal
        menu_principal(self.root)  # Passez root comme argument

    def tearDown(self):
        """Destroy the GUI after testing."""
        self.root.destroy()

    def test_window_title(self):
        """Test if the window title is correctly set."""
        self.assertEqual(self.root.title(), "MeetingPro - Gestion des Réservations")


if __name__ == "__main__":
    unittest.main()
