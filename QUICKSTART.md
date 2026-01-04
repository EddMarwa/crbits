# Trading Account Management Platform - Quick Reference

## Quick Start

```python
from decimal import Decimal
from trading_account import TradingPlatform

# Create platform and account
platform = TradingPlatform()
account = platform.create_account('USER001', Decimal('1000.00'))

# Deposit
account.deposit(Decimal('500.00'))  # Returns new balance: 1500.00

# Withdraw
account.withdraw(Decimal('300.00'))  # Returns new balance: 1200.00

# Check balance
print(account.balance)  # 1200.00

# View history
history = account.get_transaction_history()
```

## Common Operations

### Create Account with Balance
```python
account = platform.create_account('USER001', Decimal('5000.00'))
```

### Create Account with Zero Balance
```python
account = platform.create_account('USER002')
```

### Deposit Money
```python
new_balance = account.deposit(Decimal('100.00'))
```

### Withdraw Money
```python
new_balance = account.withdraw(Decimal('50.00'))
```

### Get Account Information
```python
info = account.get_account_info()
# Returns: {'account_id', 'balance', 'created_at', 'transaction_count'}
```

### View Transaction History
```python
history = account.get_transaction_history()
for trans in history:
    print(f"{trans['type']}: ${trans['amount']}")
```

### List All Accounts
```python
all_accounts = platform.list_accounts()
for acc in all_accounts:
    print(f"{acc['account_id']}: ${acc['balance']}")
```

## Error Handling

### Insufficient Funds
```python
try:
    account.withdraw(Decimal('10000.00'))
except InsufficientFundsError as e:
    print(f"Error: {e}")
```

### Invalid Amount
```python
try:
    account.deposit(Decimal('-100.00'))
except InvalidAmountError as e:
    print(f"Error: {e}")
```

## Best Practices

1. **Always use Decimal**: Never use float for monetary values
   ```python
   # Good
   account.deposit(Decimal('100.00'))
   
   # Bad - avoid
   account.deposit(100.0)
   ```

2. **Handle exceptions**: Always wrap operations in try-except
   ```python
   try:
       account.withdraw(amount)
   except (InsufficientFundsError, InvalidAmountError) as e:
       print(f"Transaction failed: {e}")
   ```

3. **Validate before operations**: Check balance before withdrawal
   ```python
   if amount <= account.balance:
       account.withdraw(amount)
   else:
       print("Insufficient funds")
   ```

## Testing

Run all tests:
```bash
python -m unittest test_trading_account.py -v
```

Run specific test class:
```bash
python -m unittest test_trading_account.TestTradingAccount -v
```

## Demo

Run the interactive demo:
```bash
python demo.py
```

## Common Use Cases

### Transfer Between Accounts
```python
def transfer(from_account, to_account, amount):
    """Transfer money between accounts."""
    try:
        from_account.withdraw(amount)
        to_account.deposit(amount)
        return True
    except (InsufficientFundsError, InvalidAmountError) as e:
        print(f"Transfer failed: {e}")
        return False

# Usage
transfer(alice, bob, Decimal('100.00'))
```

### Calculate Total Platform Balance
```python
total = sum(Decimal(acc['balance']) for acc in platform.list_accounts())
```

### Find Account by ID
```python
account = platform.get_account('USER001')
if account:
    print(f"Found: {account.account_id}")
else:
    print("Account not found")
```

## Important Notes

- All amounts are automatically rounded to 2 decimal places
- Negative balances are not allowed
- Account IDs must be unique within a platform
- Transaction history is maintained permanently
- Withdrawals fail if amount exceeds balance
- Deposits and withdrawals must be positive amounts
