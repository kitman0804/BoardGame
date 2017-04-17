import numpy as np
from .GameTree import GameTree


class Minimax(object):
    def __init__(self, hfunc, use_symmetry=False):
        self.hfunc = hfunc
        self.use_symmetry = use_symmetry
    
    def search(self, node, depth):
        root_player = node.root_player
        # Current game
        game = node.game_core
        player = node.player
        gameboard = node.gameboard
        if self.use_symmetry:
            available_coords = gameboard.equivalent_coords_dict.keys()
        else:
            available_coords = gameboard.available_coords
        # Search
        if depth <= 0 or game.winner is not None:
            node.reward = self.hfunc(game=game, player=root_player)
        elif player == root_player:
            best_value = -np.inf
            for coord in available_coords:
                game1 = game.copy()
                game1.place_stone(*coord, player)
                child_node = GameTree(name=coord, game_core=game1, parent=node)
                self.search(node=child_node, depth=depth-1)
                best_value = max(best_value, child_node.reward)
            node.reward = best_value
        else:
            best_value = np.inf
            for coord in available_coords:
                game1 = game.copy()
                game1.place_stone(*coord, player)
                child_node = GameTree(name=coord, game_core=game1, parent=node)
                self.search(node=child_node, depth=depth-1)
                best_value = min(best_value, child_node.reward)
            node.reward = best_value


class AlphaBeta(object):
    def __init__(self, hfunc, equal_sign=True, use_symmetry=False):
        self.hfunc = hfunc
        self.equal_sign = equal_sign
        self.use_symmetry = use_symmetry
    
    def search(self, node, depth, alpha=-np.inf, beta=np.inf):
        root_player = node.root_player
        # Current game
        game = node.game_core
        player = node.player
        gameboard = node.gameboard
        if self.use_symmetry:
            available_coords = gameboard.equivalent_coords_dict.keys()
        else:
            available_coords = gameboard.available_coords
        # Search
        if depth <= 0 or game.winner is not None:
            node.reward = self.hfunc(game=game, player=root_player)
        elif player == root_player:
            best_value = -np.inf
            for coord in available_coords:
                game1 = game.copy()
                game1.place_stone(*coord, player)
                child_node = GameTree(name=coord, game_core=game1, parent=node)
                self.search(node=child_node, depth=depth-1, alpha=alpha, beta=beta)
                best_value = max(best_value, child_node.reward)
                alpha = max(alpha, best_value)
                if beta < alpha:
                    break
                elif beta == alpha and self.equal_sign:
                    break
            node.reward = best_value
        else:
            best_value = np.inf
            for coord in available_coords:
                game1 = game.copy()
                game1.place_stone(*coord, player)
                child_node = GameTree(name=coord, game_core=game1, parent=node)
                self.search(node=child_node, depth=depth-1, alpha=alpha, beta=beta)
                best_value = min(best_value, child_node.reward)
                beta = min(beta, best_value)
                if beta < alpha:
                    break
                elif beta == alpha and self.equal_sign:
                    break
            node.reward = best_value


class ModifiedAlphaBeta(object):
    def __init__(self, hfunc, equal_sign=False, use_symmetry=False):
        self.hfunc = hfunc
        self.equal_sign = equal_sign
        self.use_symmetry = use_symmetry
    
    def search(self, node, depth, alpha=-np.inf, beta=np.inf):
        root_player = node.root_player
        # Current game
        game = node.game_core
        player = node.player
        gameboard = node.gameboard
        if self.use_symmetry:
            available_coords = gameboard.equivalent_coords_dict.keys()
        else:
            available_coords = gameboard.available_coords
        # Search
        if depth <= 0 or game.winner is not None:
            node.reward = self.hfunc(game=game, player=root_player)
        else:
            # Create child nodes and check winner
            win_state_found = False
            for coord in available_coords:
                game1 = game.copy()
                game1.place_stone(*coord, player)
                child_node = GameTree(name=coord, game_core=game1, parent=node)
                if player == child_node.game_core.winner:
                    win_state_found = True
                    depth = 1  # No need to search further
            if player == root_player:
                best_value = -np.inf
                for child_node in node.children:
                    self.search(node=child_node, depth=depth-1, alpha=alpha, beta=beta)
                    best_value = max(best_value, child_node.reward)
                    alpha = max(alpha, best_value)
                    if beta < alpha:
                        break
                    elif beta == alpha and self.equal_sign:
                        break
                node.reward = best_value
            else:
                best_value = np.inf
                for child_node in node.children:
                    self.search(node=child_node, depth=depth-1, alpha=alpha, beta=beta)
                    best_value = min(best_value, child_node.reward)
                    beta = min(beta, best_value)
                    if beta < alpha:
                        break
                    elif beta == alpha and self.equal_sign:
                        break
                node.reward = best_value


class Negamax(object):
    def __init__(self, hfunc, use_symmetry=False):
        self.hfunc = hfunc
        self.use_symmetry = use_symmetry
    
    def search(self, node, depth):
        root_player = node.root_player
        # Current game
        game = node.game_core
        player = node.player
        gameboard = node.gameboard
        if self.use_symmetry:
            available_coords = gameboard.equivalent_coords_dict.keys()
        else:
            available_coords = gameboard.available_coords
        # Search
        if depth <= 0 or game.winner is not None:
            node.reward = self.hfunc(game=game, player=root_player)
        else:
            best_value = -np.inf
            for coord in available_coords:
                game1 = game.copy()
                game1.place_stone(*coord, player)
                child_node = GameTree(name=coord, game_core=game1, parent=node)
                self.search(node=child_node, depth=depth-1)
                best_value = max(best_value, -child_node.reward)
            node.reward = best_value
