import unittest
import uuid
from bank.bank import Customer

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
