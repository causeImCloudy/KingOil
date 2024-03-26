import random

class RandomizationDisk:

    def __init__(self, board, positions=None, leadSpoke=1):
        self.SpokeOffset = 0
        self.LeadSpoke = leadSpoke
        self.Positions = positions
        self.Board = board

        self._makeHashMap()
        self._shuffle()

    def _makeHashMap(self):
        self.HashMap = {position: True for position in self.GetPositions()}

    def _shuffle(self):
        """
            This function shuffles individual disks to map the offset to the notch. This should be run for each disk
            and mapped back to the offset
        """
        self.SetNotch(
            random.SystemRandom().randint(1, (self.Board.SpokeTotal / self.Board.SpokeSpacing))
        )

    def SetNotch(self, notch):
        """
            Validates and Assigns the notch based on selection so that it accurately represents the total positions
            each disk could be in. Represented by the Total Spokes / spaces of the spokes = total positions.
        """
        if notch > (self.Board.SpokeTotal / self.Board.SpokeSpacing):
            raise RuntimeError("Invalid notch")

        SpokeOffSet = (notch - 1) * self.Board.SpokeSpacing + self.LeadSpoke

        self.SetSpokeOffset(self.Board.BoardLeadSpoke - SpokeOffSet)

    def SetSpokeOffset(self, offset):
        self.SpokeOffset = offset

    def GetSpokeOffset(self):
        return self.SpokeOffset

    def GetPositions(self):
        return self.Positions

    def GetStatistics(self):
        stats = {"length": len(self.GetPositions()), "oil_by_ring": {}, "oil_by_spoke": {}}

        for hit in self.GetPositions():
            stats["oil_by_ring"][str(hit[1])] = 1 if not stats["oil_by_ring"].get(str(hit[1])) else \
                stats["oil_by_ring"][str(hit[1])] + 1
            stats["oil_by_spoke"][str(hit[0])] = 1 if not stats["oil_by_spoke"].get(str(hit[0])) else \
                stats["oil_by_spoke"][str(hit[0])] + 1

        return stats

    def CheckHashMap(self, spoke, ring):
        return self.HashMap.get((spoke, ring), False)