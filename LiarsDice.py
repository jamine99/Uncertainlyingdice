from agents.player import Player
from agents.probabilitybot import ProbabilityBot
from agents.bot_challenge import Bot_Challenge
from agents.bot_nextNum import Bot_NextNum
from agents.bot_nextFace import Bot_NextFace
from agents.random_bot import Random_Bot
from agents.qlearn_bot import QBot

from agents.reduced_state import ReducedState
from agents.QlearningState import state
import qlearning

WINNING_ROUND_REWARD = 10
LOSING_ROUND_REWARD = -10
TERMINAL_WIN_STATE = 1
TERMINAL_LOSE_STATE = -1

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


def is_valid_bet(state, bet):
    if len(bet) != 2:
        print("Bet must be in the format <value of dice> <number of dice>.")
        return False

    dice = int(bet[0])
    num_dice = int(bet[1])

    if dice < 1 or dice > 6:
        print("Value of dice must be between 1 and 6.")
        return False

    if num_dice > state.totDice():
        print("Number of dice must be less than or equal to total number of dice.")
        return False

    if state.prevBet != None:
        if dice <= state.prevBet[0] and num_dice <= state.prevBet[1]:
            print("Value of dice or number of dice must be greater than the previous bet's value or number.")
            return False

    return True


#CheckBet returns true if the bet is satisfied
#Bet here will just be a tuple of dicenumber to number of that dice
def checkBet(state):
    dice = state.prevBet[0]
    numDice = state.prevBet[1]
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

#plays through one round of da game and returns which player won that round
#P1 always goes first
def round(state):
    print(state.to_string())
    p1 = state.player1
    p2 = state.player2
    currPlayer = p1
    while(True):
        # Show player 1's hand as if we are player 1.
        #if currPlayer == p1:
        #    p1.show_dice()
        # Show current player's dice, can replace with just p1 later on
        currPlayer.show_dice()

        # For the first bet, do not allow challenging.
        if state.prevBet == None:
            print(currPlayer.name + ": First Turn Bet")
            #always set to human first but we dont gotta once we start making bots
            p1Split = None
            while True:
                p1Bet = currPlayer.takeBet(state)
                p1Split = p1Bet.split()
                if is_valid_bet(state, p1Split): break
            print(currPlayer.name + " bet " + p1Split[1] + " dice of value " + p1Split[0])
            state.setPrevBet(tuple([int(p1Split[0]), int(p1Split[1])]))
        else:
            print(currPlayer.name+ "'s Turn")
            #always set to human first but we dont gotta once we start making bots
            currBetSplit = None
            while True:
                currBet = currPlayer.takeBet(state)

                print(currPlayer.name + " bet " + currBet)
                #deal with the challenge
                if currBet.lower() == "no":
                    if currPlayer == p1:
                        opposingPlayer = p2
                    else:
                        opposingPlayer = p1
                    prevBetCorrect = checkBet(state)
                    if prevBetCorrect:
                        print(opposingPlayer.name + " Won This Round!")
                        currPlayer.lose_dice()
                        return opposingPlayer
                    else:
                        print(currPlayer.name + " Won This Round!")
                        opposingPlayer.lose_dice()
                        return currPlayer

                currBetSplit = currBet.split()
                if is_valid_bet(state, currBetSplit): break

            print(currPlayer.name + " bet " + currBetSplit[1] + " dice of value " +currBetSplit[0])
            state.setPrevBet(tuple([int(currBetSplit[0]), int(currBetSplit[1])]))

        # Switch which player's turn it is.
        currPlayer = p2 if currPlayer == p1 else p1


def play_game(max_num_dice=5, player1_name="player1", player2_name="player2"):
    '''
    Plays one game of Liar's Dice.

    Args:
        max_num_dice (int): the number of dice each player starts with.
        player1_name (string): name for player1
        player2_name (string): name for player2
    '''
    player2bot = int(input("Please enter player 2 type: 1 for human, 2 for random, 3 for nextNum, 4 for nextFace, 5 for challenge, 6 for probability: "))
    player2 = None
    if player2bot == 1:
        player2 = Player(max_num_dice, player2_name)
    elif player2bot == 2:
        player2 = Random_Bot(max_num_dice, "Random Bot")
    elif player2bot == 3:
        player2 = Bot_NextNum(max_num_dice, "Next Number Bot")
    elif player2bot == 4:
        player2 = Bot_NextFace(max_num_dice, "Next Face Bot")
    elif player2bot == 5:
        player2 = Bot_Challenge(max_num_dice, "Challenge Bot")
    elif player2bot == 6:
        player2 = ProbabilityBot(max_num_dice, "Probability Bot")

    player1 = Player(max_num_dice, player1_name)
    state = GameState(player1, player2)

    while True:
        if player1.has_no_dice():
            print(player2 + " has won the game!")
            break
        if player2.has_no_dice():
            print(player1 + " has won the game!")
            break

        round(state)
        state.reset_to_round_start()

    if len(player1.dice) == 0:
        print(player2 + " has won the game!")
    else:
        print(player1 + " has won the game!")


