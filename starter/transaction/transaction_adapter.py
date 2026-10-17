# transaction_adapter.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TransactionAdapter:
    """Adapter: lets an external freelance income record be used as a normal Transaction."""

    def __init__(self, external_transaction):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external transaction to a standard Transaction."""
        # External freelance income is always income; the invoice ID and
        # description are not needed by the Transaction class.
        return Transaction(self.external_transaction.amount, TransactionCategory.INCOME)
