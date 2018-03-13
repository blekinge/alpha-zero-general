from collections import deque

from pytorch_classification.utils import AverageMeter
from pytorch_classification.utils.progress.progress.bar import Bar

from alpha_zero.Game import Game
from alpha_zero.NeuralNet import NeuralNet
from alpha_zero.Arena import Arena
from alpha_zero.MCTS import MCTS
import numpy as np
import time, os, sys
from pickle import Pickler, Unpickler
from random import shuffle


class Coach():
    """
    This class executes the self-play + learning. It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """

    def __init__(self, game: Game, nnet: NeuralNet, args):
        self.game = game
        self.nnet = nnet
        self.pnet = self.nnet.__class__(self.game)  # the competitor network

        self.args = args

        self.tempThreshold = args.tempThreshold
        self.updateThreshold = args.updateThreshold
        self.load_folder_file = args.load_folder_file
        self.checkpoint = args.checkpoint
        self.numIters = args.numIters
        self.maxlenOfQueue = args.maxlenOfQueue
        self.numEps = args.numEps
        self.numItersForTrainExamplesHistory = args.numItersForTrainExamplesHistory
        self.arenaCompare = args.arenaCompare


        self.mcts = MCTS(self.game, self.nnet, self.args)
        self.trainExamplesHistory = []  # history of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False  # can be overriden in loadTrainExamples()

    def executeEpisode(self):
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temperature=1 if episodeStep < tempThreshold, and thereafter
        uses temperature=0.

        :returns trainExamples: a list of examples of the form (canonicalBoard, action_prop_vector, v)
                           action_prop_vector is the MCTS informed policy vector,
                           v is +1 ifthe player eventually won the game, else -1.
        """
        trainExamples = []
        board = self.game.getInitBoard()
        self.curPlayer = 1
        episodeStep = 0

        while True:
            episodeStep += 1
            canonicalBoard = self.game.getCanonicalForm(board, self.curPlayer)
            temperature = int(episodeStep < self.tempThreshold)

            action_prop_vector = self.mcts.getActionProb(canonicalBoard, temperature=temperature)
            symmetries = self.game.getSymmetries(canonicalBoard, action_prop_vector)
            for board, action_prop_for_board in symmetries:
                trainExamples.append([board, self.curPlayer, action_prop_for_board, None])

            action = np.random.choice(len(action_prop_vector), p=action_prop_vector)
            board, self.curPlayer = self.game.getNextState(board, self.curPlayer, action)

            r = self.game.getGameEnded(board, self.curPlayer)

            if r != 0:
                #example[0]: Board
                #example[2]: action_prop_for_board
                #example[1]: player

                return [(example[0], example[2], r * ((-1) ** (example[1] != self.curPlayer))) for example in trainExamples]

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, self.numIters + 1):

            # bookkeeping
            print('------ITER ' + str(i) + '------')

            # examples of the iteration
            if not self.skipFirstSelfPlay or i > 1:
                iterationTrainExamples = deque([], maxlen=self.maxlenOfQueue)

                eps_time = AverageMeter()
                bar = Bar('Self Play', max=self.numEps)
                end = time.time()

                for eps in range(self.numEps):
                    self.mcts = MCTS(self.game, self.nnet, self.args)  # reset search tree
                    iterationTrainExamples += self.executeEpisode()

                    # bookkeeping + plot progress
                    eps_time.update(time.time() - end)
                    end = time.time()
                    bar.suffix = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(
                        eps=eps + 1, maxeps=self.numEps, et=eps_time.avg,
                        total=bar.elapsed_td, eta=bar.eta_td)
                    bar.next()
                bar.finish()

                # save the iteration examples to the history 
                self.trainExamplesHistory.append(iterationTrainExamples)

            if len(self.trainExamplesHistory) > self.args.numItersForTrainExamplesHistory:
                print("len(trainExamplesHistory) =", len(self.trainExamplesHistory),
                      " => remove the oldest trainExamples")
                self.trainExamplesHistory.pop(0)
            # backup history to a file
            # NB! the examples were collected using the model from the previous iteration, so (i-1)  
            self.saveTrainExamples(i - 1)

            # shuffle examlpes before training
            trainExamples = []
            for e in self.trainExamplesHistory:
                trainExamples.extend(e)
            shuffle(trainExamples)

            # training new network, keeping a copy of the old one
            self.nnet.save_checkpoint(folder=self.checkpoint, filename='temp.pth.tar')
            self.pnet.load_checkpoint(folder=self.checkpoint, filename='temp.pth.tar')
            pmcts = MCTS(self.game, self.pnet, self.args)

            self.nnet.train(trainExamples)
            nmcts = MCTS(self.game, self.nnet, self.args)


            print('PITTING AGAINST PREVIOUS VERSION')
            arena = Arena(lambda board: np.argmax(pmcts.getActionProb(board, temperature=0)),
                          lambda board: np.argmax(nmcts.getActionProb(board, temperature=0)), self.game)
            pwins, nwins, draws = arena.play_games(self.arenaCompare)

            print(f'NEW/PREV WINS : {nwins} / {pwins} ; DRAWS : {draws}')
            print("")

            if pwins + nwins > 0 and float(nwins) / (pwins + nwins) < self.updateThreshold:
                print('REJECTING NEW MODEL')
                self.nnet.load_checkpoint(folder=self.checkpoint, filename='temp.pth.tar')
            else:
                print('ACCEPTING NEW MODEL')
                self.nnet.save_checkpoint(folder=self.checkpoint, filename=self.getCheckpointFile(i))
                self.nnet.save_checkpoint(folder=self.checkpoint, filename='best.pth.tar')

    def getCheckpointFile(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, iteration):
        print("Saving training examples from iteration "+str(iteration))
        folder = self.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration) + ".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed

    def loadTrainExamples(self):
        modelFile = os.path.join(self.load_folder_file[0], self.load_folder_file[1])
        examplesFile = modelFile + ".examples"
        if not os.path.isfile(examplesFile):
            print(examplesFile)
            r = input("File with trainExamples not found. Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            print("File with trainExamples found. Read it.")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            f.closed
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True
