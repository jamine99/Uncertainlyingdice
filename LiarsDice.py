import random

class player:
    def __init__(self,numDice,name):
        self.dice = [random.randint(1,6) for i in range(numDice)]
        self.name = name
class gameState:
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2
        self.prevBet = None
        self.totDice = len(player1.dice)+len(player2.dice)
        #Bet will be a tuple of (string,tuple)->(playerName,(DiceNumber, Number of that dice))
    def setPrevBet(prevBet):
        self.prevBet = prevBet

#CheckBet returns true if the bet is satisfied
#Bet here will just be a tuple of dicenumber to number of that dice
def checkBet(bet,state):
    dice = bet[0]
    numDice = bet[1]
    count = 0
    for p1Dice in state.player1.dice:
        if p1Dice == dice:
            count+=1
    for p2Dice in state.player2.dice:
        if p2Dice == dice:
            count+=1
    if numDice <= count:
        return True
    return False

def takeBet(name, isHuman):
    if isHuman:
        bet = input(name + " Please enter your bet (number ON dice, number OF dice) or NO to challenge previous bet")

#plays through one round of da game and returns which player won that round
#P1 always goes first
def round(state):
    p1 = state.player1
    p2 = state.player2
    currPlayer = p1
    while(True):
        if state.prevBet == None:
            print(currPlayer.name+ ": First Turn Bet")
            #always set to human first but we dont gotta once we start making bots
            p1Bet = takeBet(currPlayer.name, True)
            p1Split = takeBet(currPlayer.name, True).split()
            print(currPlayer.name + " bet " + p1Bet[1] " of " +p1Bet[0])
            #TODO check if bet actually is in the form of {number number} and is valid within rules
            state.setPrevBet((p1Split[0],p1Split[1]))
        else:
            print(currPlayer.name+ "'s Turn")
            #always set to human first but we dont gotta once we start making bots
            currBet = takeBet(currPlayer.name, True)

            #deal with the challenge
            if currBet.lower() == "no":
                if currPlayer == p1:
                    opposingPlayer = p2
                else:
                    opposingPlayer = p1
                prevBetCorrect = checkBet(state)
                if prevBetCorrect:
                    print(opposingPlayer.name + " Won This Round!")
                    return opposingPlayer
                else:
                    print(currPlayer.name + " Won This Round!")
                    return currPlayer

            currBetSplit = takeBet(currPlayer.name, True).split()
            print(currPlayer.name + " bet " + p1Bet[1] " of " +p1Bet[0])
            #TODO check if bet actually is in the form of {number number} and is valid within rules
            state.setPrevBet((p1Split[0],p1Split[1]))

#TODO ADD MAIN AND HAVE IT CYCLE ROUNDS UNTIL ONE PLAYER IS OUT OF DICE
