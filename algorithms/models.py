import datetime


class Customer():
    pass


class Account():
    pass


class Loan():

    def __init__(self, amount, start_date, daily_rate, loan_payments):
        self.amount = amount
        self.start_date = start_date
        self.daily_rate = daily_rate
        self.loan_payments = loan_payments

    @property
    def days_to_start(self):
        return self.start_date - datetime.datetime.now().date()

    @property
    def loan_payments_total(self):
        total = 0
        for loan_payment in self.loan_payments:
            total += loan_payment.amount
        return total

    @property
    def fully_paid(self):
        return True if self.loan_payments_total >= self.amount else False

    @property
    def active(self):
        if (self.start_date > datetime.datetime.now().date() and
                self.fully_paid is False):
            return True
        return False


class Device():
    pass


class Payment():
    def __init__(self, amount, account):
        self.amount = amount
        self.account = account


class LoanPayment():
    """
    LoanPayment puts part of a payment to a specific loan
    """
    def __init__(self, payment, amount, loan, date):
        self.payment = payment
        self.amount = amount
        self.loan = loan
        self.date = date
