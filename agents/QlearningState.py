class state:
    def __init__(self, dice, bet):
        gameMap = {}
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
            num += str(gameMap[i])
        return int(num)

    def saveState(self,filename):
        F = open(filename,"a")
        F.write(self.gameMap)
