from tictactoe.TicTacToeDisplay import display
from tictactoe.TicTacToeGame import TicTacToeGame
from tictactoe.TicTacToePlayers import HumanPlayer, RandomPlayer, KerasNeuralNetPlayer
from alpha_zero.Arena import Arena
from alpha_zero.utils import dotdict



"""
use this script to play any two agents against each other, or play manually with
any agent.
"""


game = TicTacToeGame(3)

# all players
random_player1 = RandomPlayer(game, "Random1")
random_player2 = RandomPlayer(game, "Random1")
human_player = HumanPlayer(game, "Human")
args1 = dotdict({'numMCTSSims': 25, 'cpuct': 1.0})

neural_net_player1 = KerasNeuralNetPlayer(game,args1, "Neural_1")

neural_net_player2 = KerasNeuralNetPlayer(game,args1, "Neural_1")


if __name__ == '__main__':

    # arena = Arena(neural_net_player1, neural_net_player2, game, display=display)
    arena = Arena(human_player, neural_net_player2, game, display=display)
    results = arena.play_games(20, verbose=True)
    results_format = 'Results {0}'.format(results)
    print(results_format)
    print("")