def simulate_round(game):
    # Print inforamtion
    print(game.to_string())

    qbot = game.player1
    p2 = game.player2
    currPlayer = qbot
    while(True):
        # Show player 1's hand as if we are player 1.
        #if currPlayer == p1:
        #    p1.show_dice()
        # Show current player's dice, can replace with just p1 later on
        currPlayer.show_dice()

        # For the first bet, do not allow challenging.
        if game.prevBet == None:
            print(currPlayer.name + ": First Turn Bet")
            #always set to human first but we dont gotta once we start making bots
            p1Split = None
            while True:
                p1Bet = currPlayer.takeBet(game)
                print(p1Bet)
                p1Split = p1Bet.split()
                if is_valid_bet(game, p1Split): break
            print(currPlayer.name + " bet " + p1Split[1] + " dice of value " + p1Split[0])
            game.setPrevBet(tuple([int(p1Split[0]), int(p1Split[1])]))
        else:
            print(currPlayer.name+ "'s Turn")
            #always set to human first but we dont gotta once we start making bots
            currBetSplit = None
            while True:
                currBet = currPlayer.takeBet(game)
                print(currPlayer.name + " bet " + currBet)

                # Deal with the challenge.
                if currBet.lower() == "no":
                    if currPlayer == qbot:
                        opposingPlayer = p2
                    else:
                        opposingPlayer = qbot

                    if checkBet(game):
                        if currPlayer == p2:
                            qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index(game.prevBet), TERMINAL_WIN_STATE, WINNING_ROUND_REWARD, qbot.model)
                        else:
                            # Current action is a challenge bet denoted as (-1, -1).
                            qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index((-1, -1)), TERMINAL_LOSE_STATE, LOSING_ROUND_REWARD, qbot.model)
                        print(opposingPlayer.name + " Won This Round!")
                        return opposingPlayer
                    else:
                        if currPlayer == p2:
                            qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index(game.prevBet), TERMINAL_LOSE_STATE, LOSING_ROUND_REWARD, qbot.model)
                        else:
                            # Current action is a challenge bet denoted as (-1, -1).
                            qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index((-1, -1)), TERMINAL_WIN_STATE, WINNING_ROUND_REWARD, qbot.model)
                        print(currPlayer.name + " Won This Round!")
                        return currPlayer

                currBetSplit = currBet.split()
                if is_valid_bet(game, currBetSplit): break

            print(currPlayer.name + " bet " + currBetSplit[1] + " dice of value " +currBetSplit[0])
            new_bet = tuple([int(currBetSplit[0]), int(currBetSplit[1])])

            # If not q-learning agent
            if currPlayer == p2:
                new_state = ReducedState(qbot.dice, new_bet)
                qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index(game.prevBet), new_state.generateNumber(), 0, qbot.model)

            # Right before we update the previous bet to be p1's current bet, we update our prev_state to be the previous bet which is p2's last bet.
            if currPlayer == qbot:
                game.prev_state.update_bet(game.prevBet)

            game.setPrevBet(new_bet)

        # Switch which player's turn it is.
        currPlayer = p2 if currPlayer == qbot else qbot


def simulate_rounds(max_num_dice=5, player1_name="AgentQ", player2_name="player2", num_rounds=1000000):
    '''
    Simulates many rounds of Liar's Dice for QLearning.

    Args:
        max_num_dice (int): the number of dice each player starts with.
        player1_name (string): name for player1
        player2_name (string): name for player2
    '''
    player2bot = int(input("Please enter player 2 type: 1 for human, 2 for random, 3 for nextNum, 4 for nextFace, 5 for challenge, 6 for probability: "))
    player2 = None
    if player2bot == 1:
        player2 = Player(max_num_dice, player2_name)
    elif player2bot == 2:
        player2_name = "Random Bot"
        player2 = Random_Bot(max_num_dice, player2_name)
    elif player2bot == 3:
        player2_name = "Next Number Bot"
        player2 = Bot_NextNum(max_num_dice, player2_name)
    elif player2bot == 4:
        player2_name = "Next Face Bot"
        player2 = Bot_NextFace(max_num_dice, player2_name)
    elif player2bot == 5:
        player2_name = "Challenge Bot"
        player2 = Bot_Challenge(max_num_dice, player2_name)
    elif player2bot == 6:
        player2_name = "Probability Bot"
        player2 = ProbabilityBot(max_num_dice, player2_name)

    qbot = QBot(max_num_dice, player1_name)
    game = GameState(qbot, player2)

    wins = { player1_name : 0, player2_name: 0 }
    for i in range(num_rounds):
        winner = simulate_round(game)
        wins[winner.name] += 1
        game.reset_to_round_start()
        if i%100000 == 0:
            qbot.model.saveQFunction("qfunction.txt")

    for key in qbot.model.Q:
        print(key, qbot.model.Q[key])

    print("RESULTS")
    print("Wins for {}: {}\n".format(player1_name, wins[player1_name]))
    print("Wins for {}: {}\n".format(player2_name, wins[player2_name]))


if __name__ == "__main__":
    simulate_rounds()
