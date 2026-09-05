import json
from pathlib import Path


MENU_DIR = Path("data/menu")


def load_menu() -> list[dict]:
    """Load every menu item from the JSON menu files."""

    menu = []

    for file_path in sorted(MENU_DIR.glob("*.json")):
        with open(file_path, "r", encoding="utf-8") as file:
            items = json.load(file)

        menu.extend(items)

    return menu


def get_menu_item(item_id: str) -> dict | None:
    """Find a menu item by ID."""

    for item in load_menu():
        if item["id"] == item_id:
            return item

    return None


def get_categories() -> list[str]:
    """Return available menu categories."""

    categories = {
        item["category"]
        for item in load_menu()
    }

    return sorted(categories)