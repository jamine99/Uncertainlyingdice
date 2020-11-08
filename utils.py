WINNING_ROUND_REWARD = 10
LOSING_ROUND_REWARD = -10
TERMINAL_WIN_STATE = 1
TERMINAL_LOSE_STATE = -1

def is_valid_bet(state, bet):
    """
    Function to determine if a bet is valid accroding to the rules of the game.

    Args:
        state (GameState): current GameState that contains the previous bet.
        bet (tuple): tuple representng the current bet.
    """
    if len(bet) != 2:
        print("Bet must be in the format <value of dice> <number of dice>.")
        return False

    dice = int(bet[0])
    num_dice = int(bet[1])

    if dice < 1 or dice > 6:
        print("Value of dice must be between 1 and 6.")
        return False

    if num_dice > state.totDice():
        print("Number of dice must be less than or equal to total number of dice.")
        return False

    if state.prevBet != None:
        if dice <= state.prevBet[0] and num_dice <= state.prevBet[1]:
            print("Value of dice or number of dice must be greater than the previous bet's value or number.")
            return False

    return True


def checkBet(state):
    """
    Returns true if the bet is satisfied by the dice on the table else false.
    A bet here is a tuple (value of dice, number of dice).

    Args:
        state (GameState): current game state that contains the previous bet.
    """
    dice = state.prevBet[0]
    numDice = state.prevBet[1]
    count = 0
    for p1Dice in state.player1.dice:
        if p1Dice == dice:
            count+=1
    for p2Dice in state.player2.dice:
        if p2Dice == dice:
            count+=1
    if numDice <= count:
        return True
    return False
