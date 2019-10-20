import datetime


class Customer():
    pass


class Account():
    def __init__(self, customer, loans):
        self.customer = customer
        self.loans = loans
        self.balance = 0
        self.payments = []

    def calculate_account_daily_rate(self, date):
        account_daily_rate = 0
        for loan in self.loans:
            if loan.is_active(date):
                account_daily_rate += loan.daily_rate

        return account_daily_rate

    def add_payment(self, payment):
        self.payments.append(payment)
        self.balance += payment.amount

    def make_loan_payment(self, date):
        today_rate = self.calculate_account_daily_rate(date)
        if today_rate <= self.balance:
            for loan in self.loans:
                if loan.is_active(date):
                    loan.loan_payments.append(
                        LoanPayment(loan.daily_rate, loan, date))
            self.balance -= today_rate
        else:
            print("Insufficient Funds")


class Loan():

    def __init__(self, amount, start_date, daily_rate):
        self.amount = amount
        self.start_date = start_date
        self.daily_rate = daily_rate
        self.loan_payments = []

    @property
    def days_to_start(self):
        return self.start_date - datetime.datetime.now().date()

    @property
    def loan_payments_total(self):
        total = 0
        for loan_payment in self.loan_payments:
            total += loan_payment.amount
        return total

    def is_active(self, date):
        return True if self.start_date < date else False


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
    def __init__(self, amount, loan, date):
        self.amount = amount
        self.loan = loan
        self.date = date


def get_days_of_power(account, payment):
    days_of_power = 0
    current_date = datetime.datetime.now().date()
    account.add_payment(payment)

    while 1:
        today_rate = account.calculate_account_daily_rate(current_date)
        print("Today: {}".format(current_date))
        print("Rate: {}".format(today_rate))
        print("Money Left: {}".format(account.balance))
        print("Days of Power: {}".format(days_of_power))
        if account.balance - today_rate > 0:
            account.make_loan_payment(current_date)
            if today_rate > 0:
                days_of_power += 1
            current_date += datetime.timedelta(1)
        else:
            break
    return days_of_power


def get_days_of_power_3_loans(R1, D1, R2, D2, R3, D3, K):
    """get_days_of_power_3_loans
    Helper method to get the days of power for 3 loans and a payment

    This method initializes the Loans, Account and Payments then calls
    get_days_of_power. It also pretty prints the paramaters given and days of 
    power
    """
    today = datetime.datetime.now().date()
    loan1 = Loan(10000000, today + datetime.timedelta(D1), R1)
    loan2 = Loan(10000000, today + datetime.timedelta(D2), R2)
    loan3 = Loan(10000000, today + datetime.timedelta(D3), R3)

    loans = [loan1, loan2, loan3]

    mark = Customer()
    account = Account(mark, loans)
    payment = Payment(K, account)
    print(
        """
        ***************************
        * R1: {:<20}*
        * D1: {:<20}*
        * R2: {:<20}*
        * D2: {:<20}*
        * R3: {:<20}*
        * D3: {:<20}*
        * K : {:<20}*
        * ------------------------*
        * Days Of Power: {:<8} *
        ***************************
        """.format(R1, D1, R2, D2, R3, D3, K, get_days_of_power(
            account,
            payment
            )
        )
    )
