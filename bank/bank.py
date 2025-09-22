# Add New Customer
# customer can have a checking account
# customer can have a savings account
# customer can have both a checking and a savings account
# cashiers can type in an id or this can be automatically generated

import uuid
class Customer:
    def __init__(self, first_name, last_name, password):
        self.customer_id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.password= password
        self.accounts = []
      
    def  add_account(self, account):
        self.accounts.append(account) 
        
    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}, Customer ID: {self.customer_id}"
    
    
 # self.balance_checking =balance_checking
        # self.balance_savings = balance_savings     
   
class BankAccount(): 
    account_number_counter= 1000
    def __init__(self, customer, balance=0):
        self.account_number = BankAccount.account_number_counter
        BankAccount.account_number_counter +=1
        self.balance = balance
        self.customer = customer
        
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount 
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive")
        
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            print("Insufficient funds or invalid amount")
    def __str__(self):
        return f"Account #{self.account_number} Balance {self.balance}"
       
#  https://codebricks.co.nz/python-oop-example-01 

class CheckingAccount(BankAccount):
    def __init__(self, customer, balance = 0):
        super().__init__(customer,balance)
        
    def __str__(self):
        return f"Checking Account #{self.account_number} Balance {self.balance}"
        
class SavingsAccount(BankAccount):
    def __init__(self, customer, balance = 0):
        super().__init__(customer,balance)
        
    def __str__(self):
        return f"Saving Account #{self.account_number} Balance {self.balance}"
  
class Bank:
    def __init__(self):
        self.customers = {}
        
    def add_customer(self, first_name, last_name, password, checking_balance=None, savings_balance=None):
        new_customer = Customer(first_name, last_name, password)
        self.customers[new_customer.customer_id] = new_customer
        print(f"Customer '{first_name} {last_name}' add successfully ")
        
        if checking_balance is not None:
            checking_account = CheckingAccount(customer=new_customer, balance=checking_balance)
            new_customer.add_account(checking_account)
            print("Checking Account created")
            
        if savings_balance is not None:
            savings_account = SavingsAccount(customer=new_customer, balance=savings_balance)
            new_customer.add_account(savings_account)
            print("Savings Account created")
        return new_customer
    
    def get_initial_balance(self, account_type):
        wants_account_input = input(f"Want to open a {account_type} account? (yes/no) ").lower() 
        if wants_account_input in ['yes','y']:
            try:
               balance = float(input(f"Enter initial {account_type} balance:")) 
               return balance if balance >= 0 else 0.0
            except ValueError:
                print(f"Invalid amount. Creating {account_type} account with 0 balance ")
                return 0.0
        return None

        
    def handle_add_new_customer(self):
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        password = input("Password: ")
        # wants_cheking = input("Want to open a cheking account? (yes/no)").lower() in ['yes']
        # wants_saving = input("Want to open a saving account? (yes/no)").lower() in ['yes']
        checking_balance = self.get_initial_balance('cheking')
        savings_balance = self.get_initial_balance('savings')
        customer = self.add_customer(first_name, last_name, password, checking_balance, savings_balance)
        print(customer)
    
if __name__ == '__main__' : 
    # customer1 = Customer('deem','alqasir', '123')
    # print(customer1)
    
    # first_name = input("First Name: ")
    # last_name = input("Last Name: ")
    # password = input("Password: ")
    # customer1 = Customer(first_name, last_name, password)
    # print(customer1)
    bank = Bank()
    bank.handle_add_new_customer()