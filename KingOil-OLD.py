from src.Board import *


def SetUpGame():
    print('Welcome to King Oil the board game turned video game. Lets run through some set up questions:')
    
    numPlayers = None
    while numPlayers is None:
        numPlayers = input("Enter number of players(1-4): ")
        if not numPlayers.isdigit() and not (1 <= int(numPlayers) <= 4):
            print('Please enter a digit between 1 and 4.')
            numPlayers = None

    return int(numPlayers)


def PurchaseProperty(board, currentPlayer):
    pass


def BarterItem(board, item, currentPlayer):
    pass


def PayPipelines(board, curPlayer):
    """
        Loop through all properties owned by the current player then loop through the pipelines attached to the
        BadPipeline array(the ones you owe money on). If you have insufficient money it will transfer all assets over to
        return false
    """
    for property in curPlayer.GetProperties():
        for pipeline in property.GetBadPipeline():

            payment = property.GetOilHits() * ( 2 * pipeline.GetLevel() - 1) * 1000

            try:
                board.GetBank().TransferMoney(
                    fromAcct=curPlayer.GetBankAccount(),
                    toAcct=pipeline.GetFromProperty().GetOwner().GetBankAccount(),
                    price=payment
                )
            except ArithmeticError:
                print(f'[Turn] Player {curPlayer.GetName()} has gone bankrupt from a pipeline. All assets now belong to'
                      f'{pipeline.GetFromProperty().GetOwner()}.')

                board.BankruptPlayer(bankruptPlayer=curPlayer, richPlayer=pipeline.GetFromProperty().GetOwner())
                return False

    return True


def Turn(board, curPlayer):
    # Give money for hits
    selectedCard = board.GetDeck().DrawCard()
    curPlayerProperty = curPlayer.GetProperties()
    print(f'[Turn] Player {curPlayer.GetName()} got the {selectedCard.GetName()} card.')

    # Calculate Production vs Oil Depletion vs Fire damage
    if selectedCard.GetProduction() > 0:
        totalOil = 0
        for property in curPlayerProperty:
            totalOil += len(property.GetOilHits())

        earnings = totalOil * selectedCard.GetProduction()
        board.GetBank().TransferMoney(
            fromAcct=board.GetBank().Bank,
            toAcct=curPlayer.GetBankAccount(),
            price=earnings
        )

        print(f'[Turn] Player {curPlayer.GetName()} has {totalOil} oil derricks earning .')
    elif selectedCard.GetBasePay() > 0:
        print(f'[Turn] Player {curPlayer.GetName()} has earned {selectedCard.GetBasePay()} for oil depletion.')
        board.GetBank().TransferMoney(
            fromAcct=board.GetBank().Bank,
            toAcct=curPlayer.GetBankAccount(),
            price=selectedCard.GetBasePay()
        )
    else:
        print(f'[Turn] Player {curPlayer.GetName()} which oil derricks do you want.')
        #TODO Make fire damage card.

    # Drill for oil
    print(f'[Turn] Player {curPlayer.GetName()} has {selectedCard.GetWells()} wells to drill.')
    for x in range(int(selectedCard.GetWells())):
        print(f'[Turn] Player {curPlayer.GetName()} where would you like drill?')
        for idx, prop in enumerate(curPlayerProperty):
            print(f'[Turn] [{idx}] Property {curPlayerProperty[idx]}')

        selectedProp = input(f'[Turn] Please selected the ID of the property you would like to drill on')
        # TODO Add validation

        for idy, position in enumerate(curPlayerProperty[selectedProp].GetPositions()):
            print(f'[Turn] [{idy}] Position {curPlayerProperty[idy]}')

        selectedPosition = input(f'[Turn] Please selected the ID of the position you would like to drill')

        position = curPlayerProperty[selectedProp].GetPositions()[selectedPosition].keys()
        hit, depth = board.GetOil(position[0], position[1])

        if hit:
            drillPrice = depth * 2000
            board.GetBank().TransferMoney(
                fromAcct=curPlayer.GetBankAccount(),
                toAcct=board.GetBank().Bank,
                price=drillPrice,
                forcePurchase=True
            )
            print(f'[Turn] Player {curPlayer.GetName()} drilled oil at depth {depth} for ${drillPrice}.')
        else:
            missPrice = 6000
            board.GetBank().TransferMoney(
                fromAcct=curPlayer.GetBankAccount(),
                toAcct=board.GetBank().Bank,
                price=missPrice
            )
            print(f'[Turn] Player {curPlayer.GetName()} did not find oil at position ${missPrice}.')

        # Update positions
        # TODO need to update master record ?? does this work idk
        curPlayerProperty[selectedProp][position] = hit

    # Purchase, burn or sell property
    if selectedCard.HasProperty():
        print(f'[Turn] Player {curPlayer.GetName()} has the ability to purchase a property. What would you like to do?')
        print(f'[Turn] [1] Purchase a Property.')
        print(f'[Turn] [2] Sell the ability to purchase a property.')
        print(f'[Turn] [3] Do nothing / Burn the ability to purchase a property.')
        propertyOption = input(f'[Turn] Please selected the ID of the option you want to do?')

        allProperty = board.GetBoardProperties()

        # TODO Add bartering system
        # match propertyOption:
        #     case 1:
        #         for prop in allProperty.keys():
        #             if allProperty[prop].GetOwner() is not None:
        #                 print(f'[Turn] Property {prop} is available')

        for prop in allProperty.keys():
            if allProperty[prop].GetOwner() is not None:
                print(f'[Turn] Property {prop} is available')


