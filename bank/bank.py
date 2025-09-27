class BankError(Exception):
   pass 

class InvalidAmountError(BankError):
    pass
class InsufficientFundsError (BankError):
    pass
class AccountDeactiveError(BankError):
    pass
class OverdraftLimitError(BankError):
    pass

class AccountNotFoundError(BankError):
    pass

#import uuid
import csv
class Customer:
    def __init__(self, account_id, first_name, last_name, password):
        self.account_id = int(account_id)
        self.first_name = first_name
        self.last_name = last_name
        self.password= password
        self.checking_account =None
        self.savings_account =None
    
        
    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}, Account ID: {self.account_id}"
        
   
class BankAccount(): 
    
    def __init__(self, customer, balance=0.0):
        self.customer = customer
        self.balance = float(balance)
        
    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")      
        self.balance += amount 
       
        
    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdraw amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError(f'Insufficient funds. Current Balance:{self.balance}')
        self.balance -= amount
    
    def __str__(self):
        return f"Account ID: {self.customer.account_id} Balance {self.balance}"
       
#  https://codebricks.co.nz/python-oop-example-01 

class CheckingAccount(BankAccount): 
    OVERDRAFT_FEE = 35.0
    OVERDRAFT_LIMIT = -100.0
    MAX_OVERDRAFTS = 2
    
    def __init__(self, customer, balance=0.0, overdraft_count=0, is_active= True):
        super().__init__(customer, balance)
        self.overdraft_count = int(overdraft_count)
        self.is_active = str(is_active).lower() == 'true'
    
        
    def withdraw(self, amount):
        if not self.is_active:
            raise AccountDeactiveError(f'Account is deactivated. Current Balance is {self.balance}. Please deposit at least {-self.balance} to reactivate.')
            
        if self.balance>=amount:
            super().withdraw(amount)
          
        else: # an overdraft situation
            total_charge = amount +self.OVERDRAFT_FEE
            if (self.balance - total_charge) < self.OVERDRAFT_LIMIT:
                raise OverdraftLimitError(f'Transaction denied. Exceeds overdraft limit of ${self.OVERDRAFT_LIMIT} ')
              
            # overdraft allowed 
            self.balance -= total_charge
            self.overdraft_count += 1
            print(f'Overdraft fee of ${self.OVERDRAFT_FEE} has been applied. New Balance: {self.balance}')
            
            if self.overdraft_count >= self.MAX_OVERDRAFTS:
                self.is_active = False
                print('Warning: Account has been deactivated due to reaching the maximum number og overdrafts.')
      
        
    def deposit(self, amount):  
        was_inactive = not self.is_active
        super().deposit(amount)          
         
        if was_inactive:
            # reactivate if  the customer balance become  >=0 
            if self.balance >=0:
              self.is_active = True
              self.overdraft_count = 0
              print('Account is reactivated!') 
            
                
              
    def __str__(self):
        return f"Checking Account Balance: {self.balance}"
        
class SavingsAccount(BankAccount):        
    def __str__(self):
        return f"Saving Account Balance: {self.balance}"
  
