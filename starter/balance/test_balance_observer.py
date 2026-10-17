import io
import unittest
from contextlib import redirect_stdout
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import IBalanceObserver
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintObserver

class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)


class CountingObserver(IBalanceObserver):
    """Test helper: counts how many times it was notified."""

    def __init__(self):
        self.calls = 0

    def update(self, balance, transaction):
        self.calls += 1


class TestBalanceObservers(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.registered = []

    def tearDown(self):
        # The Balance is a shared Singleton: remove what this test added
        for observer in self.registered:
            self.balance.unregister_observer(observer)

    def register(self, observer):
        self.balance.register_observer(observer)
        self.registered.append(observer)

    def test_print_observer_prints_new_balance(self):
        self.register(PrintObserver())
        output = io.StringIO()
        with redirect_stdout(output):
            self.balance.apply_transaction(Transaction(80, TransactionCategory.INCOME))
        self.assertIn("balance is now $80.00", output.getvalue())

    def test_observer_registered_twice_is_notified_once(self):
        observer = CountingObserver()
        self.register(observer)
        self.register(observer)
        self.balance.apply_transaction(Transaction(10, TransactionCategory.INCOME))
        self.assertEqual(observer.calls, 1)

    def test_unregistered_observer_is_not_notified(self):
        observer = CountingObserver()
        self.register(observer)
        self.balance.unregister_observer(observer)
        self.balance.apply_transaction(Transaction(10, TransactionCategory.INCOME))
        self.assertEqual(observer.calls, 0)


if __name__ == "__main__":
    unittest.main()
