#!/usr/bin/env python3
import pathlib

from alpha_zero.Coach import Coach
from alpha_zero.utils import dotdict

from tictactoe.TicTacToeGame import TicTacToeGame
from tictactoe.tictactoe_keras.NNet import NNetWrapper as keras_tictactoe_neuralnet


# Print linenumbers
# from alpha_zero import dprint
# dprint.enable()

def args_to_filename(args: dict):
    filename = ""
    for key, value in args.items():
        filename += f"{value}{key}-"
    return filename


model_params = {
    'numIters': 100,
    'numEps': 10,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,
}

loadSaveArgs = {'checkpoint': './checkpoints/tictactoe/keras/' + args_to_filename(model_params),
                'load_model': False,
                'load_folder_file': ('models/tictactoe/keras/' + args_to_filename(model_params), 'best.pth.tar'),
                'numItersForTrainExamplesHistory': 10}

args = dotdict({**model_params,**loadSaveArgs})

if __name__ == "__main__":

    game = TicTacToeGame(3)
    nnet = keras_tictactoe_neuralnet(game)
    c = Coach(game, nnet, args)

    pathlib.Path(args.checkpoint).mkdir(parents=True, exist_ok=True)
    if args.load_model:
        pathlib.Path(args.load_folder_file[0]).mkdir(parents=True, exist_ok=True)

        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
