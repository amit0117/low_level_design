from app.abstract_factories.abstract_bank_factory import BankIntegrationFactory
from app.abstract_factories.hdfc_products import HDFCConnector, HDFCAuthHandler, HDFCTransactionFormatter, HDFCNotificationAdapter
from app.abstract_factories.sbi_products import SBIConnector, SBIAuthHandler, SBITransactionFormatter, SBINotificationAdapter


class HDFCFactory(BankIntegrationFactory):
    def create_connector(self):
        return HDFCConnector()

    def create_auth_handler(self):
        return HDFCAuthHandler()

    def create_formatter(self):
        return HDFCTransactionFormatter()

    def create_notifier(self):
        return HDFCNotificationAdapter()


class SBIFactory(BankIntegrationFactory):
    def create_connector(self):
        return SBIConnector()

    def create_auth_handler(self):
        return SBIAuthHandler()

    def create_formatter(self):
        return SBITransactionFormatter()

    def create_notifier(self):
        return SBINotificationAdapter()
