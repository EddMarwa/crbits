"""
Unit tests for Trading Account Management Platform
"""

import unittest
from decimal import Decimal
from datetime import datetime
from trading_account import (
    TradingAccount,
    TradingPlatform,
    Transaction,
    InsufficientFundsError,
    InvalidAmountError
)


class TestTransaction(unittest.TestCase):
    """Test cases for Transaction class."""
    
    def test_transaction_creation(self):
        """Test creating a transaction."""
        amount = Decimal('100.00')
        balance = Decimal('500.00')
        transaction = Transaction('deposit', amount, balance)
        
        self.assertEqual(transaction.transaction_type, 'deposit')
        self.assertEqual(transaction.amount, amount)
        self.assertEqual(transaction.balance_after, balance)
        self.assertIsInstance(transaction.timestamp, datetime)
    
    def test_transaction_to_dict(self):
        """Test converting transaction to dictionary."""
        transaction = Transaction('withdrawal', Decimal('50.00'), Decimal('450.00'))
        trans_dict = transaction.to_dict()
        
        self.assertEqual(trans_dict['type'], 'withdrawal')
        self.assertEqual(trans_dict['amount'], '50.00')
        self.assertEqual(trans_dict['balance_after'], '450.00')
        self.assertIn('timestamp', trans_dict)


