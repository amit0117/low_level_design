from typing import List, Optional
from app.repositories.menu_repository import MenuRepository
from app.models.item import Item


class MenuService:
    def __init__(self):
        self.menu_repo = MenuRepository()

    def add_item_to_menu(self, item: Item) -> None:
        if not item or not item.get_name():
            raise ValueError("Invalid item")

        self.menu_repo.save_item(item)
        print(f"Added {item.get_name()} to menu")

    def remove_item_from_menu(self, item: Item) -> None:
        if not item:
            raise ValueError("Invalid item")

        self.menu_repo.delete_item(item)
        print(f"Removed {item.get_name()} from menu")

    def get_all_items(self) -> List[Item]:
        return self.menu_repo.find_all_items()

    def find_item_by_name(self, name: str) -> Optional[Item]:
        return self.menu_repo.find_item_by_name(name)

    def get_veg_items(self) -> List[Item]:
        return self.menu_repo.find_veg_items()

    def get_non_veg_items(self) -> List[Item]:
        return self.menu_repo.find_non_veg_items()

    def get_menu_status(self) -> dict:
        all_items = self.menu_repo.find_all_items()
        veg_items = self.menu_repo.find_veg_items()
        non_veg_items = self.menu_repo.find_non_veg_items()

        return {"total_items": len(all_items), "veg_items": len(veg_items), "non_veg_items": len(non_veg_items)}
