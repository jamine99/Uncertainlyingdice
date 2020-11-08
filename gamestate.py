from agents.reduced_state import ReducedState
from agents.player import Player

class GameState:
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2
        self.prevBet = None
        self.prev_state = ReducedState(self.player1.dice, (0, 0))

        #Bet will be a tuple of (DiceNumber, Number of that dice)
    def setPrevBet(self, prevBet):
        self.prevBet = prevBet

    def reset_to_round_start(self):
        self.player1.roll_dice()
        self.player2.roll_dice()
        self.prevBet = None
        self.prev_state = ReducedState(self.player1.dice, (0, 0))

    def to_string(self):
        string = "Current Game State: \n"
        string += "\t" + self.player1.name + " has " + str(len(self.player1.dice)) + " dice left.\n"
        string +="\t" + self.player2.name + " has " + str(len(self.player2.dice)) + " dice left.\n"
        if self.prevBet != None:
            string += "\tPrevious bet was " + self.prevBet[1] + " " + self.prevBet[0] +  "s.\n"
        return string

    def totDice(self):
        return len(self.player1.dice) + len(self.player2.dice)