def Optionals(board, curPlayer):
    pass


def IsGameOver(players, bank):
    """
        A structured format to calculate the winning conditions.
        The Win Conditions for a game are twofold:
            1. The bank runs out of money.
            2. All but 1 player is bankrupt
    """
    bankruptPlayers = 0

    for player in players:
        
        if player.GetBankAccount().GetBalance() <= 0:
            bankruptPlayers += 1
    
    if bankruptPlayers == (len(players) - 1) or bank.GetBankBalance() < 1:
        for player in players:
            if player.GetBankAccount() > 0:
                print(f'{player.GetName()}')
        return True
    else:
        return False


def main():
    board = Board()
    bank = board.GetBank()
    players = []
    turnCount = 0
    
        numPlayers = SetUpGame()
        randomNames = ['Blue', 'Green', 'Red', 'Pink', 'Yellow', 'Brown']

    # Set up all the players and their bank accounts
    for x in range(numPlayers):
        name = randomNames.pop(random.SystemRandom().randint(0, len(randomNames) - 1))
        player = Player(name)
        account = bank.NewPlayer(player)

        players.append(player)
        player.SetBankAccount(account)
#RIGHT HERE BRO
    # Stupid simple random player order will update
    turnCount = random.SystemRandom().randint(0, numPlayers-1)

    # Purchase beginProperty Loop
    for player in players:
        PurchaseProperty(board, player)
        turnCount = (turnCount + 1) % (len(players) - 1)

    # main game loop
    while not IsGameOver(players, bank):
        # Grabs current players turn
        currentPlayerTurn = players[turnCount]

        if not currentPlayerTurn.BankruptStatus():
            print(f'Player {currentPlayerTurn.GetName()}\'s turn: ')

            """
                Goes through the three options in order 
                1. Pay pipelines at beginning of turn
                2. Draw a card and do the options on the card.
                3. Do optional items(build pipelines, trade property)
            """
            if not PayPipelines(board, currentPlayerTurn):
                break
            Turn(board, currentPlayerTurn)
            Optionals(board, currentPlayerTurn)

            print(f'Player {currentPlayerTurn}\'s has ended their turn.\n')

        turnCount = (turnCount + 1) % (numPlayers-1)

    print('Thanks for playing!')


if __name__ == "__main__":
    main()
