
"""
use this script to play any two agents against each other, or play manually with
any agent.
"""
from alpha_zero.Arena import Arena
from alpha_zero.utils import dotdict
from quatro.QuatroDisplay import display
from quatro.QuatroGame import QuatroGame
from quatro.QuatroPlayers import RandomPlayer, HumanPlayer

game = QuatroGame(5)

# all players
random_player1 = RandomPlayer(game).play
random_player2 = RandomPlayer(game).play
human_player = HumanPlayer(game).play

# nnet players
# neural_net = NNet(game)
# neural_net.load_checkpoint('./pretrained_models/quatro/keras/','best-25eps-25sim-10epch.pth.tar')

args1 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})

# monte_carlo_tree_search = MCTS(game, neural_net, args1)
# neural_net_player = lambda x: np.argmax(monte_carlo_tree_search.getActionProb(x, temp=0))

if __name__ == '__main__':

    # arena = Arena.Arena(random_player1, human_player, game, display=display)
    arena = Arena(human_player, random_player2, game, display=display)
    print(arena.play_games(2, verbose=True))
