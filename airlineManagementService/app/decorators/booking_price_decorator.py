from abc import ABC, abstractmethod

# Since booking entity has a get_price method, we need to create a price component interface to wrap the booking price


class PriceComponent(ABC):
    @abstractmethod
    def get_price(self) -> float:
        raise NotImplementedError("Subclasses must implement this method")


class BaseBookingPrice(PriceComponent):
    """Concrete implementation for base booking price"""

    def __init__(self, base_price: float):
        self.base_price = base_price

    def get_price(self) -> float:
        return self.base_price


class PriceDecorator(PriceComponent):
    def __init__(self, price_component: PriceComponent):
        self.price_component = price_component

    def get_price(self) -> float:
        return self.price_component.get_price()


class TaxDecorator(PriceDecorator):
    def __init__(self, price_component: PriceComponent, tax_rate: float):
        super().__init__(price_component)
        self.tax_rate = tax_rate

    def get_price(self) -> float:
        return self.price_component.get_price() * (1 + self.tax_rate)


class ServiceChargeDecorator(PriceDecorator):
    def __init__(self, price_component: PriceComponent, service_charge: float):
        super().__init__(price_component)
        self.service_charge = service_charge

    def get_price(self) -> float:
        return self.price_component.get_price() + self.service_charge


class BaggageFeeDecorator(PriceDecorator):
    def __init__(self, price_component: PriceComponent, baggage_fee: float):
        super().__init__(price_component)
        self.baggage_fee = baggage_fee

    def get_price(self) -> float:
        return self.price_component.get_price() + self.baggage_fee


class CancellationFeeDecorator(PriceDecorator):
    # only if the booking is cancelled
    def __init__(self, price_component: PriceComponent, cancellation_fee: float):
        super().__init__(price_component)
        self.cancellation_fee = cancellation_fee

    def get_price(self) -> float:
        return self.price_component.get_price() + self.cancellation_fee


class DiscountDecorator(PriceDecorator):
    def __init__(self, price_component: PriceComponent, discount_percentage: float):
        super().__init__(price_component)
        self.discount_percentage = discount_percentage

    def get_price(self) -> float:
        return self.price_component.get_price() * (1 - self.discount_percentage)


class AirPortFeeDecorator(PriceDecorator):
    def __init__(self, price_component: PriceComponent, airport_fee: float):
        super().__init__(price_component)
        self.airport_fee = airport_fee

    def get_price(self) -> float:
        return self.price_component.get_price() + self.airport_fee
