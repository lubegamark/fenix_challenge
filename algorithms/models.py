import datetime


class Customer():
    pass


class Account():
    pass


class Loan():

    def __init__(self, amount, start_date, daily_rate):
        self.amount = amount
        self.start_date = start_date
        self.daily_rate = daily_rate

    @property
    def days_to_start(self):
        return self.start_date - datetime.datetime.now().date()


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
