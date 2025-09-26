import unittest
from bank.bank import Customer, BankAccount, CheckingAccount, SavingsAccount, Bank

class TestCustomer(unittest.TestCase):
    def test_create_customer_object(self):
        self.customer = Customer(1001,'Deem', 'alqasir', 'password')
        self.assertEqual(self.customer.first_name,'Deem')
        self.assertEqual(self.customer.last_name,'alqasir')
        self.assertEqual(self.customer.password,'password')
        self.assertEqual(self.customer.account_id, 1001 )
    
        
    # def test_add_account(self):
    #     customer = Customer('Dana', 'alaile', 'password21')
    #     account = 'Account object'
    #     customer.add_account(account)
    #     self.assertIn(account, customer.accounts)
    #     self.assertEqual(len(customer.accounts), 1)
       
class TestBankAccountAndSubclass(unittest.TestCase):
    
    def setUp(self): 
        self.customer = Customer(1002,'Arwa', 'alslam', 'password1')
        self.checking = CheckingAccount(self.customer, balance=1500) 
        self.savings = SavingsAccount(self.customer, balance=500) 
        
    def test_account_creation(self):
        self.assertEqual(self.checking.balance, 1500.0)
        self.assertEqual(self.savings.balance, 500)
    
        
    def test_deposit(self):
        self.checking.deposit(100)
        self.assertEqual(self.checking.balance, 1600)
        self.checking.deposit(-100)
        self.assertEqual(self.checking.balance, 1600)
        
        self.savings.deposit(10000)
        self.assertEqual(self.savings.balance,10500)
        self.savings.deposit(0)
        self.assertEqual(self.savings.balance,10500)
        
        
    def test_withdraw(self):
        self.checking.withdraw(50)
        self.assertEqual(self.checking.balance, 1450)
        self.checking.withdraw(0)
        self.assertEqual(self.checking.balance, 1450)
        
        self.savings.withdraw(500)
        self.assertEqual(self.savings.balance,0)
        self.savings.withdraw(-150)
        self.assertEqual(self.savings.balance,0)

class TestChekingAccountOverdraft(unittest.TestCase):     
    def setUp(self):
        self.customer = Customer(1003,'dana', 'ahmed', 'password1') 
        self.cheking = CheckingAccount(self.customer, balance=50.0)
        
    def test_first_overdraft(self):
        self.assertTrue(self.cheking.withdraw(60)) 
        self.assertEqual(self.cheking.balance, -45.0) 
        self.assertEqual(self.cheking.overdraft_count, 1)
        self.assertTrue(self.cheking.is_active)
        
    def test_overdraft_denied(self):   
        self.assertFalse(self.cheking.withdraw(200)) 
        self.assertEqual(self.cheking.balance, 50) 
        self.assertTrue(self.cheking.is_active)
        
    def test_second_overdraft(self):
        # self.test_first_overdraft()  # I can do it like this but each test should be isolated 
        self.assertTrue(self.cheking.withdraw(60)) 
        self.assertEqual(self.cheking.balance, -45.0) 
        self.assertEqual(self.cheking.overdraft_count, 1)
        
        self.assertTrue(self.cheking.withdraw(20))
        self.assertEqual(self.cheking.overdraft_count, 2)
        self.assertFalse(self.cheking.is_active)
                 
# class TestBank(unittest.TestCas):
#     pass


#python -m unittest  tests.test_bank
# if __name__ == '__main__':
#     unittest.main()