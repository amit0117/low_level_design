from app.models.order_item import OrderItem


class BillDecorator:
    def __init__(self, order_item: OrderItem) -> None:
        self.order_item = order_item

    def get_subtotal(self) -> float:
        return self.order_item.get_subtotal()

    def get_description(self) -> str:
        return self.order_item.get_item().get_name()


class TaxDecorator(BillDecorator):
    def __init__(self, order_item: OrderItem, tax_rate: float) -> None:
        self.tax_rate = tax_rate
        super().__init__(order_item)

    def get_subtotal(self) -> float:
        return (1 + self.tax_rate) * super().get_subtotal()

    def get_description(self) -> str:
        return super().get_description() + ", Tax @" + (self.tax_rate * 100) + "%"


class DiscountDecorator(BillDecorator):
    def __init__(self, order_item: OrderItem, discount_percentage: float) -> None:
        self.discount_percentage = discount_percentage
        super().__init__(order_item)

    def get_subtotal(self) -> float:
        return ((100 - self.discount_percentage) / 100) * super().get_subtotal()

    def get_description(self) -> str:
        return super().get_description() + ", Discount @" + (self.discount_percentage) + "%"


class ServiceChargeDecorator(BillDecorator):
    def __init__(self, order_item: OrderItem, service_charge: float) -> None:
        self.service_charge = service_charge
        super().__init__(order_item)

    def get_subtotal(self) -> float:
        return self.service_charge + super().get_subtotal()

    def get_description(self) -> str:
        return super().get_description() + ", Service Charge ₹" + (self.service_charge)
