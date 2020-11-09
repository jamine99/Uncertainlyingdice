from qlearning import QLearning, find_best_action
from agents.player import Player
from action import Action
import collections

class SavedQBot(Player):
    def __init__(self, numDice, name):
        super().__init__(numDice, name)
        self.action = Action()
        self.model = QLearning(self.action, self.action.get_all_actions(), 0.9, 0.1)
        q_function = collections.defaultdict(float)
        with open("qfunction_vs_saved_q_2.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                s, a, q_value = line.split()
                q_function[(s, a)] = q_value

        self.model.Q = q_function

    def takeBet(self, state):
        a = find_best_action(self.model, state.prev_state.generateNumber(), state)
        bet = self.action.get_bet(a)
        if bet[0] == -1:
            return "no"
        else:
            return " ".join(str(element) for element in list(bet))
