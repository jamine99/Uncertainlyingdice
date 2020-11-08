import collections
import random

class QLearning:
    def __init__(self, action, A, gamma, alpha):
        self.S = enumerateStateList() # state space (assumes 1:nstates)
        self.action = action
        self.A = A # action space (assumes 1:nactions)
        self.gamma = gamma # discount
        self.Q = collections.defaultdict(float) # action value function
        self.alpha = alpha # learning rate

    def saveQFunction(self,fileName):
        f = open(fileName,"w")
        for key,value in self.Q:
            x = str(key)
            f.write(x + "," + str(value))


class EpsilonGreedyExploration:
    def __init__(self, epsilon, alpha):
        self.epsilon = epsilon
        self.alpha = alpha

def lookahead(model, s, a):
    return model.Q[s,a]

#inSANElyEpic generateFullStatespace
#def enumerateStateList():
#    ret = []
#    ret.append(-1)
#    ret.append(1)
#    for a in range(0,6):
#        for b in range(0,5-a+1):
#            for c in range(0,5-a-b+1):
#                for d in range(0,5-a-b-c+1):
#                    for e in range(0,5-a-b-c-d+1):
#                        for f in range(1,7):
#                            for g in range(1,11):
#                                currState = ""
#                                currState += str(a)+str(b)+str(c)+str(d)+str(e)+str(f)+str(g)
#                                ret.append(int(currState))

def enumerateStateList():
    ret = []
    ret.append(-1)
    ret.append(1)
    for a in range(1,7):
        for b in range(1,10):
            for c in range(1,5):
                for d in range(1,5):
                    currState = ""
                    currState += str(a)+str(b)+str(c)+str(d)
                    ret.append(int(currState))
    return ret

def ql(s, a, r, s_prime, model):
    model.Q[s,a] += model.alpha*(r + model.gamma*max(model.Q[s_prime, a] for a in model.A) - model.Q[s,a])

def ql_neighbors(s, a, r, s_prime, model):
    if model.Q[s,a] == 0:
        neighbors_Q = 0
        for k in range(-20,20):
            # 40 nearest states (bets with same quantity of dice and bets where we have same amount of same dice)
            if s-k > 0 and s-k < 50000:
                neighbors_Q += ((1/(abs(k)+1))*model.Q[s-k, a])
        model.Q[s,a] += model.alpha*(r + model.gamma*max(model.Q[s_prime, a] for a in model.A) - neighbors_Q)
    else:
        model.Q[s,a] += model.alpha*(r + model.gamma*max(model.Q[s_prime, a] for a in model.A) - model.Q[s,a])

def explore(pi, model, s):
    A, epsilon = model.A, pi.epsilon
    if random.random() < epsilon:
        return random.choice(model.action.possible_actions(s))
    else:
        maxScore = -100
        maxAction= 1
        for action in model.action.possible_actions(s):
            currScore = lookahead(model,s,action)
            if currScore > maxScore:
                maxAction = action
                maxScore = currScore
        return maxAction

def make_policy(pol, model):
    for s in model.S:
        max_Q_val = -float("inf")
        max_action = 1
        for a in model.A:
            if model.Q[s,a] > max_Q_val and model.Q[s,a] != 0:
                max_Q_val = model.Q[s,a]
                max_action = a
            pol[s] = max_action
    return pol
