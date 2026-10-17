import unittest
from balance.balance import Balance
from command.apply_transaction_command import ApplyTransactionCommand
from command.command_manager import CommandManager
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class FakeBalance:
    """Stand-in balance that only records what it was asked to apply (shows dependency injection)."""

    def __init__(self):
        self.applied = []

    def apply_transaction(self, transaction):
        self.applied.append(transaction)


class TestApplyTransactionCommand(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_execute_applies_transaction(self):
        command = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        command.execute()
        self.assertEqual(self.balance.get_balance(), 100)

    def test_undo_reverses_income(self):
        command = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        command.execute()
        command.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_reverses_expense(self):
        command = ApplyTransactionCommand(self.balance, Transaction(40, TransactionCategory.EXPENSE))
        command.execute()
        command.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_command_uses_injected_balance(self):
        fake = FakeBalance()
        transaction = Transaction(25, TransactionCategory.EXPENSE)
        ApplyTransactionCommand(fake, transaction).execute()
        self.assertEqual(fake.applied, [transaction])


class TestCommandManager(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.manager = CommandManager()

    def test_undo_last_reverts_only_the_last_transaction(self):
        self.manager.execute_command(
            ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME)))
        self.manager.execute_command(
            ApplyTransactionCommand(self.balance, Transaction(30, TransactionCategory.EXPENSE)))
        self.assertEqual(self.balance.get_balance(), 70)

        self.assertTrue(self.manager.undo_last())
        self.assertEqual(self.balance.get_balance(), 100)

        self.assertTrue(self.manager.undo_last())
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_last_with_empty_history_returns_false(self):
        self.assertFalse(self.manager.undo_last())
        self.assertEqual(self.balance.get_balance(), 0)


if __name__ == "__main__":
    unittest.main()
