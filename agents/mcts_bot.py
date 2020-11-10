from agents.player import Player
from mcts_state import MctsState
from action import Action

from agents.bot_challenge import Bot_Challenge

from mcts import mcts

class MctsBot(Player):
    def __init__(self, numDice, name):
        super().__init__(numDice, name)

    def takeBet(self, state):
        # Update opponent to internal  model.
        original_opponent = state.player2
        state.player2 = Bot_Challenge(self.num_dice, "Challenge Bot")

        # Find best action by Monte Carlo Tree Search simulation.
        action_resolver = Action()
        initialState = MctsState(state, action_resolver)
        mcts_algo = mcts(timeLimit=100)
        action = mcts_algo.search(initialState=initialState)

        action = int(action)

        # Reset to original  opponenent.
        state.player2 = original_opponent

        if action == 0:
            return "no"

        return " ".join([str(element) for element in action_resolver.get_bet(action)])
