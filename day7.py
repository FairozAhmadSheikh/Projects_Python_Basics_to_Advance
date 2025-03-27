import datetime

class Account:
    """Base class for a bank account"""
    def __init__(self, owner, balance=0.0):
        self._owner = owner  # Encapsulation
        self._balance = balance
        self._transactions = []
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self._transactions.append((datetime.datetime.now(), f"Deposited: {amount}"))
        else:
            print("Deposit amount must be positive!")
    
    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            self._transactions.append((datetime.datetime.now(), f"Withdrawn: {amount}"))
        else:
            print("Invalid withdrawal amount!")
    
    def get_balance(self):
        return self._balance
    
    def get_transaction_history(self):
        return self._transactions
    
    def __str__(self):
        return f"Account Owner: {self._owner}, Balance: {self._balance}"

class SavingsAccount(Account):
    """Derived class for a savings account with interest feature"""
    def __init__(self, owner, balance=0.0, interest_rate=0.02):
        super().__init__(owner, balance)
        self._interest_rate = interest_rate
    
    def apply_interest(self):
        interest = self._balance * self._interest_rate
        self.deposit(interest)
        self._transactions.append((datetime.datetime.now(), f"Interest Applied: {interest}"))
    
    def __str__(self):
        return f"Savings Account - {super().__str__()}, Interest Rate: {self._interest_rate * 100}%"

class CurrentAccount(Account):
    """Derived class for a current account with overdraft protection"""
    def __init__(self, owner, balance=0.0, overdraft_limit=500):
        super().__init__(owner, balance)
        self._overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if amount > 0 and amount <= (self._balance + self._overdraft_limit):
            self._balance -= amount
            self._transactions.append((datetime.datetime.now(), f"Withdrawn: {amount} (Overdraft Used)"))
        else:
            print("Withdrawal exceeds overdraft limit!")
    
    def __str__(self):
        return f"Current Account - {super().__str__()}, Overdraft Limit: {self._overdraft_limit}"

# # Example Usage
# if __name__ == "__main__":
#     sa = SavingsAccount("Alice", 1000)
#     sa.deposit(500)
#     sa.apply_interest()
#     print(sa)
#     print("Transaction History:", sa.get_transaction_history())
    
#     ca = CurrentAccount("Bob", 300, 1000)
#     ca.withdraw(1200)
#     print(ca)
#     print("Transaction History:", ca.get_transaction_history())
