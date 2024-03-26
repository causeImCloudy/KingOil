from src.KingOilGame import *
from src.aux.PyQuest import *
import pickle


'''
    How to Play King Oil
    1. Set the Game Up
        a. Gather how many players should be added
        b. 
    2. Perform beginning 
'''


if __name__ == '__main__':
    # Handle loading a game.
    loadSave = False
    question = PyQuest([{"question": "Would you like to load a saved game?",
                         "answers": ['Yes', 'No']}]).start()

    if question[0]['answer'] == 0:
        with open('KingOil.pickle', 'rb') as file:
            obj = pickle.load(file)
        loadSave = True

    try:
        if loadSave:
            game = obj
            game.MainLoop()
        else:
            game = KingOilGame(4)
            game.Start()

    except KeyboardInterrupt:
        # Handle Keyboard interrupts to save the game
        question = PyQuest([{"question":"Would you like to save the game?",
                            "answers":['Yes','No']}]).start()

        if question[0]['answer'] == 0:
            with open('KingOil.pickle', 'wb') as file:
                pickle.dump(game.GetBackup(), file)

        print("Exiting...")
