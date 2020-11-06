from agents.player import Player
import qlearning

class QBot(Player):
    def __init__(self, numDice, name):
        super().__init__(numDice, name)
        self.action = Action()
        self.model = QLearning(self.action.get_all_actions, 0.9, 0.1)
        self.strategy = EpsilonGreedyExploration(0.2, 0.01)

    def takeBet(self, state):
        return explore(self.model, self.strategy, state)
