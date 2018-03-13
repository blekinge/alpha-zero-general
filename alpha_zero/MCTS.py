import math
from typing import List

import numpy as np

from alpha_zero.Game import Game
from alpha_zero.NeuralNet import NeuralNet
from alpha_zero.Board import Board


class MCTS():
    """
    This class handles the MCTS tree.
    """

    def __init__(self, game: Game, neural_net: NeuralNet, args):
        self.game = game
        self.nnet = neural_net
        self.cpuct = args.cpuct
        self.numMCTSSims = args.numMCTSSims

        self.expected_reward_for_state_and_action = {}
        '''Qsa. stores Q values for s(tate),a(ction) (as defined in the paper)'''

        self.edge_visited = {}
        '''Nsa. stores #times edge s(tate),a(ction) was visited'''

        self.state_visited = {}
        '''Na. stores #times board s(tate) was visited'''

        self.policy = {}
        '''Ps. stores initial policy (returned by neural net)'''

        self.end_states = {}
        """Es. stores game.getGameEnded ended for board s(tate)"""

        self.valid_moves_for_state = {}
        """Vs. stores game.getValidMoves for board s(tate)"""

    def getActionProb(self, canonicalBoard: Board, temperature=1) -> List[float]:
        """
        This function performs numMCTSSims simulations of MCTS starting from
        canonicalBoard.

        :returns: action policy vector where the probability of the ith action is proportional to Nsa[(state,action)]**(1./temperature)
        """
        for i in range(self.numMCTSSims):
            self.search(canonicalBoard)

        state = self.game.stringRepresentation(canonicalBoard)

        visits_per_action = [self.edge_visited[(state, action)]
                  if (state, action) in self.edge_visited else 0
                  for action in range(self.game.getActionSize())]

        # If cold, only the best action is available
        if temperature == 0:
            best_action = np.argmax(visits_per_action)
            probs = [0] * len(visits_per_action)
            probs[best_action] = 1
            return probs

        # At higher temps, increase probabilities
        visits_per_action = [visits ** (1. / temperature) for visits in visits_per_action]

        # Then normalise
        sum_of_visits = float(sum(visits_per_action))
        probs = [visits / sum_of_visits for visits in visits_per_action]

        return probs

    def search(self, canonicalBoard: Board) -> float:
        """
        This function performs one iteration of MCTS. It is recursively called
        till action leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.

        Once action leaf node is found, the neural network is called to return an
        initial policy P and action value value for the state. This value is propogated
        up the search path. In case the leaf node is action terminal state, the
        outcome is propogated up the search path. The values of Ns, Nsa, Qsa are
        updated.

        NOTE: the return values are the negative of the value of the current
        state. This is done since value is in [-1,1] and if value is the value of action
        state for the current player, then its value is -value for the other player.

        :param canonicalBoard: the board to start from

        :return: the negative of the value of the current canonicalBoard
        """

        state = self.game.stringRepresentation(canonicalBoard)

        # if gameEnded: return -gameReward
        if state not in self.end_states:
            self.end_states[state] = self.game.getGameEnded(canonicalBoard, 1)
        if self.end_states[state] != 0:
            # terminal node
            return -self.end_states[state]

        # if not visited
        if state not in self.policy:
            return self._visit(canonicalBoard, state)

        # Select the best action
        action = self._select_best_action(state)

        next_state, next_player = self.game.getNextState(canonicalBoard, 1, action)

        next_state = self.game.getCanonicalForm(next_state, next_player)

        value = self.search(next_state)

        if (state, action) in self.expected_reward_for_state_and_action:
            exp_reward = self.expected_reward_for_state_and_action[(state, action)]

            edge_visited = self.edge_visited[(state, action)]

            self.expected_reward_for_state_and_action[(state, action)] = (edge_visited * exp_reward + value) / (
                    edge_visited + 1)

            self.edge_visited[(state, action)] += 1

        else:
            self.expected_reward_for_state_and_action[(state, action)] = value

            self.edge_visited[(state, action)] = 1

        self.state_visited[state] += 1

        return -value

    def _select_best_action(self, state: str) -> int:
        '''
        Select the action that maximises the upper confidence bounds on expected reward for this game state

        :param state: the game state
        :return: action: The action (number)
        '''
        valid_moves = self.valid_moves_for_state[state]
        current_best = -float('inf')
        best_action = -1
        # pick the action with the highest upper confidence bound
        for action in range(self.game.getActionSize()):
            if valid_moves[action]:

                policy = self.policy[state][action]
                sqrt_visited = math.sqrt(self.state_visited[state])
                edge_visited = self.edge_visited[(state, action)] if (state, action) in self.edge_visited else 0

                if (state, action) in self.expected_reward_for_state_and_action:
                    expected_reward = self.expected_reward_for_state_and_action[(state, action)]
                else:
                    expected_reward = 0

                upper_confidence_bounds_on_expected_reward = \
                    expected_reward + self.cpuct * policy * sqrt_visited / (1 + edge_visited)

                if upper_confidence_bounds_on_expected_reward > current_best:
                    current_best = upper_confidence_bounds_on_expected_reward
                    best_action = action
        action = best_action
        return action

    def _visit(self, canonicalBoard: Board, state: str) -> float:
        # Means this is a leaf node

        # Predict the policy and value for this board state
        self.policy[state], v = self.nnet.predict(canonicalBoard)

        # Mask invalid moves
        self.valid_moves_for_state[state] = self.game.getValidMoves(canonicalBoard, 1)  # Fixed size boolean vector,
        self.policy[state] = self.policy[state] * self.valid_moves_for_state[
            state]  # So the policy for the invalid set to 0

        # Sum the remaining moves
        sum_policy_for_state = np.sum(self.policy[state])

        if sum_policy_for_state > 0:
            # renormalize
            self.policy[state] /= sum_policy_for_state
        else:
            # if all valid moves were masked make all valid moves equally probable

            # NB! All valid moves may be masked if either your NNet architecture is insufficient or you've get overfitting or something else.
            # If you have got dozens or hundreds of these messages you should pay attention to your NNet and/or training process.
            print("All valid moves were masked, do workaround.")
            self.policy[state] = self.policy[state] + self.valid_moves_for_state[state]
            self.policy[state] /= np.sum(self.policy[state])

        self.state_visited[state] = 0
        return -v
