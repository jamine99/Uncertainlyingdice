import collections
import random
from action import Action

class QLearning:
    def __init__(self, action, A, gamma, alpha):
        self.S = enumerateStateList() # state space (assumes 1:nstates)
        self.action = action
        self.A = A # action space (assumes 1:nactions)
        self.gamma = gamma # discount
        self.Q = collections.defaultdict(float) # action value function
        self.alpha = alpha # learning rate

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
    # input is some dataframe
    # for i in 1:size(df)[1]
    #     # for each row in the dataframe
    #     s = df[i, 1]
    #     a = df[i, 2]
    #     r = df[i, 3]
    #     s′ = df[i, 4]
    model.Q[s,a] += model.alpha*(r + model.gamma*max(model.Q[s_prime, a] for a in model.A) - model.Q[s,a])
        #model = update!(model, s, a, r, s′)
        #print(model.Q[s,a]); print("\n")
    # end
    #print(model.Q)
    # return model
# end

def ql_neighbors(s, a, r, s_prime, model):
    # input is some dataframe
    # for i in 1:size(df)[1]
    #     # for each row in the dataframe
    #     s = df[i, 1]
    #     a = df[i, 2]
    #     r = df[i, 3]
    #     s′ = df[i, 4]
    if model.Q[s,a] == 0:
        neighbors_Q = 0
        for k in range(-20,20):
            # 40 nearest states (bets with same quantity of dice and bets where we have same amount of same dice)
            if s-k > 0 and s-k < 50000:
                neighbors_Q += ((1/(abs(k)+1))*model.Q[s-k, a])
        #     end
        # end
        model.Q[s,a] += model.alpha*(r + model.gamma*max(model.Q[s_prime, a] for a in model.A) - neighbors_Q)
        #print(model.Q[s,a])
    else:
        model.Q[s,a] += model.alpha*(r + model.gamma*max(model.Q[s_prime, a] for a in model.A) - model.Q[s,a])
    #     end
    #     #model = update!(model, s, a, r, s′)
    #     #print(model.Q[s,a]); print("\n")
    # end
    # print(model.Q)
    # return model
# end

def explore(pi, model, s):
    A, epsilon = model.A, pi.epsilon
    if random.random() < epsilon:
        print("random action")
        return random.choice(model.action.possible_actions(s))
    else:
        maxScore = -100
        maxAction= 1
        for action in model.action.possible_actions(s):
            currScore = lookahead(model,s,action)
            if currScore > maxScore:
                maxAction = action
                maxScore = currScore
        print("Max action: ", maxAction)
        return maxAction


def make_policy(pol, model):
    # for each state
    for s in model.S:
        # set pi(state) = action that maximizes Q[s,a]
        max_Q_val = -float("inf")
        max_action = 1
        for a in model.A:
            if model.Q[s,a] > max_Q_val and model.Q[s,a] != 0:
                max_Q_val = model.Q[s,a]
                max_action = a
            pol[s] = max_action
    return pol
