"""
Trading Account Management Platform
Handles user accounts with deposit and withdrawal functionality.
"""

from datetime import datetime
from typing import List, Dict, Optional
from decimal import Decimal, ROUND_DOWN


class InsufficientFundsError(Exception):
    """Raised when withdrawal amount exceeds available balance."""
    pass


class InvalidAmountError(Exception):
    """Raised when deposit or withdrawal amount is invalid."""
    pass


class Transaction:
    """Represents a single transaction in a trading account."""
    
    def __init__(self, transaction_type: str, amount: Decimal, balance_after: Decimal, timestamp: Optional[datetime] = None):
        """
        Initialize a transaction.
        
        Args:
            transaction_type: Type of transaction ('deposit' or 'withdrawal')
            amount: Transaction amount
            balance_after: Account balance after transaction
            timestamp: Time of transaction (defaults to current time)
        """
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary format."""
        return {
            'type': self.transaction_type,
            'amount': str(self.amount),
            'balance_after': str(self.balance_after),
            'timestamp': self.timestamp.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"Transaction({self.transaction_type}, {self.amount}, {self.timestamp})"


class TradingAccount:
    """
    Trading account with deposit and withdrawal capabilities.
    
    Maintains account balance and transaction history.
    """
    
    def __init__(self, account_id: str, initial_balance: Decimal = Decimal('0')):
        """
        Initialize a trading account.
        
        Args:
            account_id: Unique identifier for the account
            initial_balance: Starting balance (defaults to 0)
        
        Raises:
            InvalidAmountError: If initial balance is negative
        """
        if initial_balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative")
        
        self.account_id = account_id
        self._balance = initial_balance
        self._transactions: List[Transaction] = []
        self._created_at = datetime.now()
        
        if initial_balance > 0:
            self._transactions.append(
                Transaction('initial', initial_balance, initial_balance, self._created_at)
            )
    
    @property
    def balance(self) -> Decimal:
        """Get current account balance."""
        return self._balance
    
    def deposit(self, amount: Decimal) -> Decimal:
        """
        Deposit funds into the account.
        
        Args:
            amount: Amount to deposit
        
        Returns:
            New balance after deposit
        
        Raises:
            InvalidAmountError: If amount is not positive
        """
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        
        # Round to 2 decimal places for currency
        amount = amount.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        self._balance += amount
        transaction = Transaction('deposit', amount, self._balance)
        self._transactions.append(transaction)
        
        return self._balance
    
    def withdraw(self, amount: Decimal) -> Decimal:
        """
        Withdraw funds from the account.
        
        Args:
            amount: Amount to withdraw
        
        Returns:
            New balance after withdrawal
        
        Raises:
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If amount exceeds available balance
        """
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive")
        
        # Round to 2 decimal places for currency
        amount = amount.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Insufficient funds: attempting to withdraw {amount}, but balance is {self._balance}"
            )
        
        self._balance -= amount
        transaction = Transaction('withdrawal', amount, self._balance)
        self._transactions.append(transaction)
        
        return self._balance
    
    def get_transaction_history(self) -> List[Dict]:
        """
        Get complete transaction history for the account.
        
        Returns:
            List of transactions in dictionary format
        """
        return [t.to_dict() for t in self._transactions]
    
    def get_account_info(self) -> Dict:
        """
        Get account summary information.
        
        Returns:
            Dictionary containing account details
        """
        return {
            'account_id': self.account_id,
            'balance': str(self._balance),
            'created_at': self._created_at.isoformat(),
            'transaction_count': len(self._transactions)
        }
    
    def __repr__(self) -> str:
        return f"TradingAccount(id={self.account_id}, balance={self._balance})"


class TradingPlatform:
    """
    Trading platform that manages multiple user accounts.
    """
    
    def __init__(self):
        """Initialize the trading platform."""
        self._accounts: Dict[str, TradingAccount] = {}
    
    def create_account(self, account_id: str, initial_balance: Decimal = Decimal('0')) -> TradingAccount:
        """
        Create a new trading account.
        
        Args:
            account_id: Unique identifier for the account
            initial_balance: Starting balance (defaults to 0)
        
        Returns:
            The newly created trading account
        
        Raises:
            ValueError: If account already exists
        """
        if account_id in self._accounts:
            raise ValueError(f"Account {account_id} already exists")
        
        account = TradingAccount(account_id, initial_balance)
        self._accounts[account_id] = account
        return account
    
    def get_account(self, account_id: str) -> Optional[TradingAccount]:
        """
        Retrieve an account by ID.
        
        Args:
            account_id: Account identifier
        
        Returns:
            TradingAccount if found, None otherwise
        """
        return self._accounts.get(account_id)
    
    def list_accounts(self) -> List[Dict]:
        """
        List all accounts on the platform.
        
        Returns:
            List of account information dictionaries
        """
        return [account.get_account_info() for account in self._accounts.values()]
    
    def __repr__(self) -> str:
        return f"TradingPlatform(accounts={len(self._accounts)})"
