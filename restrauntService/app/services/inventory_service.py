from app.repositories.inventory_repository import InventoryRepository
from app.repositories.menu_repository import MenuRepository
from app.models.item import Item
from app.exceptions.inventory import InsufficientStockException


class InventoryService:
    def __init__(self):
        self.inventory_repo = InventoryRepository()
        self.menu_repo = MenuRepository()

    def add_item_to_inventory(self, item: Item, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.inventory_repo.save_item(item, quantity)
        print(f"Added {quantity} units of {item.get_name()} to inventory")

    def remove_item_from_inventory(self, item: Item, quantity: int) -> None:
        current_quantity = self.inventory_repo.find_item_quantity(item)

        if current_quantity < quantity:
            raise InsufficientStockException(f"Not enough {item.get_name()} in inventory")

        self.inventory_repo.update_quantity(item, -quantity)
        print(f"Removed {quantity} units of {item.get_name()} from inventory")

    def check_item_availability(self, item: Item, required_quantity: int) -> bool:
        available_quantity = self.inventory_repo.find_item_quantity(item)
        return available_quantity >= required_quantity

    def get_inventory_status(self) -> dict:
        available_items = self.inventory_repo.find_available_items()
        out_of_stock_items = self.inventory_repo.find_out_of_stock_items()

        return {
            "total_items": len(available_items) + len(out_of_stock_items),
            "available_items": len(available_items),
            "out_of_stock_items": len(out_of_stock_items),
        }
