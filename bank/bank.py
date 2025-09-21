# Add New Customer
# customer can have a checking account
# customer can have a savings account
# customer can have both a checking and a savings account
# cashiers can type in an id or this can be automatically generated

import uuid
class Customer():
    def __init__(self, first_name, last_name, password):
        self.account_id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.password= password
          
        
    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}, Account ID: {self.account_id}"
    
    
 # self.balance_checking =balance_checking
        # self.balance_savings = balance_savings     
   
    
    #BankAccount():
if __name__ == '__main__' : 
    customer1 = Customer('deem','alqasir', '123')
    print(customer1)
