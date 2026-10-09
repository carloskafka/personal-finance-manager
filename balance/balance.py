from numbers import Real
from math import isfinite
from threading import Lock

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class Balance:
    """Singleton to track the balance."""

    _instance = None
    _instance_lock = Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._balance = 0.0
        self._observers = []
        self._initialized = True

    @classmethod
    def get_instance(cls):
        """Return the process-wide balance manager."""
        return cls()

    def reset(self):
        """Reset the net balance to zero."""
        self._balance = 0.0

    def add_income(self, amount):
        """Add income to the balance."""
        self.apply_transaction(Transaction(amount, TransactionCategory.INCOME))

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self.apply_transaction(Transaction(amount, TransactionCategory.EXPENSE))

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if not isinstance(transaction.category, TransactionCategory):
            raise ValueError("transaction category must be a TransactionCategory")
        self._validate_amount(transaction.amount)

        if transaction.category is TransactionCategory.INCOME:
            self._balance += transaction.amount
        elif transaction.category is TransactionCategory.EXPENSE:
            self._balance -= transaction.amount
        else:
            message = f"unsupported transaction category: {transaction.category}"
            raise ValueError(message)

        self._notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Current balance: ${self._balance:.2f}"

    def register_observer(self, observer):
        if not callable(getattr(observer, "update", None)):
            raise TypeError("observer must implement IBalanceObserver")
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def clear_observers(self):
        """Remove all subscribers, primarily for isolated tests."""
        self._observers.clear()

    def _notify_observers(self, transaction):
        for observer in tuple(self._observers):
            observer.update(self._balance, transaction)

    @staticmethod
    def _validate_amount(amount):
        if (
            isinstance(amount, bool)
            or not isinstance(amount, Real)
            or not isfinite(amount)
            or amount < 0
        ):
            raise ValueError("transaction amount must be a finite non-negative number")
