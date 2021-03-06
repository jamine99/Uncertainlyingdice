from agents.player import Player
from agents.probabilitybot import ProbabilityBot
from agents.bot_challenge import Bot_Challenge
from agents.bot_nextNum import Bot_NextNum
from agents.bot_nextFace import Bot_NextFace
from agents.random_bot import Random_Bot
from agents.qlearn_bot import QBot
from agents.mcts_bot import MctsBot
from agents.saved_qbot import SavedQBot

from agents.reduced_state import ReducedState
from agents.QlearningState import state

import qlearning
from utils import WINNING_ROUND_REWARD, LOSING_ROUND_REWARD, TERMINAL_LOSE_STATE, TERMINAL_WIN_STATE
from utils import is_valid_bet, checkBet

from gamestate import GameState
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import collections

#plays through one round of da game and returns which player won that round
#P1 always goes first
def round(state):
    print(state.to_string())
    p1 = state.player1
    p2 = state.player2
    currPlayer = p1
    while(True):
        # Show player 1's hand as if we are player 1.
        #if currPlayer == p1:
        #    p1.show_dice()
        # Show current player's dice, can replace with just p1 later on
        currPlayer.show_dice()

        # For the first bet, do not allow challenging.
        if state.prevBet == None:
            print(currPlayer.name + ": First Turn Bet")
            #always set to human first but we dont gotta once we start making bots
            p1Split = None
            while True:
                p1Bet = currPlayer.takeBet(state)
                p1Split = p1Bet.split()
                if is_valid_bet(state, p1Split): break
            print(currPlayer.name + " bet " + p1Split[1] + " dice of value " + p1Split[0])
            state.setPrevBet(tuple([int(p1Split[0]), int(p1Split[1])]))
        else:
            print(currPlayer.name+ "'s Turn")
            #always set to human first but we dont gotta once we start making bots
            currBetSplit = None
            while True:
                currBet = currPlayer.takeBet(state)

                print(currPlayer.name + " bet " + currBet)
                #deal with the challenge
                if currBet.lower() == "no":
                    if currPlayer == p1:
                        opposingPlayer = p2
                    else:
                        opposingPlayer = p1
                    prevBetCorrect = checkBet(state)
                    if prevBetCorrect:
                        print(opposingPlayer.name + " Won This Round!")
                        # currPlayer.lose_dice()
                        return opposingPlayer
                    else:
                        print(currPlayer.name + " Won This Round!")
                        # opposingPlayer.lose_dice()
                        return currPlayer

                currBetSplit = currBet.split()
                if is_valid_bet(state, currBetSplit): break

            print(currPlayer.name + " bet " + currBetSplit[1] + " dice of value " +currBetSplit[0])
            state.setPrevBet(tuple([int(currBetSplit[0]), int(currBetSplit[1])]))

        # Switch which player's turn it is.
        currPlayer = p2 if currPlayer == p1 else p1


