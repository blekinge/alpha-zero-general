from Game import Game
from quatro.QuatroGame import QuatroGame

if __name__ == '__main__':
    action = 234
    game = QuatroGame()
    game.getInitBoard()

    print(action)
    print(game.encodeAction(game.decodeAction(action)))
    print(game.prettyprint_action(action))