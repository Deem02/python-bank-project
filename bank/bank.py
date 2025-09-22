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
        
    
class CheckingAccount(BankAccount):
    def __init__(self):
        pass
    
class SavingsAccount(BankAccount):
    def __init__(self):
        pass
    
    #BankAccount():
if __name__ == '__main__' : 
    # customer1 = Customer('deem','alqasir', '123')
    # print(customer1)
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    password = input("Password: ")
    customer1 = Customer(first_name, last_name, password)
    print(customer1)
    
