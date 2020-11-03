from agents.player import Player
import random

class Random_Bot(Player):
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

            if prev_numDice != totalDice: # if prev_numDice was not totalDice, then increment new_numDice but keep new_dice the same
                new_numDice = prev_numDice + 1
                new_dice = prev_dice
            else: # if prev_numDice was totalDice, then only increment new_dice (if possible) and keep new_numDice the same
                if prev_dice != 6:
                    new_numDice = prev_numDice
                    new_dice = prev_dice + 1
                else:
                    return "no"
        first = True
        bet_numDice = None
        bet_newDice = None
        betList = []
        for i in range(new_numDice,totalDice+1):
            for j in range(new_dice,7):
                if first:
                    first = False
                else:
                    betList.append((i,j))
        betList.append((0,0))
        bet_numDice , bet_newDice = random.choice(betList)

        if bet_numDice == 0:
            return "no"
            
        return str(bet_numDice) + " " + str(bet_newDice)
