import unittest

from balance.balance import Balance
from command.transaction_command import (
    ApplyTransactionCommand,
    CommandManager,
)
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransactionCommand(unittest.TestCase):
    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.balance.clear_observers()
        self.commands = CommandManager()

    def test_execute_undo_and_redo_transaction(self):
        command = ApplyTransactionCommand(
            Transaction(100, TransactionCategory.INCOME),
            self.balance,
        )

        self.commands.execute(command)
        self.assertEqual(self.balance.get_balance(), 100)

        self.assertTrue(self.commands.undo())
        self.assertEqual(self.balance.get_balance(), 0)

        self.assertTrue(self.commands.redo())
        self.assertEqual(self.balance.get_balance(), 100)

    def test_new_command_clears_redo_history(self):
        self.commands.execute(
            ApplyTransactionCommand(
                Transaction(100, TransactionCategory.INCOME),
                self.balance,
            )
        )
        self.commands.undo()
        self.commands.execute(
            ApplyTransactionCommand(
                Transaction(25, TransactionCategory.EXPENSE),
                self.balance,
            )
        )

        self.assertFalse(self.commands.redo())
        self.assertEqual(self.balance.get_balance(), -25)

    def test_undo_and_redo_return_false_when_history_is_empty(self):
        self.assertFalse(self.commands.undo())
        self.assertFalse(self.commands.redo())


if __name__ == "__main__":
    unittest.main()
