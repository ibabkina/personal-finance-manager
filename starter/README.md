# Personal Finance Manager — Reflection

## Design patterns used
- Singleton (Balance): I used it because the app must have only one balance; two separate balances would give wrong totals. It helped by making every part of the app (main.py, the commands and the tests) use the same balance through `Balance.get_instance()`.
- Adapter (TransactionAdapter): I used it because the freelance platform describes income in its own format (amount, invoice ID and description), which my app does not understand. It helped by turning that data into a normal `Transaction`, so the rest of the app never needs to know about the external format.
- Observer (PrintObserver, LowBalanceAlertObserver): I used it because several things need to react when the balance changes. It helped by keeping `Balance` simple: it only notifies its observers, and each observer decides what to do (print the new balance or show an alert below the threshold). New reactions can be added without changing `Balance`.
- Command (my choice): I chose it because it makes it possible to undo the last transaction. It is used in main.py, where every transaction is applied through an `ApplyTransactionCommand` and `CommandManager.undo_last()` reverses the last one. It improves testability and flexibility: each action is a small object that is easy to test, the balance is passed in through the constructor (dependency injection) so tests can use a fake balance, and more commands can be added later.

## Trade-offs and challenges
- The Singleton is shared by everything, including the tests, so each test has to reset the balance first, and observers added in one test stay registered in later tests. I had to unregister them in `tearDown`.
- The Command pattern adds extra classes and files compared to calling `apply_transaction` directly, and the Adapter drops the invoice ID and description because `Transaction` has no place for them.
- At first `python -m unittest discover` ran 0 tests, because the folders had no `__init__.py` files. Adding them fixed it.
