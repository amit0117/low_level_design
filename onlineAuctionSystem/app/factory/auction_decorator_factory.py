from app.decorators.bid_place_checker_decorator import (
    AuctionValidator,
    ConcreteAuctionValidator,
    OwnerCheckDecorator,
    FraudDetectionDecorator,
)


class AuctionDecoratorFactory:
    @staticmethod
    def create_default_validator() -> AuctionValidator:
        return FraudDetectionDecorator(OwnerCheckDecorator(ConcreteAuctionValidator()))

    @staticmethod
    def create_minimal_validator() -> AuctionValidator:
        return ConcreteAuctionValidator()

    @staticmethod
    def create_fraud_protection_validator() -> AuctionValidator:
        return FraudDetectionDecorator(ConcreteAuctionValidator())

    @staticmethod
    def create_owner_protection_validator() -> AuctionValidator:
        return OwnerCheckDecorator(ConcreteAuctionValidator())

    @staticmethod
    def create_custom_validator(*decorators) -> AuctionValidator:
        validator = ConcreteAuctionValidator()

        for decorator_class in reversed(decorators):
            validator = decorator_class(validator)

        return validator
