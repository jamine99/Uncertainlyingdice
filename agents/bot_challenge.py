import Player

class Bot_Challenge(Player):
    def __init__(self,numDice,name):
        super().__init__(numDice, name)

    def takeBet(self, state):
        return "no"
