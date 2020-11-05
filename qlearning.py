class QLearning:
    def __init__(self, S, A, gamma, Q, alpha):
        self.S # state space (assumes 1:nstates)
        self.A = A # action space (assumes 1:nactions)
        self.gamma = gamma # discount
        self.Q = Q # action value function
        self.alpha = alpha # learning rate

class EpsilonGreedyExploration(self, epsilon, alpha):
    def __init__(self, epsilon, alpha):
        self.epsilon = epsilon
        self.alpha = alpha

def lookahead(model, s, a):
    return model.Q[s,a]

def ql(s, a, r, s_prime, model):
    # input is some dataframe
    # for i in 1:size(df)[1]
    #     # for each row in the dataframe
    #     s = df[i, 1]
    #     a = df[i, 2]
    #     r = df[i, 3]
    #     s′ = df[i, 4]
    model.Q[s,a] += model.α*(r + model.γ*maximum(model.Q[s′,:]) - model.Q[s,a])
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
        for k in -20:20:
            # 40 nearest states (bets with same quantity of dice and bets where we have same amount of same dice)
            if s-k > 0 && s-k < 50000:
                neighbors_Q += ((1/(abs(k)+1))*model.Q[s-k, a])
        #     end
        # end
        model.Q[s,a] += model.α*(r + model.γ*maximum(model.Q[s′,:]) - neighbors_Q)
        #print(model.Q[s,a])
    else
        model.Q[s,a] += model.α*(r + model.γ*maximum(model.Q[s′,:]) - model.Q[s,a])
    #     end
    #     #model = update!(model, s, a, r, s′)
    #     #print(model.Q[s,a]); print("\n")
    # end
    # print(model.Q)
    # return model
# end

def explore(pi, model, s):
    A, epsilon = model.A, pi.epsilon
    if rand() < epsilon:
        return rand(A)
    else:
        Q(s,a) = lookahead(model, s, a)
        return _argmax(a->Q(s,a), A)



def make_policy(pol, model):
    # for each state
    for s in model.S
        # set pi(state) = action that maximizes Q[s,a]
        max_Q_val = -float("inf")
        max_action = 1
        for a in model.A:
            if model.Q[s,a] > max_Q_val && model.Q[s,a] != 0:
                max_Q_val = model.Q[s,a]
                max_action = a
            pol[s] = max_action
    return pol

small_df = DataFrame!(CSV.File("data/small.csv"))
nstates_small = 100
nactions_small = 4
Q_small = zeros(nstates_small, nactions_small)
S_small = 1:nstates_small
A_small = 1:nactions_small
γ_small = 0.95
α_small = 0.2


ϵ = 0.1 # probability of random action
α = 1.0 # exploration decay factor
π = EpsilonGreedyExploration(ϵ, α)

#call exploration func


small_model = QLearning(S_small, A_small, γ_small, Q_small, α_small)
small_pol = zeros(nstates_small)
ql(small_df, small_model)
final_small_pol = make_policy(small_pol, small_model)
writedlm("small.policy", final_small_pol)
