from src.RandomizationDisk import *
from src.Property import *


class Board:
    def __init__(self):

        """
            Each disk can be set in 12 different positions, leading to 4 spokes per position, which is consistent with
            the 12^3 calculation of possible final boards listed on Wikipedia.This section is mainly for debugging since
            I am reviewing this data off a picture of a 480p YouTube video. The LeadSpoke variable indicates at which
            spoke position on that specific disk >= 1 a *position notch* exists where the board could be locked in.
            This will be used to calculate the potential positions later.

            The following contains the blocked positions, or positive hits of oil, of the three disks of the classical
            board. Each tuple is an x,y pair of Spoke Count and ring number. The IRL board operates in a circle off the
            spinning disk, each spoke originates from the center. Each disk is made of 48 spokes, and 7 rings.
            ***These Number represents counted numbers and do not consider 0 as an actual space.***
        """

        self.BoardLeadSpoke = 25
        self.SpokeSpacing = 4
        self.SpokeTotal = 48
        self.RandomizationDisks = []

        # Positions for each disk level and which spoke is lead to align correctly and check oil hits
        ShallowPositions = [(1, 7), (2, 1), (2, 7), (4, 2), (6, 6), (7, 4), (7, 5), (7, 6), (8, 6), (9, 3), (12, 5),
                            (13, 1), (13, 5), (13, 6), (14, 6), (15, 2), (17, 2), (18, 3), (19, 2), (24, 1), (27, 2),
                            (29, 2), (31, 6), (32, 6), (33, 7), (34, 1), (34, 7), (35, 2), (35, 3), (37, 2), (38, 1),
                            (39, 7), (40, 2), (40, 5), (40, 6), (40, 7), (41, 7), (42, 1), (43, 2), (45, 2), (46, 3),
                            (48, 6), (48, 7)]
        MiddlePositions = [(1, 1), (3, 7), (4, 5), (4, 6), (4, 7), (7, 3), (8, 2), (8, 3), (9, 1), (10, 5), (10, 6),
                           (11, 5), (12, 2), (12, 6), (12, 7), (13, 1), (16, 2), (17, 1), (18, 2), (18, 5), (19, 5),
                           (19, 6), (19, 7), (20, 2), (20, 7), (21, 1), (22, 3), (24, 7), (25, 2), (25, 5), (25, 6),
                           (25, 7), (26, 5), (27, 1), (28, 2), (29, 1), (30, 3), (32, 5), (32, 6), (32, 7), (33, 4),
                           (34, 2), (37, 1), (37, 6), (37, 7), (38, 6), (38, 7), (39, 3), (40, 4), (40, 7), (41, 6),
                           (41, 7), (42, 7), (43, 5), (43, 6), (44, 5), (45, 2), (45, 5), (46, 3), (46, 4), (47, 3),
                           (48, 3)]
        DeepPositions = [(1, 6), (2, 5), (4, 5), (5, 5), (6, 5), (6, 6), (6, 7), (7, 1), (7, 4), (8, 4), (9, 1), (9, 3),
                         (9, 4), (9, 6), (9, 7), (10, 5), (10, 6), (11, 2), (12, 2), (12, 4), (13, 4), (13, 5), (13, 6),
                         (13, 7), (14, 1), (15, 3), (16, 3), (17, 3), (17, 6), (17, 7), (18, 2), (18, 3), (18, 4),
                         (18, 5), (18, 6), (20, 4), (20, 5), (20, 6), (21, 6), (22, 3), (22, 4), (23, 1), (23, 4),
                         (26, 2), (26, 7), (27, 7), (28, 2), (28, 4), (28, 5), (28, 6), (29, 3), (30, 3), (30, 6),
                         (31, 6), (31, 7), (32, 7), (33, 1), (36, 2), (37, 7), (38, 7), (39, 5), (39, 6), (39, 7),
                         (41, 1), (43, 1), (43, 5), (43, 6), (44, 2), (44, 5), (45, 1), (45, 3), (45, 5), (46, 3),
                         (47, 2), (47, 3), (48, 2), (48, 3), (48, 6), (48, 7)]

        ShallowLeadSpoke = 2
        MiddleLeadSpoke = 1
        DeepLeadSpoke = 1

        # Create the 3 disks
        self.CreateDisk(ShallowLeadSpoke, ShallowPositions)
        self.CreateDisk(MiddleLeadSpoke, MiddlePositions)
        self.CreateDisk(DeepLeadSpoke, DeepPositions)

        # Board positions and properties dict object. These are the *visible* spaces in play
        self.BoardSpokes = {
            "1": {4, 5, 6, 7},
            "2": {4, 5, 6, 7},
            "3": {1, 3, 4, 5, 6, 7},
            "4": {2, 5, 6, 7},
            "5": {3, 4, 5, 6, 7},
            "6": {2, 5, 7},
            "7": {4, 5, 6, 7},
            "8": {3, 5, 6, 7},
            "9": {1, 3, 5, 7},
            "10": {2, 5, 7},
            "11": {4, 6},
            "12": {2, 3, 5, 6},
            "13": {1, 4, 6},
            "14": {2, 3, 6},
            "15": {3, 4, 7},
            "16": {4, 6, 7},
            "17": {1, 5, 7},
            "18": {2, 3, 4, 6, 7},
            "19": {4, 5, 6},
            "20": {2, 3, 5, 6, 7},
            "21": {1, 5, 6, 7},
            "22": {4, 7},
            "23": {1, 3, 4, 5},
            "24": {2, 4, 6},
            "25": {3, 5, 6},
            "26": {4, 5, 6},
            "27": {1},
            "28": {2, 4, 5, 7},
            "29": {1, 4, 6},
            "30": {2, 3, 5, 7},
            "31": {6},
            "32": {3, 5, 7},
            "33": {1, 4, 6},
            "34": {2, 4, 5},
            "35": {1, 4, 7},
            "36": {2, 3, 4, 5, 7},
            "37": {1, 5, 6, 7},
            "38": {2, 3, 4, 5, 6, 7},
            "39": {1, 6},
            "40": {2, 4, 5, 7},
            "41": {1, 4, 6, 7},
            "42": {2, 5, 6, 7},
            "43": {3, 5, 7},
            "44": {4},
            "45": {3, 4, 6, 7},
            "46": {2, 5, 6, 7},
            "47": {3, 5, 6, 7},
            "48": {2, 4, 5, 6, 7}
        }
        self.RawBoardProperties = {
            "1": {
                "price": 12000,
                "adjacentProperties": [2, 6, 10, 9],
                "positions": [(39, 6), (40, 7), (40, 5), (40, 4), (41, 7), (41, 6), (41, 4), (42, 7), (42, 6), (42, 5),
                              (43, 7), (43, 5)]
            },
            "2": {
                "price": 8000,
                "adjacentProperties": [1, 6, 3],
                "positions": [(45, 7), (45, 6), (46, 7), (46, 6), (46, 5), (47, 7), (47, 6), (47, 5)]
            },
            "3": {
                "price": 9000,
                "adjacentProperties": [2, 6, 7, 4],
                "positions": [(48, 7), (48, 6), (48, 5), (1, 7), (1, 6), (1, 5), (2, 7), (2, 6), (2, 5)]
            },
            "4": {
                "price": 11000,
                "adjacentProperties": [3, 7, 5],
                "positions": [(3, 7), (3, 6), (3, 5), (4, 7), (4, 6), (4, 5), (5, 7), (5, 6), (5, 5), (5, 4), (6, 5)]
            },
            "5": {
                "price": 9000,
                "adjacentProperties": [4, 7, 8],
                "positions": [(6, 7), (7, 7), (7, 6), (7, 5), (7, 4), (8, 7), (8, 6), (8, 5), (9, 7)]
            },
            "6": {
                "price": 9000,
                "adjacentProperties": [1, 2, 3, 10],
                "positions": [(43, 3), (44, 4), (45, 4), (45, 3), (46, 2), (47, 3), (48, 2), (48, 4), (1, 4)]
            },
            "7": {
                "price": 8000,
                "adjacentProperties": [6, 3, 4, 5, 8, 11],
                "positions": [(2, 4), (3, 4), (3, 3), (3, 1), (4, 2), (5, 3), (6, 2), (9, 1)]
            },
            "8": {
                "price": 8000,
                "adjacentProperties": [7, 5, 11, 12],
                "positions": [(8, 3), (9, 3), (9, 5), (10, 2), (10, 5), (10, 7), (11, 6), (11, 4)]
            },
            "9": {
                "price": 10000,
                "adjacentProperties": [1, 10, 13],
                "positions": [(38, 7), (38, 6), (38, 5), (38, 4), (37, 7), (37, 6), (37, 5), (36, 7), (36, 5), (36, 4)]
            },
            "10": {
                "price": 10000,
                "adjacentProperties": [14, 13, 9],
                "positions": [(35, 1), (36, 2), (36, 3), (37, 1), (38, 2), (38, 3), (39, 1), (40, 2), (41, 1), (42, 2)]
            },
            "11": {
                "price": 9000,
                "adjacentProperties": [7, 8, 12, 15],
                "positions": [(12, 2), (12, 3), (12, 5), (13, 1), (13, 4), (14, 2), (14, 3), (15, 4), (14, 5)]
            },
            "12": {
                "price": 8000,
                "adjacentProperties": [8, 11, 15, 18],
                "positions": [(12, 6), (13, 6), (14, 6), (15, 7), (16, 7), (16, 6), (16, 4), (17, 5)]
            },
            "13": {
                "price": 8000,
                "adjacentProperties": [9, 10, 14, 16],
                "positions": [(35, 7), (35, 4), (34, 5), (34, 4), (33, 6), (33, 4), (32, 7), (32, 5)]
            },
            "14": {
                "price": 10000,
                "adjacentProperties": [10, 13, 16, 17, 15],
                "positions": [(34, 2), (33, 1), (32, 3), (30, 2), (30, 3), (29, 1), (28, 2), (27, 1), (23, 1), (24, 2)]
            },
            "15": {
                "price": 8000,
                "adjacentProperties": [11, 12, 14, 17, 18],
                "positions": [(21, 1), (20, 2), (20, 3), (19, 4), (18, 2), (18, 3), (18, 4), (17, 1)]
            },
            "16": {
                "price": 8000,
                "adjacentProperties": [13, 14, 17],
                "positions": [(31, 6), (30, 5), (30, 7), (29, 4), (29, 6), (28, 4), (28, 5), (28, 7)]
            },
            "17": {
                "price": 12000,
                "adjacentProperties": [16, 14, 15, 18],
                "positions": [(26, 6), (26, 5), (26, 4), (25, 6), (25, 5), (25, 3), (24, 6), (24, 4), (23, 3), (23, 4),
                              (23, 5), (22, 4)]
            },
            "18": {
                "price": 12000,
                "adjacentProperties": [17, 15, 12],
                "positions": [(22, 7), (21, 7), (21, 6), (21, 5), (20, 7), (20, 6), (20, 5), (19, 6), (19, 5), (18, 7),
                              (18, 6), (17, 7)]
            },

        }

        # Create property object for each property in order stored in RawBoardProperties
        self.BoardProperties = [
                Property(
                    name=property,
                    price=self.RawBoardProperties[property]['price'],
                    adjacentProperties=self.RawBoardProperties[property]['adjacentProperties'],
                    positions=self.RawBoardProperties[property]['positions']
                ) for property in self.RawBoardProperties.keys()
            ]

    def CreateDisk(self, leadspoke, positions):

        disk = RandomizationDisk(board=self, leadSpoke=leadspoke, positions=positions)
        self.RandomizationDisks.append(disk)

    def GetDisks(self):
        return self.RandomizationDisks

    def GetStatistics(self):
        """
            Function to run statistics on the current board. This is for debugging purposes only and should not be used
            as a function of the game.
        """

        for level, disk in enumerate(self.GetDisks()):

            stats = disk.GetStatistics()

            print(f"Disk Level: {level + 1}")
            print(f'Total Hits: {stats["length"]}')
            print("Hits by Ring: ")
            for stat in sorted(stats["oil_by_ring"].keys()):
                print(f'Ring:{stat} - {stats["oil_by_ring"][stat]}')
            print('')
            print("Hits by Spoke: ")
            for stat in sorted(stats["oil_by_spoke"].keys()):
                print(f'Spoke:{stat} - {stats["oil_by_spoke"][stat]}')

            print('__________________________\n')

    def GetOil(self, spoke, ring):
        """
        This method searches for oil at a given spoke and ring in the disks. It iterates through each disk and checks if
         the oil is present at the relative spoke and the given ring position *. If oil is found, it returns a tuple
         with True and the depth at which the oil is found. If oil is not found in any disk, it returns a tuple with
         False and a depth of -1.

        """
        for depth, disk in enumerate(self.GetDisks()):
            relativeSpoke = (spoke - disk.GetSpokeOffset()) % self.SpokeTotal
            if disk.CheckHashMap(spoke=relativeSpoke, ring=ring):
                return True, depth

        # Returns False and fixed 3 depth which is max cost of 6000
        return False, 3

    def GetRawBoardProperties(self):
        return self.RawBoardProperties

    def GetBoardProperties(self):
        return self.BoardProperties

    def GetBoardPositions(self):
        return self.BoardSpokes

    def GetUnownedProperties(self):
        returnable = []
        return [property.GetName() for property in self.GetBoardProperties() if property.GetOwner() is None]

    def GetNamedProperty(self, property):
        # Takes in Int or Str of named property (1-18) and correlates to the saved property
        return self.BoardProperties[int(property)-1]
