import time
from typing import Callable, Tuple

from alpha_zero.Board import Board
from alpha_zero.Game import Game
from pytorch_classification.utils import AverageMeter
from pytorch_classification.utils.progress.progress.bar import Bar


class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self,
                 player1: Callable[[Board], int],
                 player2: Callable[[Board], int],
                 game: Game,
                 display: Callable[[Board], None] = None):
        """

        :param player1: function that takes board as input, return action number
        :param player2: function that takes board as input, return action number
        :param game: Game object
        :param display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example.

        See pit.py for pitting human players/other baselines with each other.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def play_single_game(self, verbose: bool = False) -> float:
        '''
        Executes one episode of a game.

        :param verbose: Print moves
        :return: either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        '''

        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.getInitBoard()
        it = 0
        while self.game.getGameEnded(board, curPlayer) == 0:
            it += 1

            if verbose:
                assert (self.display)
                print("Turn ", str(it), "Player ", str(curPlayer))
                self.display(board)

            canonical_board = self.game.getCanonicalForm(board, curPlayer)

            action = players[curPlayer + 1](canonical_board)

            valids = self.game.getValidMoves(canonical_board, 1)

            if valids[action] == 0:
                # Invalid action selected...
                print(action)
                assert valids[action] > 0

            board, curPlayer = self.game.getNextState(board, curPlayer, action)

        if verbose:
            assert (self.display)
            print("Game over: Turn ", str(it), "Result ", str(self.game.getGameEnded(board, 1)))
            self.display(board)

        return self.game.getGameEnded(board, 1)

    def play_games(self, number_games:int, verbose:bool=False) -> Tuple[int, int, int]:
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        :param number_games: number of games to play
        :param verbose: Print game boards along the way

        :returns oneWon: games won by player1
        :returns twoWon: games won by player2
        :returns draws:  games won by nobody
        """

        eps_time = AverageMeter()
        bar = Bar('Arena.playGames', max=number_games)
        end = time.time()
        eps = 0
        maxeps = int(number_games)

        # Because each game is two games, with sides switched
        number_games = int(number_games / 2)

        draws_first, end, eps, oneWon_first, twoWon_first = self._play_games(bar, end, eps, eps_time, maxeps, number_games, verbose)

        # Switch the players
        self.player1, self.player2 = self.player2, self.player1

        draws_second, end, eps, oneWon_second, twoWon_second = self._play_games(bar, end, eps, eps_time, maxeps, number_games, verbose)

        # Switch the players back
        self.player1, self.player2 = self.player2, self.player1

        bar.finish()

        return oneWon_first+twoWon_second, twoWon_first+oneWon_second, draws_first+draws_second

    def _play_games(self, bar: Bar, end: float, eps:int, eps_time: AverageMeter, maxeps: int, number_games: int, verbose:bool) -> Tuple[int,float,int,int,int]:
        '''
        Play a set of games

        :param bar: the bar chart to update with wins and losses
        :param end: timestamp
        :param eps: ?
        :param eps_time: ?
        :param maxeps: ?
        :param number_games: number of games to play
        :param verbose: verbose mode
        :returns draws: number of draws
        :returns end: timestamp...
        :returns eps: ?
        :returns oneWon: number of games player 1 won
        :returns twoWon: number of games player 2 won
        '''

        oneWon = 0
        twoWon = 0
        draws = 0

        for _ in range(number_games):
            gameResult = self.play_single_game(verbose=verbose)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1
            # bookkeeping + plot progress
            eps += 1
            eps_time.update(time.time() - end)
            end = time.time()

            bar.suffix = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps + 1,
                                                                                                       maxeps=maxeps,
                                                                                                       et=eps_time.avg,
                                                                                                       total=bar.elapsed_td,
                                                                                                       eta=bar.eta_td)
            bar.next()
        return draws, end, eps, oneWon, twoWon
