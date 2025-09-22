import unittest
from bank.bank import Customer

class TestCustomer(unittest.TestCase):
    def test_create_customer_object(self):
        self.customer = Customer('Deem', 'alqasir', 'password')
        self.assertEqual(self.customer.first_name,'Deem')
        self.assertEqual(self.customer.last_name,'alqasir')
        self.assertEqual(self.customer.password,'password')