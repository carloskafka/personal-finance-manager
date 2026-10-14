import unittest
from contextlib import redirect_stdout
from io import StringIO
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver


class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.balance.clear_observers()

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME)
        )
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.EXPENSE)
        )
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(100, TransactionCategory.INCOME)
        )
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.EXPENSE)
        )
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(
            Transaction(60, TransactionCategory.EXPENSE)
        )
        self.assertTrue(observer.alert_triggered)

    def test_low_balance_alert_observer_prints_when_threshold_is_crossed(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        output = StringIO()

        with redirect_stdout(output):
            self.balance.apply_transaction(
                Transaction(40, TransactionCategory.INCOME)
            )

        self.assertTrue(observer.alert_triggered)
        self.assertIn("below", output.getvalue().lower())

    def test_print_observer_reports_updated_balance(self):
        self.balance.register_observer(PrintObserver())
        output = StringIO()

        with redirect_stdout(output):
            self.balance.apply_transaction(
                Transaction(75, TransactionCategory.INCOME)
            )

        self.assertIn("$75", output.getvalue())


if __name__ == "__main__":
    unittest.main()
