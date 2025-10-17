from app.decorators.bid_place_checker_decorator import AuctionDecorator, BaseAuctionDetector, OwnerCheckDecorator, FraudDetectionDecorator


class AuctionDecoratorFactory:
    @staticmethod
    def create_bid_place_checker_decorator() -> AuctionDecorator:
        return BaseAuctionDetector(OwnerCheckDecorator(FraudDetectionDecorator()))
