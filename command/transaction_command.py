from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class ApplyTransactionCommand:
    """Apply and reverse one transaction using an injected balance manager."""

    def __init__(self, transaction, balance):
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction")
        if not hasattr(balance, "apply_transaction"):
            raise TypeError("balance must support apply_transaction")
        self.transaction = transaction
        self.balance = balance
        self._executed = False

    def execute(self):
        if self._executed:
            raise RuntimeError("command has already been executed")
        self.balance.apply_transaction(self.transaction)
        self._executed = True

    def undo(self):
        if not self._executed:
            raise RuntimeError("command has not been executed")
        inverse_category = (
            TransactionCategory.EXPENSE
            if self.transaction.category is TransactionCategory.INCOME
            else TransactionCategory.INCOME
        )
        inverse_transaction = Transaction(
            self.transaction.amount,
            inverse_category,
        )
        self.balance.apply_transaction(inverse_transaction)
        self._executed = False


class CommandManager:
    """Execute commands and maintain undo/redo history."""

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def execute(self, command):
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            return False
        command = self._undo_stack.pop()
        try:
            command.undo()
        except Exception:
            self._undo_stack.append(command)
            raise
        self._redo_stack.append(command)
        return True

    def redo(self):
        if not self._redo_stack:
            return False
        command = self._redo_stack.pop()
        try:
            command.execute()
        except Exception:
            self._redo_stack.append(command)
            raise
        self._undo_stack.append(command)
        return True
