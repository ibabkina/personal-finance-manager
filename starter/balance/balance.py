# balance.py

from transaction.transaction_category import TransactionCategory


class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __new__(cls):
        """Create the one and only Balance the first time; afterwards return that same object."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._balance = 0.0
            cls._instance._observers = []
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Return the single shared Balance object."""
        return cls()

    def register_observer(self, observer):
        """Subscribe an observer to balance changes (ignored if already registered)."""
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        """Unsubscribe an observer from balance changes."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, transaction):
        """Tell every registered observer the new balance and the transaction that caused it."""
        for observer in self._observers:
            observer.update(self._balance, transaction)

    def reset(self):
        """Reset the net balance to zero."""
        self._balance = 0.0

    def add_income(self, amount):
        """Add income to the balance."""
        self._balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance, then notify observers.

        Args:
            transaction (Transaction): The transaction to apply.

        Raises:
            ValueError: If the transaction category is not INCOME or EXPENSE.
        """
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError(f"Unknown transaction category: {transaction.category}")
        self.notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Current balance: ${self._balance:.2f}"
