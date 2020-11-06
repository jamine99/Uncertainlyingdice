import collections

class state:
    def __init__(self, dice, bet):
        gameMap = collections.defaultdict(int)
        for d in dice:
            if d in gameMap:
                gameMap[d]+=1
            else:
                gameMap[d] = 1
        gameMap[7] = bet[0]
        gameMap[8] = bet[1]
        self.gameMap = gameMap

    def generateNumber(self):
        num = ""
        for i in range(1,9):
            num += str(self.gameMap[i])
        return int(num)

    def saveState(self,filename):
        F = open(filename,"a")
        F.write(self.gameMap)

    def update_bet(self, bet):
        self.gameMap[7] = bet[0]
        self.gameMap[8] = bet[1]

    def get_neighbors(self):
        pass
        # neighbors = []
        #
        # dice_val_of_bet = self.gameMap[7]
        # self.gameMap[dice_value_of_bet]
        #
        # curr_state = [0] * 9
        # curr_state[dice_value_of_bet] = self.gameMap[dice_value_of_bet]
        # curr_state[7] = self.gameMap[7]
        # curr_state[8] = self.gameMap[8]
        #
        # used_indices = [dice_value_of_bet, 7, 8]
        #
        # return neighbors
