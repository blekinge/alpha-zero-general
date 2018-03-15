from keras.layers import *
from keras.models import *
from keras.optimizers import *

from alpha_zero.Game import Game

"""
NeuralNet for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloNNet by SourKream and Surag Nair.
"""
class TicTacToeNNet():
    def __init__(self, game: Game, args):
        # game params
        self.board_width, self.board_height = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        width = self.board_width
        height = self.board_height
        action_size = self.action_size

        # 'learning_rate': 0.001,
        learning_rate = self.args.learningRate

        # 'dropout': 0.3,
        dropout = self.args.dropout

        # 'num_channels': 512,
        num_channels = self.args.num_channels

        # s: batch_size x width x width
        input_boards = Input(shape=(width, height))

        # batch_size x width x height x 1
        x_image = Reshape((width, height, 1))(input_boards)

        # batch_size x width x height x num_channels
        h_conv1 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(num_channels, 3, padding='same')(x_image)))

        # batch_size x width x height x num_channels
        h_conv2 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(num_channels, 3, padding='same')(h_conv1)))

        # batch_size x width x height x num_channels
        h_conv3 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(num_channels, 3, padding='same')(h_conv2)))

        # batch_size x width x height x num_channels
        h_conv4 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(num_channels, 3, padding='valid')(h_conv3)))

        h_conv4_flat = Flatten()(h_conv4)

        # batch_size x 1024
        s_fc1 = Dropout(dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_conv4_flat))))

        # batch_size x 1024
        s_fc2 = Dropout(dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(s_fc1))))

        # batch_size x self.action_size
        pi = Dense(action_size, activation='softmax', name='pi')(s_fc2)

        # batch_size x 1
        v = Dense(1, activation='tanh', name='v')(s_fc2)

        self.model = Model(inputs=input_boards, outputs=[pi, v])

        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(learning_rate))


        """
        Below are some common definitions that are necessary to know and understand to correctly utilize Keras:
        
        Sample: one element of a dataset.
            Example: one image is a sample in a convolutional network
            Example: one audio file is a sample for a speech recognition model
        
        Batch: a set of N samples. The samples in a batch are processed independently, in parallel. If training, a batch results in only one update to the model.
            A batch generally approximates the distribution of the input data better than a single input. The larger the batch, the better the approximation; however, it is also true that the batch will take longer to process and will still result in only one update. For inference (evaluate/predict), it is recommended to pick a batch size that is as large as you can afford without going out of memory (since larger batches will usually result in faster evaluating/prediction).
        
        Epoch: an arbitrary cutoff, generally defined as "one pass over the entire dataset", used to separate training into distinct phases, which is useful for logging and periodic evaluation.
            When using evaluation_data or evaluation_split with the fit method of Keras models, evaluation will be run at the end of every epoch.
        
        Within Keras, there is the ability to add callbacks specifically designed to be run at the end of an epoch. Examples of these are learning rate changes and model checkpointing (saving).
        
        """