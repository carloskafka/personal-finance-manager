# balance_observer.py

from math import isfinite
from numbers import Real


class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(
            f"Balance updated: ${balance:.2f} "
            f"after {transaction.category.name.lower()} of ${transaction.amount:.2f}"
        )


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        if (
            isinstance(threshold, bool)
            or not isinstance(threshold, Real)
            or not isfinite(threshold)
            or threshold < 0
        ):
            raise ValueError("threshold must be a non-negative number")
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        below_threshold = balance < self.threshold
        if below_threshold and not self.alert_triggered:
            print(
                f"Low balance alert: ${balance:.2f} is below "
                f"the ${self.threshold:.2f} threshold"
            )
        self.alert_triggered = below_threshold


PrintBalance = PrintObserver
