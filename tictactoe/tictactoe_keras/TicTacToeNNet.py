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

        # 'lr': 0.001,
        lr = self.args.lr

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

        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(lr))
