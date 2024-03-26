class Property:
    """
        Property class.
        Positions = {
            "(x,y)" : True/False/Nil
        }

    """
    def __init__(self, name, price, adjacentProperties, positions):
        self.Name = str(name)
        self.Price = price
        self.AdjacentProperties = adjacentProperties
        self.Positions = {key: None for key in positions}

        self.GoodPipeline = []
        self.BadPipeline = []
        self.OilHits = 0

        self.Owner = None

    def GetName(self):
        return self.Name

    def GetGoodPipeline(self):
        """
            Returns *Good* pipelines or pipelines that owe this property money
        """
        return self.GoodPipeline

    def GetBadPipeline(self):
        """
            Returns *Bad* pipelines or pipelines this property owes money on
        """
        return self.BadPipeline

    def AddGoodPipeline(self, pipeline, level):
        """
            Verifies you can purchase a pipeline and adds it.
            Pipelines require oil hits/derricks:
            4 for level 1
            5 for level 2
            6 for level 3
        """
        numberOilHits = len(self.GetOilHits())

        if level in [2, 3] and numberOilHits >= level + 3:
            pipeline.AddLevel()
        elif level == 1 and numberOilHits >= 4:
            self.GoodPipeline.append(pipeline)

    def AddBadPipeline(self, pipeline):

        if pipeline.GetFromProperty() in [pipe.GetFromProperty() for pipe in self.GetBadPipeline()]:
            raise RuntimeError("Pipeline already exists in array")

        self.BadPipeline.append(pipeline)

    def GetOilHits(self):
        return [prop for prop in self.Positions if self.Positions[prop] is True]

    def GetOwner(self):
        return self.Owner

    def SetOwner(self, newOwner):
        self.Owner = newOwner

    def GetOpenPositions(self):
        return [pos for pos in self.Positions if self.Positions[pos] is None]

    def GetOilHitPositions(self):
        return [pos for pos in self.Positions if self.Positions[pos] is True]

    def SetOilHitPosition(self, position, oil=True):
        self.Positions[position] = oil

    def GetPrice(self):
        return self.Price
