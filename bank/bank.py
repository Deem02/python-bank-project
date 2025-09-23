# Add New Customer
# customer can have a checking account
# customer can have a savings account
# customer can have both a checking and a savings account
# cashiers can type in an id or this can be automatically generated

import uuid
import csv
class Customer:
    def __init__(self, account_id, first_name, last_name, password):
        #self.customer_id = uuid.uuid4()
        self.account_id = int(account_id)
        self.first_name = first_name
        self.last_name = last_name
        self.password= password
        #self.accounts = []
        self.checking_account =None
        self.savings_account =None
      
    # def  add_account(self, account):
    #     self.accounts.append(account) 
        
    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}, Account ID: {self.account_id}"
    
    
 # self.balance_checking =balance_checking
        # self.balance_savings = balance_savings     
   
class BankAccount(): 
    
    def __init__(self, customer, balance=0.0):
        self.customer = customer
        self.balance = float(balance)
        
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount 
            print(f"Deposited {amount}. New balance: {self.balance}")
            return True
        else:
            print("Deposit amount must be positive")
            return False
        
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
            return True
        else:
            print("Insufficient funds or invalid amount")
            return False
    def __str__(self):
        return f"Account ID: {self.customer.account_id} Balance {self.balance}"
       
#  https://codebricks.co.nz/python-oop-example-01 

class CheckingAccount(BankAccount):     
    def __str__(self):
        return f"Checking Account ID: {self.customer.account_id} Balance {self.balance}"
        
class SavingsAccount(BankAccount):        
    def __str__(self):
        return f"Saving Account ID: {self.customer.account_id} Balance {self.balance}"
  
class Bank:
    def __init__(self, filename='data/bank.csv'):
        self.filename = filename
        self.customers = {}
        self.load_customers()
       
    def load_customers(self):
        try:
            with open(self.filename, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    account_id= int(row['account_id'])
                    customer = Customer(
                        account_id=account_id,   
                        first_name= row['frst_name'],
                        last_name= row['last_name'],
                        password= row['password']                        
                        )
                    customer.checking_account = CheckingAccount(customer, float(row['balance_checking']) )
                    customer.savings_account = SavingsAccount(customer, float(row['balance_savings']))
                    self.customers[account_id] = customer
        except Exception as e:
              print(f"An error occuured while loading the file: {e}")
                
    def save_customers(self):
        try:
           fieldnames = ['account_id','frst_name','last_name','password','balance_checking','balance_savings'] 
           with open(self.filename, 'w', newline='') as file:
               writer = csv.DictWriter(file, fieldnames=fieldnames) 
               writer.writeheader()
               for customer in self.customers.values():
                writer.writerow({
                    'account_id': customer.account_id,
                    'frst_name': customer.first_name,
                    'last_name': customer.last_name, 
                    'password': customer.password,
                    'balance_checking': customer.checking_account.balance if customer.checking_account else 0,
                    'balance_savings': customer.savings_account.balance if customer.savings_account else 0
                })
        except IOError as e:
            print(f'Error: could not save data. {e}')
          #https://realpython.com/python-csv/ 
          
    def get_account_id(self):
        if not self.customers:
            return 1001
        return max(self.customers.keys()) +1
        
    def add_customer(self, first_name, last_name, password, checking_balance=0, savings_balance=0):
        account_id = self.get_account_id()
        new_customer = Customer(account_id,first_name, last_name, password)
        new_customer.checking_account = CheckingAccount(new_customer,checking_balance)
        new_customer.savings_account = SavingsAccount(new_customer, savings_balance)
        self.customers[account_id] = new_customer
        print(f"Customer '{first_name} {last_name}' Account ID: {account_id} added successfully ")
        
        self.save_customers()
        return new_customer
  
        
    def handle_add_new_customer(self):
        while True:
            first_name = input("First Name: ").strip()
            if first_name:
                break
            print('First name cannnot be empty. Please try agein ')
        while True:
            last_name = input("Last Name: ").strip()
            if last_name:
                break
            print('Last name cannnot be empty. Please try agein ')
        while True:
            password = input("Password: ").strip()
            if password:
                break
            print('Password cannnot be empty. Please try agein ')
        try:
            checking_balance = float(input('Enter initiial cheking balance: ') or '0.0') # if its empty string
            savings_balance = float(input('Enter initiial savings balance: ') or '0.0')
            if checking_balance < 0 or savings_balance < 0:
               print('Balance cannot be nefative. Setting it to 0.') 
               checking_balance = max(0, checking_balance)
               savings_balance = max(0, savings_balance)
        except ValueError:
           print("Invalid amount. Creating account with 0 balance")
           checking_balance = 0.0
           savings_balance = 0.0
           
        customer = self.add_customer(first_name, last_name, password, checking_balance, savings_balance)
        #print(customer)
    
if __name__ == '__main__' : 
    # customer1 = Customer('deem','alqasir', '123')
    # print(customer1)
    
    # first_name = input("First Name: ")
    # last_name = input("Last Name: ")
    # password = input("Password: ")
    # customer1 = Customer(first_name, last_name, password)
    # print(customer1)
    bank = Bank()
    while True:
        print('1) Add New Customer')
        print('2) Exit')
        choice = input('Choose an option: ').strip()
        
        if choice == '1':   
            bank.handle_add_new_customer()
        elif choice == '2':
            print('Exiting from application')
            break
        else:
            print('Invalid option. Please try agin.')