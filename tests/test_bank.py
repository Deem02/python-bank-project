import unittest
import uuid
from bank.bank import Customer, BankAccount, CheckingAccount, SavingsAccount, Bank

class TestCustomer(unittest.TestCase):
    def test_create_customer_object(self):
        self.customer = Customer('Deem', 'alqasir', 'password')
        self.assertEqual(self.customer.first_name,'Deem')
        self.assertEqual(self.customer.last_name,'alqasir')
        self.assertEqual(self.customer.password,'password')
        self.assertIsInstance(self.customer.customer_id, uuid.UUID )
        self.assertEqual(self.customer.accounts, [])
        
    def test_add_account(self):
        customer = Customer('Dana', 'alaile', 'password21')
        account = 'Account object'
        customer.add_account(account)
        self.assertIn(account, customer.accounts)
        self.assertEqual(len(customer.accounts), 1)
       
class TestBankAccountAndSubclass(unittest.TestCase):
    def setUp(self):
        BankAccount.account_number_counter = 1001
        self.customer = Customer('Arwa', 'alslam', 'password1')
        self.checking = CheckingAccount(self.customer, balance=1500) 
        self.savings = SavingsAccount(self.customer, balance=500) 
        
    def test_account_creation(self):
        self.assertEqual(self.checking.balance, 1500)
        self.assertEqual(self.savings.balance, 500)
        self.assertEqual(self.checking.account_number, 1001)
        self.assertEqual(self.savings.account_number, 1002)
        
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
        self.checking.withdraw(-100)
        self.assertEqual(self.checking.balance, 1450)
        
        self.savings.withdraw(500)
        self.assertEqual(self.savings.balance,0)
        self.savings.withdraw(0)
        self.assertEqual(self.savings.balance,0)
        
class TestBank(unittest.TestCas):
    pass
