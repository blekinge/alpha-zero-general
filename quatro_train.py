#!/usr/bin/env python3
from alpha_zero.Coach import Coach
from alpha_zero.utils import dotdict
from quatro.QuatroGame import QuatroGame


from quatro.quatro_keras.NNet import NNetWrapper as keras_neuralnet

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

loadSaveArgs = {'checkpoint': './checkpoints/quatro/keras/' + args_to_filename(model_params),
                'load_model': False,
                'load_folder_file': ('models/quatro/keras/' + args_to_filename(model_params), 'best.pth.tar'),
                'numItersForTrainExamplesHistory': 10}

args = dotdict({**model_params,**loadSaveArgs})


if __name__=="__main__":
    # g = OthelloGame(6)
    # nnet = pytorch_othello_neuralnet(g)

    game = QuatroGame(5)
    nnet = keras_neuralnet(game)


    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(game, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
