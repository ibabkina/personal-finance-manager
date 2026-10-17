# apply_transaction_command.py

from command.command import Command
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class ApplyTransactionCommand(Command):
    """Concrete command: apply one transaction to a balance, and undo it again."""

    def __init__(self, balance, transaction):
        """The balance is injected (dependency injection), so any balance-like object can be used."""
        self.balance = balance
        self.transaction = transaction

    def execute(self):
        """Apply the transaction to the balance."""
        self.balance.apply_transaction(self.transaction)

    def undo(self):
        """Apply the opposite transaction, which puts the balance back."""
        if self.transaction.category == TransactionCategory.INCOME:
            opposite = TransactionCategory.EXPENSE
        else:
            opposite = TransactionCategory.INCOME
        self.balance.apply_transaction(Transaction(self.transaction.amount, opposite))
