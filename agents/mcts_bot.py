from agents.player import Player
from mcts_state import MctsState
from action import Action
from mcts import mcts

class MctsBot(Player):
    def __init__(self, numDice, name):
        super().__init__(numDice, name)

    def takeBet(self, state):
        action_resolver = Action()
        initialState = MctsState(state, action_resolver)
        mcts_algo = mcts(timeLimit=100)
        action = mcts_algo.search(initialState=initialState)

        action = int(action)

        if action == 0:
            return "no"

        return " ".join([str(element) for element in action_resolver.get_bet(action)])
