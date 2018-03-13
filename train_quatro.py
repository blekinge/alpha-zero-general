#!/usr/bin/env python3

# Print linenumbers
import dprint
from Coach import Coach
from quatro.QuatroGame import QuatroGame
from utils import *
from quatro.keras.NNet import NNetWrapper as keras_quatro_neuralnet
from quatro.tensorflow.NNet import NNetWrapper as tensorflow_quatro_neuralnet

dprint.enable()

args = dotdict({
    'numIters': 100,
    'numEps': 20,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__=="__main__":
    # g = OthelloGame(6)
    # nnet = pytorch_othello_neuralnet(g)

    g = QuatroGame(4)
    nnet = tensorflow_quatro_neuralnet(g)


    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
