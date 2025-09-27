# Command-Line Banking Application

## Project Overview

This project is a comprehensive, command-line interface (CLI) banking application built entirely in Python. Using only numbers for better User experience. It demonstrates core software engineering principles, including Object-Oriented Programming (OOP), reliable file saving, and a focus on unit testing.

The application simulates a real-world banking system where cashiers can manage customer accounts. All customer and account data is persistently stored and retrieved from .csv file.

## Core Features:

- Customer Account Management: Add new customers with checking and savings account.

- Secure Authentication: A customer login system to access their accounts.

- Standard Banking Operations: Deposit, withdrawal and transfer (internal, between a customer own accounts and external, to other customer account).

- An Overdraft Protection: A rule-based overdraft system for checking account and account deactivation/reactivation logic.

- An Exception handling: Implement custom exceptions to handle business logic errors giving the user a clear feedback.

- Unit Test: Implement  unit tests using Python unittest framework to make sure that everything is reliable and correct.



## Code Snippet: 
transfer_external method:
```
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
```
  

## What I Learned from This Project:

- Unit Testing: I learned the importance of unit testing to ensure the quality of the code and avoid bugs in the future. 
After implementing the core features, I wrote specific tests with the Python unittest framework to each functionality (e.g. testoverdraftdenied, test_login).

- Object-Oriented Architecture: It is achieved by creating a clear class structure which is well-defined and separates responsibilities. The Bank class provides the overall control, while the BankAccount, CheckingAccount and SavingsAccount classes implement the details of logic and data of each account type.

- Strong Error Handling: I re-engineered the whole application from a return True/False system to a custom exception hierarchy. This created a cleaner division between business logic and the user interface that made the code much easier to maintain and debug. 

- Reliable CSV File Handling: I learned to write code that is robust to handle an application data using Python csv module. My implementation is backward-compatible, its a safe way of handling files with missing columns by using default values to avoid crashes


## What am plaining to do for Future Enhancements:

- Display Transaction Data: Implement a system that records all transactions in to a separate transactions.csv file so that the customer can see all account activity.

- Password Strength Checker: enforce stronger password requirements when creating a customer to increase account security.




