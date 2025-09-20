from app.models.cart_item import CartItem
from app.models.product import Product


class ShoppingCart:
    def __init__(self) -> None:
        self.items: list[CartItem] = []

    def add_item(self, product: Product, quantity: int) -> None:
        for item in self.items:
            if item.get_product() == product:
                item.increment_quantity(quantity)
                break
        else:
            self.items.append(CartItem(product, quantity))

    def remove_item(self, product: Product, quantity: int = 1) -> None:
        item_found = False
        for item in self.items:
            if item.get_product() == product:
                item.decrement_quantity(quantity)
                if item.get_quantity() == 0:
                    self.items.remove(item)
                    item_found = True
                    break

        if not item_found:
            print(f"Item {product.get_name()} not found in the shopping cart")

    def clear(self):
        print(f"Clearing the shopping cart")
        self.items.clear()

    def get_items(self) -> list[CartItem]:
        return self.items

    def get_total(self) -> float:
        return sum(item.get_price() for item in self.items)

    def __repr__(self) -> str:
        return f"ShoppingCart(items={self.items})"
