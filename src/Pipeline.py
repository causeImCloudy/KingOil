
class Pipeline:
    def __init__(self, fromProperty, toProperty):
        self.fromProperty = fromProperty
        self.toProperty = toProperty
        self.Level = 1

    def AddLevel(self):
        """
            Pipelines max out at 3 on the board game, and represented by level 3 here.
        """
        if self.Level >= 3:
            raise RuntimeError("Pipeline Level Maxed")
        else:
            self.Level += 1

    def GetLevel(self):
        # Levels are 1,2,3
        return self.Level

    def GetFromProperty(self):
        return self.fromProperty

    def GetToProperty(self):
        return self.toProperty
