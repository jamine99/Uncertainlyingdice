class Action:
    def __init__(self, num_values=6, num_dice=5):
        self.num_values = num_values
        self.total_num_dice = num_dice * 2

    def get_index(self, bet):
        """
        Given a bet, return the corresponding index.
        """
        value, num_dice = bet
        # Reserve index 0 for challenge bet.
        if value == -1 or num_dice == -1:
            return 0

        # Ensure that bet is in bounds.
        if value > self.num_values or num_dice > self.total_num_dice:
            raise Exception

        bucket = self.total_num_dice * (value - 1)
        index = bucket + (num_dice - 1)
        return index

    def get_bet(self, index):
        """
        Given an index, return the corresponding bet.
        """
        # Reserve index 0 for challenge bet
        if index == 0:
            return (-1, -1)

        # Ensure that index is within bounds.
        if index >= self.num_values * self.total_num_dice:
            raise Exception

        num_dice = (index % self.total_num_dice) + 1
        value = (index // self.total_num_dice) + 1

        return (value, num_dice)

    def get_all_actions(self):
        """
        Return all actions by index.
        """
        return list(range(self.num_values * self.total_num_dice))

    def possible_actions(self, state):
        """
        Generate all possible legal actions given a state.
        """
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

        first = True
        bet_numDice = None
        bet_newDice = None
        betList = []
        for i in range(new_numDice,totalDice+1):
            for j in range(new_dice,7):
                if first:
                    first = False
                else:
                    betList.append((j,i))

        # Include the challenge bet if not first turn.
        if state.prevBet != None:
            betList.append((-1, -1))

        # Turn it into index.
        ret = []
        for i in betList:
            ret.append(self.get_index(i))
        return ret