class TestTradingAccount(unittest.TestCase):
    """Test cases for TradingAccount class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.account = TradingAccount('TEST001', Decimal('1000.00'))
    
    def test_account_creation(self):
        """Test creating a new account."""
        account = TradingAccount('TEST002')
        self.assertEqual(account.account_id, 'TEST002')
        self.assertEqual(account.balance, Decimal('0'))
    
    def test_account_creation_with_initial_balance(self):
        """Test creating account with initial balance."""
        account = TradingAccount('TEST003', Decimal('500.00'))
        self.assertEqual(account.balance, Decimal('500.00'))
    
    def test_account_creation_negative_balance(self):
        """Test that negative initial balance raises error."""
        with self.assertRaises(InvalidAmountError):
            TradingAccount('TEST004', Decimal('-100.00'))
    
    def test_deposit_success(self):
        """Test successful deposit."""
        initial_balance = self.account.balance
        deposit_amount = Decimal('250.00')
        new_balance = self.account.deposit(deposit_amount)
        
        self.assertEqual(new_balance, initial_balance + deposit_amount)
        self.assertEqual(self.account.balance, Decimal('1250.00'))
    
    def test_deposit_zero_amount(self):
        """Test that depositing zero raises error."""
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(Decimal('0'))
    
    def test_deposit_negative_amount(self):
        """Test that depositing negative amount raises error."""
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(Decimal('-50.00'))
    
    def test_deposit_rounding(self):
        """Test that deposit amount is rounded to 2 decimal places."""
        self.account.deposit(Decimal('10.999'))
        # Should round down to 10.99
        self.assertEqual(self.account.balance, Decimal('1010.99'))
    
    def test_withdraw_success(self):
        """Test successful withdrawal."""
        initial_balance = self.account.balance
        withdraw_amount = Decimal('300.00')
        new_balance = self.account.withdraw(withdraw_amount)
        
        self.assertEqual(new_balance, initial_balance - withdraw_amount)
        self.assertEqual(self.account.balance, Decimal('700.00'))
    
    def test_withdraw_exact_balance(self):
        """Test withdrawing exact balance."""
        balance = self.account.balance
        self.account.withdraw(balance)
        self.assertEqual(self.account.balance, Decimal('0'))
    
    def test_withdraw_insufficient_funds(self):
        """Test that withdrawing more than balance raises error."""
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(Decimal('2000.00'))
    
    def test_withdraw_zero_amount(self):
        """Test that withdrawing zero raises error."""
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(Decimal('0'))
    
    def test_withdraw_negative_amount(self):
        """Test that withdrawing negative amount raises error."""
        with self.assertRaises(InvalidAmountError):
            self.account.withdraw(Decimal('-50.00'))
    
    def test_multiple_deposits(self):
        """Test multiple deposits."""
        self.account.deposit(Decimal('100.00'))
        self.account.deposit(Decimal('200.00'))
        self.account.deposit(Decimal('50.00'))
        
        self.assertEqual(self.account.balance, Decimal('1350.00'))
    
    def test_multiple_withdrawals(self):
        """Test multiple withdrawals."""
        self.account.withdraw(Decimal('100.00'))
        self.account.withdraw(Decimal('200.00'))
        self.account.withdraw(Decimal('50.00'))
        
        self.assertEqual(self.account.balance, Decimal('650.00'))
    
    def test_deposit_and_withdraw_combination(self):
        """Test combination of deposits and withdrawals."""
        self.account.deposit(Decimal('500.00'))  # 1500
        self.account.withdraw(Decimal('200.00'))  # 1300
        self.account.deposit(Decimal('100.00'))  # 1400
        self.account.withdraw(Decimal('300.00'))  # 1100
        
        self.assertEqual(self.account.balance, Decimal('1100.00'))
    
    def test_transaction_history(self):
        """Test transaction history tracking."""
        self.account.deposit(Decimal('100.00'))
        self.account.withdraw(Decimal('50.00'))
        
        history = self.account.get_transaction_history()
        # Should have initial + 2 transactions
        self.assertEqual(len(history), 3)
        self.assertEqual(history[1]['type'], 'deposit')
        self.assertEqual(history[2]['type'], 'withdrawal')
    
    def test_get_account_info(self):
        """Test getting account information."""
        info = self.account.get_account_info()
        
        self.assertEqual(info['account_id'], 'TEST001')
        self.assertEqual(info['balance'], '1000.00')
        self.assertIn('created_at', info)
        self.assertIn('transaction_count', info)


class TestTradingPlatform(unittest.TestCase):
    """Test cases for TradingPlatform class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.platform = TradingPlatform()
    
    def test_platform_creation(self):
        """Test creating a new platform."""
        platform = TradingPlatform()
        self.assertEqual(len(platform.list_accounts()), 0)
    
    def test_create_account(self):
        """Test creating an account on the platform."""
        account = self.platform.create_account('USER001')
        
        self.assertIsInstance(account, TradingAccount)
        self.assertEqual(account.account_id, 'USER001')
        self.assertEqual(account.balance, Decimal('0'))
    
    def test_create_account_with_initial_balance(self):
        """Test creating account with initial balance."""
        account = self.platform.create_account('USER002', Decimal('1000.00'))
        self.assertEqual(account.balance, Decimal('1000.00'))
    
    def test_create_duplicate_account(self):
        """Test that creating duplicate account raises error."""
        self.platform.create_account('USER003')
        
        with self.assertRaises(ValueError):
            self.platform.create_account('USER003')
    
    def test_get_account(self):
        """Test retrieving an account."""
        created_account = self.platform.create_account('USER004', Decimal('500.00'))
        retrieved_account = self.platform.get_account('USER004')
        
        self.assertEqual(created_account, retrieved_account)
        self.assertEqual(retrieved_account.balance, Decimal('500.00'))
    
    def test_get_nonexistent_account(self):
        """Test retrieving nonexistent account returns None."""
        account = self.platform.get_account('NONEXISTENT')
        self.assertIsNone(account)
    
    def test_list_accounts(self):
        """Test listing all accounts."""
        self.platform.create_account('USER005', Decimal('100.00'))
        self.platform.create_account('USER006', Decimal('200.00'))
        self.platform.create_account('USER007', Decimal('300.00'))
        
        accounts = self.platform.list_accounts()
        self.assertEqual(len(accounts), 3)
    
    def test_platform_integration(self):
        """Test complete platform workflow."""
        # Create account
        account = self.platform.create_account('USER008', Decimal('1000.00'))
        
        # Perform operations
        account.deposit(Decimal('500.00'))
        account.withdraw(Decimal('300.00'))
        
        # Verify through platform
        retrieved = self.platform.get_account('USER008')
        self.assertEqual(retrieved.balance, Decimal('1200.00'))
        
        # Check transaction history
        history = retrieved.get_transaction_history()
        self.assertEqual(len(history), 3)  # initial + deposit + withdrawal


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_large_amount_deposit(self):
        """Test depositing very large amount."""
        account = TradingAccount('TEST_LARGE')
        account.deposit(Decimal('999999999.99'))
        self.assertEqual(account.balance, Decimal('999999999.99'))
    
    def test_small_amount_operations(self):
        """Test operations with very small amounts."""
        account = TradingAccount('TEST_SMALL', Decimal('1.00'))
        account.deposit(Decimal('0.01'))
        self.assertEqual(account.balance, Decimal('1.01'))
        
        account.withdraw(Decimal('0.01'))
        self.assertEqual(account.balance, Decimal('1.00'))
    
    def test_zero_balance_account(self):
        """Test operations on zero balance account."""
        account = TradingAccount('TEST_ZERO')
        self.assertEqual(account.balance, Decimal('0'))
        
        with self.assertRaises(InsufficientFundsError):
            account.withdraw(Decimal('0.01'))
        
        account.deposit(Decimal('10.00'))
        self.assertEqual(account.balance, Decimal('10.00'))


if __name__ == '__main__':
    unittest.main()
