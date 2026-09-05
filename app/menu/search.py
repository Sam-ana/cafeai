from app.menu.loader import load_menu


def search_menu(query: str) -> list[dict]:
    """Search the menu using simple keyword matching."""

    query = query.lower().strip()

    if not query:
        return load_menu()

    results = []

    for item in load_menu():
        searchable_text = " ".join(
            [
                item["name"],
                item["category"],
                item["description"],
                *item.get("tags", []),
            ]
        ).lower()

        if query in searchable_text:
            results.append(item)

    return results


def get_items_by_category(category: str) -> list[dict]:
    """Return all items in a category."""

    return [
        item
        for item in load_menu()
        if item["category"].lower() == category.lower()
    ]