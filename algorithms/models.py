import datetime


class Customer():
    """Customer

    Customer is the primary user who has an account, owns devices, takes
    loans, makes payment
    """
    pass


class Account():
    """Account
    An Account belonging to a Customer

    The initial balance is zero.
    customer the customer who owns the account
    loans    list of all loans belonging to account
    payments list of all payments made to account
    """
    def __init__(self, customer):
        self.customer = customer
        self.loans = []
        self.balance = 0
        self.payments = []

    def calculate_account_daily_rate(self, date):
        """Calculate the total Daily Rate for all active loans in an account

        Daily Rate is sum of all daily rates on that date.
        """
        account_daily_rate = 0
        for loan in self.loans:
            if loan.is_active(date):
                account_daily_rate += loan.daily_rate

        return account_daily_rate

    def add_loans(self, loans):
        """Add loans to an account
        """
        self.loans.extend(loans)

    def make_payment(self, payment):
        """Make Payment into an account
        """
        self.payments.append(payment)
        self.balance += payment.amount

    def make_loan_payment(self, date):
        """Make all Loan Payments towards all loans due on date

        If balance is insufficient to clear all loans, none is paid back
        """
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
    """Loan

    Loan represents a debt which a customer is expected to pay back in
    installments on a daily basis

    amount        the total amount of the loan
    start_date    the date when daily repayments start
    daily_rate    amount expected to be paid on a daily basis
    loan_payments list of all payments towards this loan
    """

    def __init__(self, amount, start_date, daily_rate):
        self.amount = amount
        self.start_date = start_date
        self.daily_rate = daily_rate
        self.loan_payments = []

    @property
    def days_to_start(self):
        """Days until this loan becomes active

        Number of days until this payments towards it are expected to start
        """
        return self.start_date - datetime.datetime.now().date()

    @property
    def loan_payments_total(self):
        """Total of all loan payments made to this loan
        """
        total = 0
        for loan_payment in self.loan_payments:
            total += loan_payment.amount
        return total

    def is_active(self, date):
        return True if self.start_date <= date else False


class Device():
    """Device
    A device which acts as collateral for loan
    """
    pass


class Payment():
    """Payment
    A payment of money into an account. This credits the account with the
    amount specified.

    amount  amount paid
    account account paid into
    """
    def __init__(self, amount, account):
        self.amount = amount
        self.account = account


class LoanPayment():
    """LoanPayment
    LoanPayment puts part of the account balance towards specific loan. This
    debits the Account.

    amount   amount put towards that loan
    loan     the loan to which this payment is made
    date     date when this transaction was debited to this loan and credited
             from the balance
    """
    def __init__(self, amount, loan, date):
        self.amount = amount
        self.loan = loan
        self.date = date


def get_days_of_power(account, payment):
    days_of_power = 0
    current_date = datetime.datetime.now().date()
    account.make_payment(payment)

    while 1:
        today_rate = account.calculate_account_daily_rate(current_date)
        if account.balance - today_rate > 0:
            account.make_loan_payment(current_date)
            if today_rate > 0:
                days_of_power += 1
            current_date += datetime.timedelta(1)
            print("Today: {}".format(current_date))
            print("Rate: {}".format(today_rate))
            print("Money Left: {}".format(account.balance))
            print("Days of Power: {}".format(days_of_power))
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
    account = Account(mark)
    account.add_loans(loans)
    payment = Payment(K, account)

    days_of_power = get_days_of_power(account, payment)
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
        """.format(R1, D1, R2, D2, R3, D3, K, days_of_power)
    )

    return days_of_power
