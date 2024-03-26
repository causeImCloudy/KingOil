MAXBANK = 1000000
ACCOUNTSTART = 80000

class Bank: 
    def __init__(self):
        self.Bank = Account("Bank", MAXBANK)
        self.accounts = []
        
    def NewPlayer(self, player):
        '''
            Constructor Function that creates a new bank account, transfers the standard starting money
            to the player, and assigns the bank accounts
        '''
        account = Account(player.GetName())
        
        player.SetBankAccount(account)
        
        self.TransferMoney(self.Bank, account, ACCOUNTSTART)
        
        self.accounts.append(account)
        
        return account

    def TransferMoney(self, fromAcct, toAcct, price, forcePurchase=False):
        """
            First Calculates if a transaction can happen, then transfers the money.

            If price is more then account balance and force purchase is on (used in pipline royalties)
            then it forces the purchase of the remaining balance and bankrupts the player.

            The bank as a final measure is allowed to pay out a single person(i.e. 4k per well = 100k bank has 20k
            bank will still pay you 100k). To do this we exclude the account named bank, then check
            for balances < 1 incase there's multiple transactions in one turn before the win conditions are checked.
        """

        if price > fromAcct.GetBalance() and forcePurchase and fromAcct.GetName() != "Bank":
            price = fromAcct.GetBalance()
        elif price > fromAcct.GetBalance() and fromAcct.GetName() != "Bank":
            raise ArithmeticError("Insufficient Funds") 
        elif fromAcct.GetBalance() < 1:
            raise ArithmeticError("Insufficient Funds")
        
        fromAcct.SubBalance(price)
        toAcct.AddBalance(price)
        
    def GetAccounts(self):
        return self.accounts
    
    def GetBankBalance(self):
        return self.Bank.GetBalance()


class Account:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
    
    def AddBalance(self, amount):
        self.balance += amount
        return self.GetBalance()
        
    def SubBalance(self, amount):
        self.balance -= amount
        return self.GetBalance()
    
    def GetBalance(self):
        return self.balance
    
    def GetName(self):
        return self.name