class Bank:
    def __init__(self, filename='data/bank.csv'):
        self.filename = filename
        self.customers = {}
        self.current_customer = None # to track logged in
        self.CSV_HEADERS = [
            'account_id','frst_name','last_name','password','balance_checking',
            'balance_savings','checking_overdrafts','checking_is_active'
        ]
        self.load_customers()
       
    def load_customers(self):
        try:
            with open(self.filename, 'r', newline='') as file:
                rows = list(csv.DictReader(file))
                for row in rows:
                    account_id= int(row['account_id'])
                    customer = Customer(
                        account_id=account_id,   
                        first_name= row['frst_name'],
                        last_name= row['last_name'],
                        password= row['password']                        
                        )
                    customer.checking_account = CheckingAccount(customer, 
                                                                float(row.get('balance_checking') or 0.0),
                                                                int(row.get('checking_overdrafts') or 0), 
                                                                row.get('checking_is_active') or 'True' )
                    customer.savings_account = SavingsAccount(customer, float(row['balance_savings']))
                    self.customers[account_id] = customer
        except Exception as e:
              print(f"An error occuured while loading the file: {e}")
                
    def save_customers(self):
        try:
           with open(self.filename, 'w', newline='') as file:
               writer = csv.DictWriter(file, fieldnames=self.CSV_HEADERS) 
               writer.writeheader()
               for customer in self.customers.values():
                writer.writerow({
                    'account_id': customer.account_id,
                    'frst_name': customer.first_name,
                    'last_name': customer.last_name, 
                    'password': customer.password,
                    'balance_checking': customer.checking_account.balance if customer.checking_account else 0,
                    'balance_savings': customer.savings_account.balance if customer.savings_account else 0,
                    'checking_overdrafts': customer.checking_account.overdraft_count,
                    'checking_is_active': customer.checking_account.is_active,
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
  
    def login(self): 
        try:
            account_id = int(input("Enter your account ID: "))  
            password = input("Enter your password: ") 
            customer = self.customers.get(account_id)
            if customer and customer.password == password:
                self.current_customer = customer
                print(f"Welcome {customer.first_name} {customer.last_name}!")
            else: 
                print('Invalid account ID or password') 
        except ValueError:
            print('Invalid account ID format. Enter a number') 
    def logout(self):
        self.current_customer = None        
      
    def handle_deposit(self):
        print("1) Checking Account")
        print("2) Savings Account")
        choice = input("Choose an account to deposit: ")
        
        if choice == '1' or choice == '2' : 
            try:
                amount = float(input("Enter the amount:"))
                if choice == '1':
                    self.current_customer.checking_account.deposit(amount)
                    print(f'Deposited {amount} New balance: {self.current_customer.checking_account.balance}')
                    self.save_customers()
                elif choice == '2':
                    self.current_customer.savings_account.deposit(amount)
                    print(f'Deposited {amount} New balance: {self.current_customer.savings_account.balance}')
                    self.save_customers()
            except InvalidAmountError as e:
                print(f'Deposit failed: {e}')                                
            except ValueError:
                print('Invalid amount. Enter a number')
        else:
          print('Invalid choice')
          
          
    def handle_withdraw(self):
        print("1) Checking Account")
        print("2) Savings Account")
        choice = input("Choose an account to withdraw: ")
        if choice == '1' or choice == '2' :
            try:
                amount = float(input("Enter the amount:"))
                if choice == '1': 
                    self.current_customer.checking_account.withdraw(amount)
                    print(f'Withdrew {amount} New balance: {self.current_customer.checking_account.balance}')
                    self.save_customers()
                elif choice == '2':
                    self.current_customer.savings_account.withdraw(amount)
                    print(f'Withdrew {amount} New balance: {self.current_customer.savings_account.balance}')
                    self.save_customers() 
                  
            except BankError as e:
                print(f'withdraw failed: {e}')           
            except ValueError:
                print('Invalid amount. Enter a number')
        else:
         print('Invalid choice')  
    
    def handle_transfer(self):
        print('1) Transfer between your accounts')
        print('2) Transfer to another customer accounts')
        choice = input("Choose a transfer type: ")
        
        if choice =='1':
            self.transfer_internal()
        elif choice == '2':
            self.transfer_external()
        else:
            print('Invalid choice.')
            
    def transfer_internal(self):
        print('1) From Cheking -> Savings')
        print('2) From Savings -> Cheking')
        choice = input("Choose a transfer direction: ")
        
        if choice == '1':
            source = self.current_customer.checking_account
            destination = self.current_customer.savings_account
        elif choice == '2':
            source = self.current_customer.savings_account
            destination = self.current_customer.checking_account 
        else:
            print('Invalid choice.')
            return 
            
        try:
            amount = float(input('Enter amount to transfer:'))
   
            source.withdraw(amount)
            destination.deposit(amount)
            self.save_customers()
            print('Transfer successfully ✅')
            
        except BankError as e:
               print(f'Transfer failed: {e}') 
        except ValueError:
            print('Invaild amount')     
            
    def transfer_external(self):
        try:
            recipient_id = int(input('Enter recipient account ID: ')) 
            recipient = self.customers.get(recipient_id)  
            if not recipient:
                raise AccountNotFoundError('Recipient account nor found')
                
            if recipient_id == self.current_customer.account_id:
                raise BankError('Cannot transfer to yourself. Use internal transfer option ')
                
            print(f'Transfer will be deposited to {recipient.first_name} {recipient.last_name} cheking account')
            print('Transfer from: ')
            print('1) My Cheking account')
            print('2) My Savings account')
            source_choice = input('Choose your source account: ').strip()
            source_account = None
            if source_choice == '1':
                source_account = self.current_customer.checking_account
            elif source_choice == '2':
                source_account = self.current_customer.savings_account
            else:
                print('Invaild source account choice')
                return
            dest_account = recipient.checking_account
            amount = float(input('Enter amount to transfer:'))
            source_account.withdraw(amount)
            dest_account.deposit(amount)
            self.save_customers()
            print('Transfer to other customer successfully ✅')
        except BankError as e:
            print(f'Transfer failed: {e}')     
                
        except ValueError:
            print('Invalid ID or amont') 
            
            
                     
    def handle_add_new_customer(self):
        while True:
            first_name = input("First Name: ").strip()
            if not first_name:
                print('First name cannnot be empty. Please try agein ')   
            elif not first_name.isalpha():
                print('Error: Please enter only alphabetical characters for your name') 
            else:
                break
            
        while True:
            last_name = input("Last Name: ").strip()
            if not last_name:
                print('Last name cannnot be empty. Please try agein ')
            elif not last_name.isalpha():
                print('Error: Please enter only alphabetical characters for your name') 
            else:
                break
        while True:
            password = input("Password: ").strip()
            if password:
                break
            print('Password cannnot be empty. Please try agein ')
        try:
            checking_balance = float(input('Enter initiial cheking balance: ') or '0.0') # if its empty string
            savings_balance = float(input('Enter initiial savings balance: ') or '0.0')
            if checking_balance < 0 or savings_balance < 0:
               print('Balance cannot be negative. Setting it to 0.') 
               checking_balance = max(0, checking_balance)
               savings_balance = max(0, savings_balance)
        except ValueError:
           print("Invalid amount. Creating account with 0 balance")
           checking_balance = 0.0
           savings_balance = 0.0
           
        self.add_customer(first_name, last_name, password, checking_balance, savings_balance)
        #print(customer)
    def show_customer_menu(self):
        customer= self.current_customer
        print(customer.checking_account)
        print(customer.savings_account)
        print('1) Deposit')
        print('2) Withdraw')
        print('3) Transfer')
        print('4) Logout')
        choice = input('Choose an option:').strip()
        
        if choice == '1':
            self.handle_deposit()
        elif choice == '2':
            self.handle_withdraw()
        elif choice == '3':
            self.handle_transfer()
        elif choice == '4':
            self.logout()
        else:
            print('Invalid option')
            
            
if __name__ == '__main__' : 
    
    bank = Bank()
    while True:
        
        if bank.current_customer:
            bank.show_customer_menu()
        else:
            print('1) Add New Customer')
            print('2) Login')
            print('3) Exit')
            choice = input('Choose an option: ').strip()
            
            if choice == '1':   
                bank.handle_add_new_customer()
                continue
            if choice == '2':
                bank.login()
            elif choice == '3':
                print('Exiting from application')
                break
            else:
                print('Invalid option. Please try agin.')