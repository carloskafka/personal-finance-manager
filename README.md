# Personal Finance Manager

A small Python application for recording income and expenses, tracking a
balance, and notifying observers when the balance changes or drops below a
threshold. It demonstrates Singleton, Adapter, Observer, and Command patterns
using only the Python standard library.

## Requirements and usage

Requires Python 3.8 or newer. No third-party packages are needed.

```bash
python main.py
python -m unittest discover -v
```

The demonstration adapts freelance income, applies all transactions, prints
balance updates, and finishes with the current balance. The singleton balance
is process-local; it resets when the program exits.

## Patterns

- **Singleton — `balance/balance.py`:** `Balance.get_instance()` and direct
  construction return the same balance manager, avoiding multiple conflicting
  totals. `reset()` supports repeatable demonstrations and isolated tests.
- **Adapter — `transaction/transaction_adapter.py`:**
  `TransactionAdapter` turns the freelance platform's income record into the
  application's `Transaction` and `TransactionCategory.INCOME` format, keeping
  external data details out of the balance logic.
- **Observer — `balance/balance_observer.py`:** the balance notifies registered
  observers after transactions. `PrintObserver` (also exported as
  `PrintBalance`) reports changes; `LowBalanceAlertObserver` alerts when the
  total crosses below its threshold and clears its state when the balance
  recovers. Observers are injected through registration, and can be removed.
- **Command — `command/transaction_command.py`:** each
  `ApplyTransactionCommand` receives its `Balance` dependency explicitly.
  `CommandManager` executes transactions and retains undo/redo history. This
  provides a clear extension point for transaction history and reversible
  actions; its trade-off is extra state and bookkeeping.

The balance has no hard-coded observer dependencies, and command objects take
the balance through their constructors. This dependency injection keeps the
components easier to replace and test. Unit tests use Python's built-in
`unittest` framework and cover the balance, transaction model, adapter,
observers, and command history:

```bash
python -m unittest discover -v
```

## Reflection

I chose Command as the additional pattern because applying financial
transactions is naturally represented as an action that can be undone or
redone. Injecting the balance into each command makes the target explicit and
testable, while the Singleton ensures the app still shares one balance. The
Adapter isolates the external freelance format, and Observer separates alerts
and printing from balance calculations. The main trade-off is the additional
history and observer state that must be managed; the balance remains in memory
only, so a future version should persist transactions and balance changes.