# def calculateAllPossible():
#     board = KingOilBoard()
#     properties = board.GetBoardProperties()
#
#     for prop in properties:
#
#         oilCount = 0
#         properties[prop] = {'oilCount': [], 'hits': {}}
#
#         for spoke, ring in properties[prop]["positions"]:
#             properties[prop]['hits'][(spoke, ring)] = 0
#
#     disks = board.GetDisks()
#
#     # Calculate all boards
#     for ShallowNotch in range(1, 13):
#         disks[0].SetNotch(ShallowNotch)
#         for MiddleNotch in range(1, 13):
#             disks[1].SetNotch(MiddleNotch)
#             for DeepNotch in range(1, 13):
#                 disks[2].SetNotch(DeepNotch)
#
#                 for prop in properties:
#
#                     oilCount = 0
#                     for spoke, ring in properties[prop]["positions"]:
#
#                         oil = board.GetOil(spoke, ring)
#
#                         if oil:
#                             properties[prop]['hits'][(spoke, ring)] += 1
#                             oilCount += 1
#
#                     properties[prop]['oilCount'].append(oilCount)
#                     print(f'Property: {prop}')
#                     print(f'Hits: {oilCount}')
#
#                 # val = input("Continue....")
#
#     for prop in properties:
#         oilCount = properties[prop]["oilCount"]
#
#         print(f'Property: {prop}')
#         print(f'Average: {round(sum(oilCount) / len(oilCount))}')
#         print(f'Most: {Counter(properties[prop]["hits"]).most_common(6)}')
#         print(f'Highest: {max(oilCount)}')
#         print(f'Lowest: {min(oilCount)}')
#         print(f'Most Common: {Counter(oilCount).most_common(7)}')
#         print('')
#
#         pipeables = {property: [] for property in properties}
#
#         for idx, board in enumerate(oilCount):
#             temp = 0
#             for adjacentProp in properties[prop]["adjacentProperties"]:
#                 if properties[str(adjacentProp)]["oilCount"][idx] >= 4:
#                     # pipeables[str(adjcentProp)].append(1)
#                     temp += 1
#                 else:
#                     pipeables[str(adjacentProp)].append(0)
#             # pipeables[property].append(temp/len(Properties[property]["adjacentProperties"]))
#
#         ''' for adjProp in pipeables:
#             print(f'Adjcent Prop: {adjProp} - {sum(pipeables[adjProp])/len(pipeables[adjProp])}')'''
#
#         '''for prop in pipeables:
#             print(f'Average Pipeable: {sum(pipeables[prop])/len(pipeables[prop])}')'''
#
#     pipeables = {property: [] for property in properties}
#
#     for x in range(len(properties["1"]["oilCount"])):
#         for prop in properties:
#             if properties[prop]["oilCount"][x] >= 4:
#                 pipeables[prop].append(1)
#             else:
#                 pipeables[prop].append(0)
#
#     for prop in pipeables:
#         print(f'Prop: {prop} - {sum(pipeables[prop]) / len(pipeables[prop])}')
#         print(f'Prop: {prop} - {Counter(pipeables[prop]).most_common(7)}')
#         print()
#
#
# if __name__ == "__main__":
#     calculateAllPossible()
#     pass
