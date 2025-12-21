# Admin will be able to add or remove items from the inventory
# If some ingredient is out of stock, admin will be able to add it to the inventory
from uuid import uuid4
from app.models.inventory import Inventory
from app.observers.inventory.observer import InventoryObserver


class Admin(InventoryObserver):
    def __init__(self, name: str):
        InventoryObserver.__init__(self)
        self.admin_id = str(uuid4())
        self.name = name
        self.inventory = Inventory.get_instance()

    def get_admin_id(self) -> str:
        return self.admin_id

    def get_name(self) -> str:
        return self.name

    def add_item_to_inventory(self, item: str, quantity: int) -> None:
        self.inventory.add_item(item, quantity)

    def remove_item_from_inventory(self, item: str, quantity: int) -> None:
        self.inventory.remove_item(item, quantity)

    def get_inventory_status(self) -> dict:
        return self.inventory.get_status()

    # To notify the admin about the inventory status
    def update_inventory_status(self, item: str, quantity: int) -> None:
        print(f"Admin {self.name} received update about inventory status of {item} which is now {quantity}")
