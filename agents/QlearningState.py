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

    #inSANElyEpic
    def enumerateStateList(self):
        ret = []
        for a in range(1,7):
            for b in range(1,7):
                for c in range(1,7):
                    for d in range(1,7):
                        for e in range(1,7):
                            for f in range(1,7):
                                for g in range(1,11):
                                    currState = ""
                                    currState += str(a)+str(b)+str(c)+str(d)+str(e)+str(f)+str(g)
                                    ret+= int(currState)
        return ret

    def saveState(self,filename):
        F = open(filename,"a")
        F.write(self.gameMap)
