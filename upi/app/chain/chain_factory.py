from app.chain.base_handler import PaymentHandler
from app.chain.validation_handler import ValidationHandler
from app.chain.authentication_handler import AuthenticationHandler
from app.chain.fraud_handler import FraudHandler
from app.chain.routing_handler import RoutingHandler
from app.chain.settlement_handler import SettlementHandler


class PaymentChainFactory:
    """Factory to create payment processing chains"""

    @staticmethod
    def create_full_chain() -> PaymentHandler:
        """Create complete payment processing chain"""

        # Create handlers
        validation = ValidationHandler()
        authentication = AuthenticationHandler()
        fraud = FraudHandler()
        routing = RoutingHandler()
        settlement = SettlementHandler()

        # Build chain: validation → authentication → fraud → routing → settlement
        validation.set_next(authentication).set_next(fraud).set_next(routing).set_next(settlement)

        return validation

    @staticmethod
    def create_basic_chain() -> PaymentHandler:
        """Create basic payment processing chain (validation + routing)"""

        validation = ValidationHandler()
        routing = RoutingHandler()

        validation.set_next(routing)

        return validation

    @staticmethod
    def create_secure_chain() -> PaymentHandler:
        """Create secure payment processing chain (validation + auth + fraud + routing)"""

        validation = ValidationHandler()
        authentication = AuthenticationHandler()
        fraud = FraudHandler()
        routing = RoutingHandler()

        validation.set_next(authentication).set_next(fraud).set_next(routing)

        return validation

    @staticmethod
    def create_custom_chain(*handler_types: str) -> PaymentHandler:
        """Create custom chain with specified handlers"""

        handler_map = {
            "validation": ValidationHandler,
            "authentication": AuthenticationHandler,
            "fraud": FraudHandler,
            "routing": RoutingHandler,
            "settlement": SettlementHandler,
        }

        if not handler_types:
            raise ValueError("At least one handler type must be specified")

        # Create handlers
        handlers = []
        for handler_type in handler_types:
            if handler_type not in handler_map:
                raise ValueError(f"Unknown handler type: {handler_type}")
            handlers.append(handler_map[handler_type]())

        # Build chain
        for i in range(len(handlers) - 1):
            handlers[i].set_next(handlers[i + 1])

        return handlers[0]
