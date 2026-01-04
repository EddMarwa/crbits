# crbits - Trading Account Management Platform

A robust trading account management platform that enables users to manage their trading accounts with deposit and withdrawal functionality.

## Features

- **Account Management**: Create and manage multiple trading accounts
- **Deposit Operations**: Add funds to trading accounts with validation
- **Withdrawal Operations**: Withdraw funds with balance verification
- **Transaction History**: Track all account transactions with timestamps
- **Error Handling**: Comprehensive validation and error messages
- **Decimal Precision**: Uses Decimal type for accurate financial calculations

## Installation

No external dependencies required. The platform uses Python's standard library.

Requirements:
- Python 3.6 or higher

## Usage

### Basic Example

```python
from decimal import Decimal
from trading_account import TradingPlatform

# Initialize the platform
platform = TradingPlatform()

# Create a new account with initial balance
account = platform.create_account('USER001', Decimal('1000.00'))

# Deposit funds
account.deposit(Decimal('500.00'))
print(f"Balance after deposit: ${account.balance}")  # $1500.00

# Withdraw funds
account.withdraw(Decimal('300.00'))
print(f"Balance after withdrawal: ${account.balance}")  # $1200.00

# View transaction history
history = account.get_transaction_history()
for transaction in history:
    print(transaction)
```

### Running the Demo

```bash
python demo.py
```

This will run a comprehensive demonstration of all platform features.

### Running Tests

```bash
python -m unittest test_trading_account.py
```

Or run with verbose output:

```bash
python -m unittest test_trading_account.py -v
```

## API Reference

### TradingPlatform

Main platform class for managing multiple accounts.

**Methods:**
- `create_account(account_id, initial_balance=0)` - Create a new trading account
- `get_account(account_id)` - Retrieve an account by ID
- `list_accounts()` - List all accounts on the platform

### TradingAccount

Individual trading account with deposit/withdrawal capabilities.

**Methods:**
- `deposit(amount)` - Deposit funds into the account
- `withdraw(amount)` - Withdraw funds from the account
- `get_transaction_history()` - Get all transactions
- `get_account_info()` - Get account summary

**Properties:**
- `balance` - Current account balance (read-only)
- `account_id` - Unique account identifier

### Exceptions

- `InsufficientFundsError` - Raised when withdrawal exceeds balance
- `InvalidAmountError` - Raised when deposit/withdrawal amount is invalid

## Examples

### Creating Multiple Accounts

```python
platform = TradingPlatform()

alice = platform.create_account('ALICE', Decimal('5000.00'))
bob = platform.create_account('BOB', Decimal('3000.00'))
charlie = platform.create_account('CHARLIE')  # Zero balance
```

### Handling Errors

```python
try:
    account.withdraw(Decimal('10000.00'))
except InsufficientFundsError as e:
    print(f"Cannot withdraw: {e}")

try:
    account.deposit(Decimal('-100.00'))
except InvalidAmountError as e:
    print(f"Invalid amount: {e}")
```

### Transaction History

```python
account.deposit(Decimal('100.00'))
account.withdraw(Decimal('50.00'))

history = account.get_transaction_history()
for trans in history:
    print(f"{trans['type']}: ${trans['amount']} at {trans['timestamp']}")
```

## Design Principles

1. **Precision**: Uses Python's `Decimal` type to avoid floating-point arithmetic issues in financial calculations
2. **Validation**: All operations validate inputs before executing
3. **Immutability**: Balance cannot be directly modified; only through deposit/withdraw
4. **Audit Trail**: Complete transaction history maintained for all operations
5. **Error Handling**: Clear, specific exceptions for different error conditions

## Security Considerations

- All amounts are rounded to 2 decimal places (currency standard)
- Negative amounts are rejected
- Balance cannot go negative (withdrawal validation)
- Account IDs must be unique per platform

## License

This project is open source.

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting pull requests.