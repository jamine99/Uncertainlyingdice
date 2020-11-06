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
