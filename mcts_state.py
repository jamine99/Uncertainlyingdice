from gamestate import GameState
from utils import WINNING_ROUND_REWARD, LOSING_ROUND_REWARD, is_valid_bet, checkBet
import copy

class MctsState():
    def __init__(self, game_state, action):
        self.game = game_state
        self.action = action
        self.won = False
        self.lost = False

    def to_string(self):
        # Helper function for debugging purposes.
        string_representation = "Previous bet: {}\n".format(self.game.prevBet)
        string_representation += "Action: {}\n".format(self.action)
        string_representation += "Win: {}\n".format(self.won)
        string_representation += "Lose: {}".format(self.lost)
        return string_representation

    def getPossibleActions(self):
        # Get possible actions from the action class.
        actions = self.action.possible_actions(self.game)
        return [str(action) for action in actions]

    def takeAction(self, action):
        newState = copy.deepcopy(self)
        newState.game.player2.roll_dice()

        # Convert action to an int as required by action class.
        action = int(action)

        # if action is challenge, update state to terminal state.
        if action == 0:
            # print("Self Challenge")
            prevBetCorrect = checkBet(newState.game)
            if prevBetCorrect:
                newState.lost = True
                # print(newState.to_string())
                newState.game = None
                return newState
            else:
                newState.won = True
                # print(newState.to_string())
                newState.game = None
                return newState

        # Update previous bet to be the current action.
        newState.game.setPrevBet(self.action.get_bet(action))

        # Get the opponent's bet as the next state.
        while True:
            currBet = newState.game.player2.takeBet(newState.game)

            # If opponent challenges, transition to a terminal state.
            if currBet.lower() == "no":
                # print("P2 Challenge")
                prevBetCorrect = checkBet(newState.game)
                if prevBetCorrect:
                    newState.won = True
                    # print(newState.to_string())
                    newState.game = None
                    return newState
                else:
                    newState.lost = True
                    # print(newState.to_string())
                    newState.game = None
                    return newState

            currBetSplit = currBet.split()
            if is_valid_bet(newState.game, currBetSplit): break

        newState.game.setPrevBet(tuple([int(currBetSplit[0]), int(currBetSplit[1])]))
        # print("Bet")
        # print(newState.to_string())
        return newState

    def isTerminal(self):
        is_terminal = self.lost or self.won
        # print("TERMINAL state:", is_terminal)
        return is_terminal

    def getReward(self):
        if self.won:
            return WINNING_ROUND_REWARD
        elif self.lost:
            return LOSING_ROUND_REWARD
        else:
            return False
