class Player:
    """
        Class Player represents a player in a game.
    """
    def __init__(self, name):
        self.BankAccount = None
        self.Properties = {}
        self.Name = name

    def SetBankAccount(self, account):
        self.BankAccount = account

    def GetBankAccount(self):
        return self.BankAccount

    def GetName(self):
        return self.Name

    def GetProperties(self):
        return self.Properties

    def BankruptStatus(self):
        if self.BankAccount.GetBalance() > 0:
            return False
        else:
            return True

    def AddProperty(self, property):
        self.Properties[property.GetName()] = property

    def RemoveProperty(self, property):
        del self.Properties[property.GetName()]

    def GetTotalOil(self):
        totalOil = 0
        for property in self.Properties:
            totalOil += len(property.GetOilHits())
        return totalOil
