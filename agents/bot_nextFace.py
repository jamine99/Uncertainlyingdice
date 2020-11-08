from agents.player import Player

class Bot_NextFace(Player):
    def __init__(self,numDice,name):
        super().__init__(numDice, name)

    def takeBet(self, state):
        new_dice = 0
        new_numDice = 0
        totalDice = state.totDice()

        if state.prevBet == None:
            new_dice = 1
            new_numDice = 1
        else:
            prev_dice = state.prevBet[0]
            prev_numDice = state.prevBet[1]

            if prev_dice == 6: # if prev_dice was 6, then increment new_numDice (if possible) but keep new_dice the same face
                if prev_numDice == totalDice:
                    return "no"
                else:
                    new_dice = prev_dice
                    new_numDice = prev_numDice + 1
            else: # if prev_dice was NOT 6, then keep new_numDice the same but increment new_dice up one face
                new_dice = prev_dice + 1
                new_numDice = prev_numDice

        return str(new_dice) + " " + str(new_numDice)
