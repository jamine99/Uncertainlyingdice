from agents.player import Player
from qlearning import QLearning, EpsilonGreedyExploration, explore
from action import Action

class QBot(Player):
    def __init__(self, numDice, name):
        super().__init__(numDice, name)
        self.action = Action()
        self.model = QLearning(self.action.get_all_actions(), 0.9, 0.1)
        self.strategy = EpsilonGreedyExploration(0.2, 0.01)

    def takeBet(self, state):
        a = explore(self.strategy, self.model, state)
        bet = self.action.get_bet(a)
        if bet[0] == -1:
            return "no"
        else:
            return " ".join(str(element) for element in list(bet))
