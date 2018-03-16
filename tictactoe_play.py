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


# nnet players

checkpoints_dir = "./checkpoints/tictactoe/keras/3numIterations-25numEpisodes-15tempThreshold-0.6updateThreshold-200000maxlenOfQueue-25numMCTSSims-40arenaCompare-1cpuct-"
neural_net_player1 = KerasNeuralNetPlayer(game,args1, "Neural_1")
neural_net_player1.load_brain(checkpoints_dir,'best.pth.tar')


if __name__ == '__main__':

    # arena = Arena(neural_net_player1, neural_net_player2, game, display=display)
    arena = Arena(human_player, neural_net_player1, game, display=display)
    results = arena.play_games(2, verbose=True)
    results_format = 'Results {0}'.format(results)
    print(results_format)
    print("")



