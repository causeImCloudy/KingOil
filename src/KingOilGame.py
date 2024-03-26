import copy
import rich
import pdb
from icecream import ic

from src.Board import *
from src.Bank import *
from src.Deck import *
from src.Player import *
from src.aux.PyQuest import *


def __print_info__(string):
    rich.print(f'[bold blue][King Oil][/bold blue] {string}')


def __calculate_earning__(currentPlayerProperty, productionRate):
    totalOil = 0
    for property in currentPlayerProperty:
        totalOil += len(currentPlayerProperty[property].GetOilHits())
    return totalOil * productionRate


def __split_cordinates__(position):
    x, y = position.strip("()").strip(" ").split(",")
    return x, y


class KingOilGame:
    def __init__(self, playerCount):
        """
            Takes in player count, then instantiates the King Oil Game. Creating a Bank, Board, Deck of Cards, and a
            Player for player count.
        """
        self.Board = Board()
        self.PlayerCount = playerCount
        self.Players = []

        # Simple tracker int which is randomized at the beginning of the game.
        self.TurnTracker = random.SystemRandom().randint(0, self.PlayerCount-1)

        self.Bank = Bank()
        self.Deck = Deck()

        randomNames = ['Blue', 'Green', 'Red', 'Pink', 'Yellow', 'Brown']

        for i in range(playerCount):
            self.NewPlayer(
                randomNames.pop(random.SystemRandom().randint(0, len(randomNames) - 1))
            )

        # Loads saved files JSON used within the PyQuest class.

        with open('savedQuestions.json') as f:
            self.SavedQuestions = json.load(f)

        # Sets a saving function action by incrementing
        self.PreviousTurn = None

    def GetBank(self):
        return self.Bank

    def GetDeck(self):
        return self.Deck

    def BankruptPlayer(self, bankruptPlayer, richPlayer):
        """
            Function to bankrupt a player, transferring all remaining money and property to the attacking player
        """
        balance = bankruptPlayer.GetAccount().GetBalance()

        # Transfer all money
        self.Bank.TransferMoney(fromAcct=bankruptPlayer.GetAccount(), toAcct=richPlayer.GetAccount(), price=balance)

        # Transfer all properties
        for property in bankruptPlayer.GetProperties():
            property.SetOwner(richPlayer)

    def GameOver(self):
        """
            A structured format to calculate the winning conditions.
            The Win Conditions for a game are twofold:
                1. The bank runs out of money.
                2. All but 1 player is bankrupt
        """
        bankruptPlayers = 0

        for player in self.Players:

            if player.GetBankAccount().GetBalance() <= 0:
                bankruptPlayers += 1

        if bankruptPlayers == (len(self.Players) - 1) or self.Bank.GetBankBalance() < 1:
            for player in self.Players:
                if player.GetBankAccount() > 0:
                    print(f'{player.GetName()}')
            return True
        else:
            return False

    def NewPlayer(self, name):
        """
            Creates a new Player and assigns them all the required items for a new player then appends the player back
            to the Parents tracking array.
        """

        player = Player(name)
        account = self.Bank.NewPlayer(player)
        player.SetBankAccount(account)
        self.Players.append(player)

    def IncreaseTurnTracker(self, amount=1):
        self.TurnTracker = (self.TurnTracker + amount) % (self.PlayerCount - 1)

    def GetCurrentPlayer(self):
        return self.Players[self.TurnTracker]

    def HandlePropertyPurchase(self, player, force=False):
        # Add option to force the purchase of property for the start of the game
        if force:
            savedQuestions = self.SavedQuestions['purchaseFirstProperty']
        else:
            savedQuestions = self.SavedQuestions['purchaseProperty']

        # Fill in answers with unowned properties
        savedQuestions[0]['sub-questions'][0]['answers'] = self.Board.GetUnownedProperties()

        purchaser = PyQuest(savedQuestions)
        answers = purchaser.start()

        ic(int(answers[0]['answer']))
        match int(answers[0]['answer']):
            case 0:
                # Purchase a property
                # Pulls the answered value from the given answer array
                purchasedProperty = answers[0]['sub-questions'][0]['answers'][
                    answers[0]['sub-questions'][0]['answer']
                ]

                propertyObj = self.Board.GetNamedProperty(purchasedProperty)

                # Checks if user can purchase the property
                if player.GetBankAccount().GetBalance() >= propertyObj.GetPrice():
                    __print_info__(f"{self.GetCurrentPlayer().GetName()} has purchased the property {purchasedProperty}")

                    # Assigns current player to property
                    propertyObj.SetOwner(self.GetCurrentPlayer())
                    # Update assignment in player reference
                    self.GetCurrentPlayer().AddProperty(propertyObj)

                    # Transfers Money
                    self.Bank.TransferMoney(
                        fromAcct=player.GetBankAccount(),
                        toAcct=self.GetBank().Bank,
                        price=propertyObj.GetPrice()
                    )

                else:
                    self.HandlePropertyPurchase(player)

            case 1:
                # TODO Not enabled yet
                # Sell the ability to purchase property
                pass
            case -2:
                __print_info__(f"{self.GetCurrentPlayer().GetName()} has burned the ability to purchase property.")
            case _:
                raise ValueError(f"Invalid property {answers[0]['sub-questions']}")

    def DrillOil(self, force=False):

        # Determine if this is the first question(required to drill for oil) or more than one which user can stop at
        # any time
        if force:
            question = self.SavedQuestions['drillForFirstOil']
        else:
            question = self.SavedQuestions['drillForOil']

        # Grab current players properties
        currentPlayerProps = self.GetCurrentPlayer().GetProperties()

        # Loop through properties and fill out the python dict to send to PyQuest.
        # Only fills properties with open positions
        for id, property in enumerate(currentPlayerProps):

            oilOpenPosition = currentPlayerProps[property].GetOpenPositions()

            if len(oilOpenPosition) > 0:
                question[0]['answers'].append(
                    {
                        "answer": property,
                        "value": id
                    }
                )
                question[0]['sub-questions'].append(
                    {
                        "question": "Which position would you like to drill?",
                        "answers": oilOpenPosition,
                    }
                )
        ic(question)
        drillPosition = PyQuest(question).start()

        # Checks if answer is not -2 which is listed as stop drilling
        if drillPosition[0]['answers'][drillPosition[0]['answer']]['value'] >= 0:
            # Correlates answer to viewable answer
            cords = drillPosition[0]['sub-questions'][drillPosition[0]['answer']]['answers'][
                drillPosition[0]['sub-questions'][0]['answer']]

            # Splits the string viewable to two ints representing the coordinates
            spoke, ring = cords

            oil, depth = self.Board.GetOil(spoke, ring)

            if oil:
                __print_info__(f"{self.GetCurrentPlayer().GetName()} has drilled {depth} level of oil")

                # Assigns the list position Ture for the oil
                (self.Board.GetNamedProperty(drillPosition[0]['answers'][drillPosition[0]['answer']]['answer'])
                 .SetOilHitPosition(cords, True))

            else:
                # Set cord to no oil to False
                (self.Board.GetNamedProperty(drillPosition[0]['answers'][drillPosition[0]['answer']]['answer'])
                 .SetOilHitPosition(cords, True))
                __print_info__(f"{self.GetCurrentPlayer()} did not find any oil.")

            # Transfer money for drilling. On first drill
            self.GetBank().TransferMoney(
                fromAcct=self.GetCurrentPlayer().GetBankAccount(),
                toAcct=self.GetBank().Bank,
                price=2000 * depth,
                forcePurchase=True
            )

            # Checks if the user has run out of money drilling
            ic(self.GetCurrentPlayer().GetBankAccount().GetBalance())
            if self.GetCurrentPlayer().GetBankAccount().GetBalance() == 0:
                return False

            return True
        else:
            # If backed out return false
            return False

    def HandleDrillOil(self, max):
        # Drill Oil 1 time - returns true to continue and false skips
        track = self.DrillOil(force=True)
        ic(max)
        ic(range(int(max) - 1))
        ic(track)
        for i in range(int(max) - 1):
            if track:
                track = self.DrillOil()
            else:
                break

    def HandleFireDamage(self):
        # Checks if current player has any wells to remove
        if self.GetCurrentPlayer().GetTotalOil() > 0:
            question = self.SavedQuestions['fireDamageProperty']

            # Lists all owned property and formats them into the two tiered question and answer and correlates all of
            # them to their correct sub-questions
            for id, property in enumerate(self.GetCurrentPlayer().GetProperties()):
                question[0]['answers'].append(
                    {
                        "answer" : property.GetName(),
                        "value" : id
                    }
                )
                question[0]['sub-questions'].append(
                    {
                        "question" : "Which oil rig would you like to burn",
                        "answers": property.GetOilHitPositions(),
                    }
                )

            answer = PyQuest(question).start()

            selectedProperty = self.Board.GetNamedProperty(
                answer[0]['answers'][answer[0]['answer']]
            )

            # This may need to be updated if answers is stored within the sub question not the holding array
            # answer[0]['sub-questions'][answer[0]['answer']]['answer']
            selectedProperty.SetOilHitPosition(answer[0]['sub-questions']['answer'])

    def GetBackup(self):
        return self.PreviousTurn

    def HandlePipelines(self):

        currentPlayer = self.GetCurrentPlayer()
        properties = self.GetCurrentPlayer().GetProperties()

        for prop in properties:
            pipelines = properties[prop].GetBadPipeline()
            for pipeline in pipelines:
                if len(pipelines) >= 1:
                    # Calculate cost - Level 1,2,3 = 1000,2000,3000 * Pipelines
                    payment = (((pipeline.GetLevel() - 1) * 1000) + 1000) * self.GetCurrentPlayer().GetTotalOil()
                    # Transfer money
                    self.GetBank().TransferMoney(
                        fromAcct=currentPlayer.GetBankAccount(),
                        toAcct=pipeline.GetFromProperty().GetOwner().GetBankAccount(),
                        price=payment,
                        forcePurchase=False
                    )
                    # Announce
                    __print_info__(f'{currentPlayer.GetName()} payed {pipeline.GetFromProperty().GetOwner().GetName()} '
                                   f'for the pipeline from {pipeline.GetFromProperty().GetName()} to {property}.')
                    # Calculate end game
                    if currentPlayer.GetBankAccount().GetBalance() <= 0:
                        # If player is bankrupt, bankrupt the player and return false
                        self.BankruptPlayer(bankruptPlayer=currentPlayer, richPlayer=pipeline.GetFromProperty().GetOwner())
                        return False
        return True

    def Turn(self):
        """
            This walks through the standard turn of a King Oil Game.
            First Select the Current player, then pay pipelines, draw a card and do all card options, then opt for
            optional tasks(build pipeline, trade with someone), and end turn.
        """

        # Used to save the game
        self.PreviousTurn = copy.deepcopy(self)

        # Gather who is the current player and take inventory of their property
        currentPlayer = self.GetCurrentPlayer()
        currentPlayerProperty = currentPlayer.GetProperties()
        __print_info__(f"It is now {currentPlayer.GetName()}'s turn.")

        # Handles the payment of pipelines and exits if they are bankrupt
        if not self.HandlePipelines():
            __print_info__(f"{currentPlayer.GetName()} is Bankrupt.")
            return

        # Draw a card from the deck and announce to game what they have drawn
        drawnCard = self.Deck.DrawCard()
        __print_info__(f"{currentPlayer.GetName()} has drawn the {drawnCard.GetName()} card.")

        # Calculate which card you have received, negative production is referenced to Fire damage card
        if drawnCard.GetProduction() == -1:
            # Fire Damage Removes 2 Wells
            for _ in range(2):
                self.HandleFireDamage()

        else:
            """ 
                Calculate earnings per property and include oil depletion. Force money transfer from Bank to current 
                players bank account.
            """
            earnings = __calculate_earning__(currentPlayerProperty, drawnCard.GetProduction())
            self.GetBank().TransferMoney(
                fromAcct=self.GetBank().Bank,
                toAcct=currentPlayer.GetBankAccount(),
                price=earnings,
                forcePurchase=True
            )
            __print_info__(f"{currentPlayer.GetName()} produced ${earnings + drawnCard.GetBasePay()}.")

        # Drill 1 - x spots for oil
        self.HandleDrillOil(drawnCard.GetWells())

        # Purchase property if players drawn card has the ability
        if drawnCard.HasProperty():
            self.HandlePropertyPurchase(currentPlayer)
        exit()

    def MainLoop(self):
        while not self.GameOver():
            self.Turn()
            self.IncreaseTurnTracker()

    def Start(self):

        # Purchase starting property for each player
        for player in self.Players:
            __print_info__(f"{self.GetCurrentPlayer().GetName()} is buying their first property.")
            self.HandlePropertyPurchase(self.GetCurrentPlayer(), force=True)
            self.IncreaseTurnTracker()

        self.MainLoop()