def play_game(max_num_dice=5, player1_name="player1", player2_name="player2", num_rounds=10000):
    '''
    Plays one game of Liar's Dice.

    Args:
        max_num_dice (int): the number of dice each player starts with.
        player1_name (string): name for player1
        player2_name (string): name for player2
    '''
    player1bot = int(input("Please enter player 1 type: 1 for human, 2 for random, 3 for nextNum, 4 for nextFace, 5 for challenge, 6 for probability, 7 for savedQBot: "))
    player1 = None
    if player1bot == 1:
        player1 = Player(max_num_dice, player1_name)
    elif player1bot == 2:
        player1_name = "Random Bot"
        player1 = Random_Bot(max_num_dice, player1_name)
    elif player1bot == 3:
        player1_name = "Next Number Bot"
        player1 = Bot_NextNum(max_num_dice, player1_name)
    elif player1bot == 4:
        player1_name = "Next Face Bot"
        player1 = Bot_NextFace(max_num_dice, player1_name)
    elif player1bot == 5:
        player1_name = "Challenge Bot"
        player1 = Bot_Challenge(max_num_dice, player1_name)
    elif player1bot == 6:
        player1_name = "Probability Bot"
        player1 = ProbabilityBot(max_num_dice, player1_name)
    elif player1bot == 7:
        player1_name = "Saved Q Bot"
        player1 = SavedQBot(max_num_dice, player1_name)

    player2bot = int(input("Please enter player 2 type: 1 for human, 2 for random, 3 for nextNum, 4 for nextFace, 5 for challenge, 6 for probability, 7 for savedQBot: "))
    player2 = None
    if player2bot == 1:
        player2 = Player(max_num_dice, player2_name)
    elif player2bot == 2:
        player2_name = "Random Bot"
        player2 = Random_Bot(max_num_dice, player2_name)
    elif player2bot == 3:
        player2_name = "Next Number Bot"
        player2 = Bot_NextNum(max_num_dice, player2_name)
    elif player2bot == 4:
        player2_name = "Next Face Bot"
        player2 = Bot_NextFace(max_num_dice, player2_name)
    elif player2bot == 5:
        player2_name = "Challenge Bot"
        player2 = Bot_Challenge(max_num_dice, player2_name)
    elif player2bot == 6:
        player2_name = "Probability Bot"
        player2 = ProbabilityBot(max_num_dice, player2_name)
    elif player2bot == 7:
        player2_name = "Saved Q Bot"
        player2 = SavedQBot(max_num_dice, player2_name)

    game = GameState(player1, player2)

    wins = { player1_name : 0, player2_name: 0 }
    for i in range(num_rounds):
        winner = round(game)
        wins[winner.name] += 1

        plot_color = ""
        if winner.name == player1_name:
            plot_color = "blue"
        else:
            plot_color = "red"
        plt.scatter(i, wins[winner.name] / (i + 1), color=plot_color)

        game.reset_to_round_start()

    print("RESULTS")
    print("Wins for {}: {}\n".format(player1_name, wins[player1_name]))
    print("Wins for {}: {}\n".format(player2_name, wins[player2_name]))
    plt.title("Percentage of Wins Over Time")
    plt.xlabel("Rounds")
    plt.ylabel("Percentage of Wins")
    player1_legend = mpatches.Patch(color="blue", label=player1_name)
    player2_legend = mpatches.Patch(color="red", label=player2_name)
    plt.legend(handles=[player1_legend, player2_legend])
    plt.show()

    # while True:
    #     if player1.has_no_dice():
    #         print(player2 + " has won the game!")
    #         break
    #     if player2.has_no_dice():
    #         print(player1 + " has won the game!")
    #         break
    #
    #     round(state)
    #     state.reset_to_round_start()
    #
    # if len(player1.dice) == 0:
    #     print(player2 + " has won the game!")
    # else:
    #     print(player1 + " has won the game!")


def simulate_round(game):
    # Print inforamtion
    print(game.to_string())

    qbot = game.player1
    p2 = game.player2
    currPlayer = qbot
    while(True):
        # Show player 1's hand as if we are player 1.
        #if currPlayer == p1:
        #    p1.show_dice()
        # Show current player's dice, can replace with just p1 later on
        currPlayer.show_dice()

        # For the first bet, do not allow challenging.
        if game.prevBet == None:
            print(currPlayer.name + ": First Turn Bet")
            #always set to human first but we dont gotta once we start making bots
            p1Split = None
            while True:
                p1Bet = currPlayer.takeBet(game)
                print(p1Bet)
                p1Split = p1Bet.split()
                if is_valid_bet(game, p1Split): break
            print(currPlayer.name + " bet " + p1Split[1] + " dice of value " + p1Split[0])
            game.setPrevBet(tuple([int(p1Split[0]), int(p1Split[1])]))
        else:
            print(currPlayer.name+ "'s Turn")
            #always set to human first but we dont gotta once we start making bots
            currBetSplit = None
            while True:
                currBet = currPlayer.takeBet(game)
                print(currPlayer.name + " bet " + currBet)

                # Deal with the challenge.
                if currBet.lower() == "no":
                    if currPlayer == qbot:
                        opposingPlayer = p2
                    else:
                        opposingPlayer = qbot

                    if checkBet(game):
                        if currPlayer == p2:
                            qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index(game.prevBet), WINNING_ROUND_REWARD, TERMINAL_WIN_STATE, qbot.model)
                        else:
                            # Current action is a challenge bet denoted as (-1, -1).
                            qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index((-1, -1)), LOSING_ROUND_REWARD, TERMINAL_LOSE_STATE, qbot.model)
                        print(opposingPlayer.name + " Won This Round!")
                        return opposingPlayer
                    else:
                        if currPlayer == p2:
                            qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index(game.prevBet), LOSING_ROUND_REWARD, TERMINAL_LOSE_STATE, qbot.model)
                        else:
                            # Current action is a challenge bet denoted as (-1, -1).
                            qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index((-1, -1)), WINNING_ROUND_REWARD, TERMINAL_WIN_STATE, qbot.model)
                        print(currPlayer.name + " Won This Round!")
                        return currPlayer

                currBetSplit = currBet.split()
                if is_valid_bet(game, currBetSplit): break

            print(currPlayer.name + " bet " + currBetSplit[1] + " dice of value " +currBetSplit[0])
            new_bet = tuple([int(currBetSplit[0]), int(currBetSplit[1])])

            # If not q-learning agent
            if currPlayer == p2:
                new_state = ReducedState(qbot.dice, new_bet)
                qlearning.ql(game.prev_state.generateNumber(), qbot.action.get_index(game.prevBet), 0, new_state.generateNumber(), qbot.model)

            # Right before we update the previous bet to be p1's current bet, we update our prev_state to be the previous bet which is p2's last bet.
            if currPlayer == qbot:
                game.prev_state.update_bet(game.prevBet)

            game.setPrevBet(new_bet)

        # Switch which player's turn it is.
        currPlayer = p2 if currPlayer == qbot else qbot


