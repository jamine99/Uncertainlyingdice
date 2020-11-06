import random
from agents.player import Player

class ProbabilityBot(Player):
    def __init__(self,numDice, name):
        super().__init__(numDice, name)
        self.threshold = 0.3

    def takeBet(self, state):
        opponent_player = None
        if state.player1 == self:
            opponent_player = state.player2
        else:
            opponent_player = state.player1

        # Challenge if probability of previous bet is below threshold.
        if self.compute_probability(state.prevBet, len(opponent_player.dice)) < self.threshold:
            return "NO"
        else:
            bet_value, bet_num_dice = None, None
            if state.prevBet == None:
                bet_value, bet_num_dice = 1, 0
            else:
                bet_value, bet_num_dice = state.prevBet

            highest_prob_bet = None
            highest_prob = 0
            # Iterate over possible bets that are greater than previous bet.
            for value in range(bet_value, 7):
                for num_dice in range(bet_num_dice, state.totDice()):
                    # Skip if previous bet is the same and therefore invalid.
                    if value == bet_value and num_dice == bet_num_dice: continue
                    # Compute probabilities and cache most probable.
                    prob = self.compute_probability((value, num_dice), len(opponent_player.dice))
                    if prob > highest_prob:
                        highest_prob_bet = (value, num_dice)
                        highest_prob = prob

            if highest_prob_bet == None: return "no"

            return " ".join([str(element) for element in list(highest_prob_bet)])

    def compute_probability(self, bet, opponent_num_dice):
        if bet == None:
            return 1

        bet_value, bet_num_dice = bet

        # Account for dice in bot's hand and reframe as probability of remaining
        # dice in opponent's hand.
        for dice_val in self.dice:
            if dice_val == bet_value:
                bet_num_dice -= 1

        # Probability of there being greater than or equal to a certain number
        # of dice can be written as the probability of all cases (1) minus the
        # probability of cases that have less than the number of dice.
        prob = 1
        for i in range(bet_num_dice):
            prob -= (5.0 / 6.0) ** (opponent_num_dice - i) * (1.0 / 6.0) ** i

        return prob
