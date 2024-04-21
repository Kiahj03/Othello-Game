import math
import random

import game

class HumanPlayer(game.Player):

    def __init__(self):
        super().__init__()

    def choose_move(self, state):
        # generate the list of moves:
        moves = state.generateMoves()

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]

class RandomAgent(game.Player):
    def choose_move(self, state):
        moves = state.generateMoves()

        if moves:
            return random.choice(moves)
        else:
            return None

class MinimaxAgent(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.depth = depth

    def choose_move(self, state):
        move = self.minimax(state, self.depth)
        return move
    
    def minimax(self, state, depth):
        player = state.nextPlayerToMove
        value, move = self.max_value(state, player, depth)
        return move
    
    def max_value(self, state, player, depth):
        if depth == 0 or state.game_over():
            return state.score(), None
        
        v = -math.inf
        move = None

        moves = state.generateMoves(player)
        for m in moves:
            new_state = state.applyMoveCloning(m)
            v2, a2 = self.min_value(new_state, player, depth - 1)

            if v2 > v:
                v, move = v2, m
        return v, move
    
    def min_value(self, state, player, depth):
        if depth == 0 or state.game_over():
            return state.score(), None
        
        v = math.inf
        move = None

        moves = state.generateMoves(player)
        for m in moves:
            new_state = state.applyMoveCloning(m)
            v2, a2 = self.max_value(new_state, player, depth - 1)

            if v2 < v:
                v, move = v2, m
        return v, move

class AlphaBeta(game.Player):
    def __init__(self, depth):
        super().__init__()
        self.depth = depth

    def choose_move(self, state):
        move = self.alphabeta(state, self.depth)
        return move
    
    def alphabeta(self, state, depth):
        alpha = -math.inf
        beta = math.inf
        player = state.nextPlayerToMove
        value, move = self.max_value(state, player, depth, alpha, beta)
        return move
    
    def max_value(self, state, player, depth, alpha, beta):
        if depth == 0 or state.game_over():
            return state.score(), None
        
        v = -math.inf
        move = None

        moves = state.generateMoves(player)
        for m in moves:
            new_state = state.applyMoveCloning(m)
            v2, a2 = self.min_value(new_state, player, depth - 1, alpha, beta)

            if v2 > v:
                v, move = v2, m
                alpha = max(alpha, v)

            if v >= beta:
                return v, move
        return v, move

    def min_value(self, state, player, depth, alpha, beta):
        if depth == 0 or state.game_over():
            return state.score(), None
        
        v = math.inf
        move = None

        moves = state.generateMoves(player)
        for m in moves:
            new_state = state.applyMoveCloning(m)
            v2, a2 = self.max_value(new_state, player, depth - 1, alpha, beta)

            if v2 < v:
                v, move = v2, m
                beta = min(beta, v)
                
            if v <= alpha:
                return v, move
        return v, move