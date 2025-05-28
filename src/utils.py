import json


def load_data(file_path: str) -> dict:
    """Load data from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)


def save_data(file_path: str, data: dict) -> None:
    """Save data to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
