from collections import Counter

class reduced_State:
    def __init__(self,dice,bet):
        self.data = []
        valDice, numDice = bet
        self.data.append(valDice)
        self.data.append(numDice)
        selfBetDice = 0
        selfMostDice = 0
        selfNumMostDice = 0
        d = Counter(dice)
        for i in range(1,7):
            if d[i] > selfMostDice:
                selfMostDice = i
                selfNumMostDice = d[i]
            if i == valDice:
                selfBetDice = d[i]
        self.data.append(selfBetDice)
        self.data.append(selfMostDice)

    def generateNumber(self):
        num = ""
        for i in self.data:
            num += str(i)
        return int(num)
        
