

class Card:
    def __init__(self, name, production, basePay, wells, property):
        self.name = name
        self.production = production
        self.basePay = basePay
        self.wells = wells if isinstance(wells, int) else wells[len(wells)-1]
        self.property = property

    def GetName(self):
        return self.name

    def HasProperty(self):
        return self.property

    def GetWells(self):
        return self.wells

    def GetProduction(self):
        return self.production

    def GetBasePay(self):
        return self.basePay
