import random

class Player:
    def __init__(self,numDice,name):
        self.num_dice = numDice
        self.dice = [random.randint(1,6) for i in range(self.num_dice)]
        self.name = name

    def roll_dice(self):
        self.dice = [random.randint(1,6) for i in range(self.num_dice)]

    def lose_dice(self):
        self.num_dice -= 1

    def has_no_dice(self):
        return self.num_dice == 0

    def show_dice(self):
        print("Dice: " + ", ".join([str(dice) for dice in self.dice]))

    def takeBet(self,state):
        return input(self.name + ", please enter your bet <value of dice> <number of dice> or NO to challenge previous bet: ")
