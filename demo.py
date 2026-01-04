#!/usr/bin/env python3
"""
Trading Account Management Platform - Command Line Interface

Example usage of the trading account management system.
"""

from decimal import Decimal
from trading_account import TradingPlatform, InsufficientFundsError, InvalidAmountError


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_account_info(account):
    """Print account information in a formatted way."""
    info = account.get_account_info()
    print(f"Account ID: {info['account_id']}")
    print(f"Balance: ${info['balance']}")
    print(f"Created: {info['created_at']}")
    print(f"Transactions: {info['transaction_count']}")


def print_transaction_history(account):
    """Print transaction history."""
    history = account.get_transaction_history()
    if not history:
        print("No transactions yet.")
        return
    
    print("\nTransaction History:")
    print(f"{'Type':<15} {'Amount':<15} {'Balance After':<15} {'Timestamp':<25}")
    print("-" * 70)
    
    for trans in history:
        print(f"{trans['type']:<15} ${trans['amount']:<14} ${trans['balance_after']:<14} {trans['timestamp'][:19]}")


def main():
    """Run the trading platform demo."""
    print_header("Trading Account Management Platform - Demo")
    
    # Initialize platform
    platform = TradingPlatform()
    print("✓ Platform initialized\n")
    
    # Create accounts
    print_header("Creating User Accounts")
    
    alice = platform.create_account('ALICE001', Decimal('5000.00'))
    print("✓ Created account for Alice with $5,000 initial balance")
    
    bob = platform.create_account('BOB002', Decimal('3000.00'))
    print("✓ Created account for Bob with $3,000 initial balance")
    
    charlie = platform.create_account('CHARLIE003')
    print("✓ Created account for Charlie with $0 initial balance")
    
    # Display account info
    print_header("Account Information - Alice")
    print_account_info(alice)
    
    # Perform deposits
    print_header("Deposit Operations")
    
    print("Alice deposits $1,500...")
    alice.deposit(Decimal('1500.00'))
    print(f"✓ New balance: ${alice.balance}\n")
    
    print("Bob deposits $2,000...")
    bob.deposit(Decimal('2000.00'))
    print(f"✓ New balance: ${bob.balance}\n")
    
    print("Charlie deposits $1,000...")
    charlie.deposit(Decimal('1000.00'))
    print(f"✓ New balance: ${charlie.balance}")
    
    # Perform withdrawals
    print_header("Withdrawal Operations")
    
    print("Alice withdraws $2,000...")
    alice.withdraw(Decimal('2000.00'))
    print(f"✓ New balance: ${alice.balance}\n")
    
    print("Bob withdraws $1,500...")
    bob.withdraw(Decimal('1500.00'))
    print(f"✓ New balance: ${bob.balance}")
    
    # Demonstrate error handling
    print_header("Error Handling Examples")
    
    print("Attempting to withdraw more than balance (Charlie)...")
    try:
        charlie.withdraw(Decimal('2000.00'))
    except InsufficientFundsError as e:
        print(f"✗ Error: {e}\n")
    
    print("Attempting to deposit negative amount (Alice)...")
    try:
        alice.deposit(Decimal('-100.00'))
    except InvalidAmountError as e:
        print(f"✗ Error: {e}\n")
    
    print("Attempting to withdraw zero (Bob)...")
    try:
        bob.withdraw(Decimal('0'))
    except InvalidAmountError as e:
        print(f"✗ Error: {e}")
    
    # Show transaction history
    print_header("Transaction History - Alice")
    print_transaction_history(alice)
    
    # List all accounts
    print_header("All Platform Accounts")
    accounts = platform.list_accounts()
    
    print(f"Total accounts: {len(accounts)}\n")
    for acc_info in accounts:
        print(f"  {acc_info['account_id']}: ${acc_info['balance']} ({acc_info['transaction_count']} transactions)")
    
    # Final summary
    print_header("Demo Complete")
    total_balance = sum(Decimal(acc['balance']) for acc in accounts)
    print(f"Total platform balance: ${total_balance}")
    print("\nThe trading account management platform is working correctly! ✓\n")


if __name__ == '__main__':
    main()
