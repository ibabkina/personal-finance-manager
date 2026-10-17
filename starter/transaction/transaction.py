# transaction.py

from transaction.transaction_category import TransactionCategory


class Transaction:
    """Represents a financial transaction with an amount and category."""

    def __init__(self, amount, category: TransactionCategory):
        self.amount = amount
        self.category = category

    def __str__(self):
        """Readable text, e.g. Transaction($50, category='TransactionCategory.INCOME')."""
        return f"Transaction(${self.amount}, category='{self.category}')"

    def __eq__(self, other):
        """Two transactions are equal when amount and category are the same."""
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.amount == other.amount and self.category == other.category
