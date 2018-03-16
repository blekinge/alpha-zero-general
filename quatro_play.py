
"""
use this script to play any two agents against each other, or play manually with
any agent.
"""
from alpha_zero.Arena import Arena
from alpha_zero.utils import dotdict
from quatro.QuatroDisplay import display
from quatro.QuatroGame import QuatroGame
from quatro.QuatroPlayers import RandomPlayer, HumanPlayer, KerasNeuralNetPlayer

game = QuatroGame(5)

# all players
random_player1 = RandomPlayer(game,"random1")
random_player2 = RandomPlayer(game,"random2")
human_player = HumanPlayer(game,"human")

# nnet players
# neural_net = NNet(game)
# neural_net.load_checkpoint('./pretrained_models/quatro/keras/','best-25eps-25sim-10epch.pth.tar')

args1 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
ai_player = KerasNeuralNetPlayer(game,args1,"AI")

if __name__ == '__main__':

    # arena = Arena(random_player1, human_player, game, display=display)
    arena = Arena(ai_player, random_player1, game, display=display)
    results = arena.play_games(4, verbose=True)
    print(results)

    results_format = 'Results (Won,Lost,Draws)={0}'.format(results)
    print(results_format)
    print("")

