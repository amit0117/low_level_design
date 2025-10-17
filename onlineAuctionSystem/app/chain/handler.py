from abc import ABC, abstractmethod


class AuctionHandler(ABC):
    @abstractmethod
    def handle(self, request):
        raise NotImplementedError("Handle method has not been implemented")

    @abstractmethod
    def set_next(self, handler: "AuctionHandler"):
        raise NotImplementedError("Set next method has not been implemented")


class BaseAuctionHandler(AuctionHandler):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return False


class ConcreteHandler1(Handler):
    def handle(self, request):
        print("ConcreteHandler1 handles the request")


class ConcreteHandler2(Handler):
    def handle(self, request):
        print("ConcreteHandler2 handles the request")