def simulate_rounds(max_num_dice=5, player1_name="AgentQ", player2_name="player2", num_rounds=100000):
    '''
    Simulates many rounds of Liar's Dice for QLearning.

    Args:
        max_num_dice (int): the number of dice each player starts with.
        player1_name (string): name for player1
        player2_name (string): name for player2
    '''
    player2bot = int(input("Please enter player 2 type: 1 for human, 2 for random, 3 for nextNum, 4 for nextFace, 5 for challenge, 6 for probability, 7 for savedQBot: "))
    player2 = None
    if player2bot == 1:
        player2 = Player(max_num_dice, player2_name)
    elif player2bot == 2:
        player2_name = "Random Bot"
        player2 = Random_Bot(max_num_dice, player2_name)
    elif player2bot == 3:
        player2_name = "Next Number Bot"
        player2 = Bot_NextNum(max_num_dice, player2_name)
    elif player2bot == 4:
        player2_name = "Next Face Bot"
        player2 = Bot_NextFace(max_num_dice, player2_name)
    elif player2bot == 5:
        player2_name = "Challenge Bot"
        player2 = Bot_Challenge(max_num_dice, player2_name)
    elif player2bot == 6:
        player2_name = "Probability Bot"
        player2 = ProbabilityBot(max_num_dice, player2_name)
    elif player2bot == 7:
        player2_name = "Saved Q Bot"
        player2 = SavedQBot(max_num_dice, player2_name)

    qbot = QBot(max_num_dice, player1_name)
    q_function = collections.defaultdict(float)
    with open("qfunction_0.49.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            s, a, q_value = line.split()
            q_function[(s, a)] = q_value
    qbot.model.q = q_function
    game = GameState(qbot, player2)

    wins = { player1_name : 0, player2_name: 0 }
    for i in range(num_rounds):
        winner = simulate_round(game)
        wins[winner.name] += 1

        plot_color = ""
        if winner.name == player1_name:
            plot_color = "blue"
        else:
            plot_color = "red"
        plt.scatter(i, wins[winner.name] / (i + 1), color=plot_color)

        game.reset_to_round_start()
        if (i + 1) % 10000 == 0:
            print("HERE")
            qbot.model.saveQFunction("qfunction.txt")

    for key in qbot.model.Q:
        print(key, qbot.model.Q[key])

    print("RESULTS")
    print("Wins for {}: {}\n".format(player1_name, wins[player1_name]))
    print("Wins for {}: {}\n".format(player2_name, wins[player2_name]))
    plt.title("Wins Over Time")
    plt.xlabel("Rounds")
    plt.ylabel("Wins")
    player1_legend = mpatches.Patch(color="blue", label=player1_name)
    player2_legend = mpatches.Patch(color="red", label=player2_name)
    plt.legend(handles=[player1_legend, player2_legend])
    plt.show()


def run_mcts_simulation(max_num_dice=5, player1_name="MctsBot", player2_name="player2", num_rounds=10000):
    """
    Set up and simulate many rounds using Monte Carlo Tree Search (mcts).

    Args:
        max_num_dice (int): the number of dice each player starts with.
        player1_name (string): name for player1
        player2_name (string): name for player2
    """
    player2bot = int(input("Please enter player 2 type: 1 for human, 2 for random, 3 for nextNum, 4 for nextFace, 5 for challenge, 6 for probability, 7 for savedQBot: "))
    player2 = None
    if player2bot == 1:
        player2 = Player(max_num_dice, player2_name)
    elif player2bot == 2:
        player2_name = "Random Bot"
        player2 = Random_Bot(max_num_dice, player2_name)
    elif player2bot == 3:
        player2_name = "Next Number Bot"
        player2 = Bot_NextNum(max_num_dice, player2_name)
    elif player2bot == 4:
        player2_name = "Next Face Bot"
        player2 = Bot_NextFace(max_num_dice, player2_name)
    elif player2bot == 5:
        player2_name = "Challenge Bot"
        player2 = Bot_Challenge(max_num_dice, player2_name)
    elif player2bot == 6:
        player2_name = "Probability Bot"
        player2 = ProbabilityBot(max_num_dice, player2_name)
    elif player2bot == 7:
        player2_name = "Saved Q Bot"
        player2 = SavedQBot(max_num_dice, player2_name)

    mctsbot = MctsBot(max_num_dice, player1_name)
    game = GameState(mctsbot, player2)

    wins = { player1_name : 0, player2_name: 0 }
    for i in range(num_rounds):
        winner = simulate_mcts_round(game)
        wins[winner.name] += 1

        plot_color = ""
        if winner.name == player1_name:
            plot_color = "blue"
        else:
            plot_color = "red"
        plt.scatter(i, wins[winner.name] / (i + 1), color=plot_color)

        game.reset_to_round_start()

    print("RESULTS")
    print("Wins for {}: {}\n".format(player1_name, wins[player1_name]))
    print("Wins for {}: {}\n".format(player2_name, wins[player2_name]))
    plt.title("Percentage of Wins Over Time")
    plt.xlabel("Rounds")
    plt.ylabel("Percentage of Wins")
    player1_legend = mpatches.Patch(color="blue", label=player1_name)
    player2_legend = mpatches.Patch(color="red", label=player2_name)
    plt.legend(handles=[player1_legend, player2_legend])
    plt.show()


def simulate_mcts_round(state):
    """
    Simulate one round using an mcts bot. In particular, this means not updating
    any data structures within this function but rather letting the bot simulate
    and do online planning.

    Args:
        state (GameState): state of the game.
    """
    print(state.to_string())
    mctsbot = state.player1
    p2 = state.player2
    player2_true_dice = state.player2.dice
    currPlayer = mctsbot
    while(True):
        # Show player 1's hand as if we are player 1.
        #if currPlayer == p1:
        #    p1.show_dice()
        # Show current player's dice, can replace with just p1 later on
        currPlayer.show_dice()

        if currPlayer == p2:
            state.player2.dice = player2_true_dice

        # For the first bet, do not allow challenging.
        if state.prevBet == None:
            print(currPlayer.name + ": First Turn Bet")
            #always set to human first but we dont gotta once we start making bots
            p1Split = None
            while True:
                p1Bet = currPlayer.takeBet(state)
                p1Split = p1Bet.split()
                if is_valid_bet(state, p1Split): break
            print(currPlayer.name + " bet " + p1Split[1] + " dice of value " + p1Split[0])
            state.setPrevBet(tuple([int(p1Split[0]), int(p1Split[1])]))
        else:
            print(currPlayer.name+ "'s Turn")
            #always set to human first but we dont gotta once we start making bots
            currBetSplit = None
            while True:
                currBet = currPlayer.takeBet(state)

                print(currPlayer.name + " bet " + currBet)
                #deal with the challenge
                if currBet.lower() == "no":
                    if currPlayer == mctsbot:
                        opposingPlayer = p2
                    else:
                        opposingPlayer = mctsbot
                    prevBetCorrect = checkBet(state)
                    if prevBetCorrect:
                        print(opposingPlayer.name + " Won This Round!")
                        return opposingPlayer
                    else:
                        print(currPlayer.name + " Won This Round!")
                        return currPlayer

                currBetSplit = currBet.split()
                if is_valid_bet(state, currBetSplit): break

            print(currPlayer.name + " bet " + currBetSplit[1] + " dice of value " +currBetSplit[0])
            state.setPrevBet(tuple([int(currBetSplit[0]), int(currBetSplit[1])]))

        # Switch which player's turn it is.
        currPlayer = p2 if currPlayer == mctsbot else mctsbot

if __name__ == "__main__":
    run_mcts_simulation()
