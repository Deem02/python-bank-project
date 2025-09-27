import unittest
import tempfile
import os
from unittest.mock import patch
from bank.bank import Customer, BankAccount, CheckingAccount, SavingsAccount, Bank, InvalidAmountError, InsufficientFundsError, OverdraftLimitError

class TestCustomer(unittest.TestCase):
    def test_create_customer_object(self):
        self.customer = Customer(1001,'Deem', 'alqasir', 'password')
        self.assertEqual(self.customer.first_name,'Deem')
        self.assertEqual(self.customer.last_name,'alqasir')
        self.assertEqual(self.customer.password,'password')
        self.assertEqual(self.customer.account_id, 1001 )
    

class TestBankAccountAndSubclass(unittest.TestCase):
    
    def setUp(self): 
        self.customer = Customer(1002,'Arwa', 'alslam', 'password1')
        self.checking = CheckingAccount(self.customer, balance=1500) 
        self.savings = SavingsAccount(self.customer, balance=500) 
        
    def test_account_creation(self):
        self.assertEqual(self.checking.balance, 1500.0)
        self.assertEqual(self.savings.balance, 500)
    
        
    def test_deposit_valid(self):
        self.checking.deposit(100)
        self.assertEqual(self.checking.balance, 1600)
       
       
        
    def test_deposit_invalid_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.checking.deposit(-100)  
        self.assertEqual(self.checking.balance, 1500)
        
        with self.assertRaises(InvalidAmountError):
            self.savings.deposit(0)
        self.assertEqual(self.savings.balance,500)
          
    def test_withdraw_vailed(self):
        self.checking.withdraw(50)
        self.assertEqual(self.checking.balance, 1450)

        
    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError):
            self.savings.withdraw(600)
        self.assertEqual(self.savings.balance, 500) 


class TestChekingAccountOverdraft(unittest.TestCase):     
    def setUp(self):
        self.customer = Customer(1003,'dana', 'ahmed', 'password1') 
        self.cheking = CheckingAccount(self.customer, balance=50.0)
        
    def test_first_overdraft(self):
        with patch('sys.stdout'):
            self.cheking.withdraw(60)
        self.assertEqual(self.cheking.balance, -45.0) 
        self.assertEqual(self.cheking.overdraft_count, 1)
        self.assertTrue(self.cheking.is_active)
        
    def test_overdraft_denied(self):   
        with self.assertRaises(OverdraftLimitError):
            with patch('sys.stdout'):
                self.cheking.withdraw(200)
        self.assertEqual(self.cheking.balance, 50) 
        self.assertTrue(self.cheking.is_active)
        
    def test_second_overdraft(self):
        # self.test_first_overdraft()  # I can do it like this but each test should be isolated 
        with patch('sys.stdout'):
            self.cheking.withdraw(60)
        self.assertEqual(self.cheking.balance, -45.0) 
        self.assertEqual(self.cheking.overdraft_count, 1)
        with patch('sys.stdout'):
            self.cheking.withdraw(20)
        self.assertEqual(self.cheking.overdraft_count, 2)
        self.assertFalse(self.cheking.is_active)
                 
                 
class TestBank(unittest.TestCase):
    def setUp(self):
        self.temp_file =  tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.test_file_path = self.temp_file.name
        self.temp_file.close()
        self.bank = Bank(filename=self.test_file_path)
    def tearDown(self):
        os.remove(self.test_file_path)
        
    def test_add_and_save_customer(self):
        with patch('sys.stdout'):
            self.bank.add_customer('mohamed', 'alahmed', 'pass321', checking_balance=2000, savings_balance=200)
        self.assertIn(1001,self.bank.customers)
        new_bank_instance = Bank(filename=self.test_file_path)
        self.assertEqual(len(new_bank_instance.customers), 1)
        loaded_customer = new_bank_instance.customers.get(1001)
        self.assertEqual(loaded_customer.first_name, 'mohamed')
        self.assertEqual(loaded_customer.last_name, 'alahmed')
        self.assertEqual(loaded_customer.checking_account.balance, 2000)
        self.assertEqual(loaded_customer.savings_account.balance, 200)
        
        
    @patch('builtins.input')    
    def test_login(self,mock_input):
        with patch('sys.stdout'): 
            self.bank.add_customer('mohamed', 'alahmed', 'pass321')
            mock_input.side_effect=[1001,'pass321'] 
            self.bank.login() 
        self.assertIsNotNone(self.bank.current_customer)
        self.assertEqual(self.bank.current_customer.account_id, 1001)
        self.assertEqual(self.bank.current_customer.first_name, 'mohamed')
        

#python -m unittest --buffer  tests.test_bank # to hidden the print output      
#python -m unittest  tests.test_bank
# if __name__ == '__main__':
#     unittest.main()