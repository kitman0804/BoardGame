import numpy as np
from anytree import Node, RenderTree


class GameTree(Node):
    def __init__(self, name, game, parent=None):
        super().__init__(name=name, parent=parent)
        self._game = game
        self._reward = None
    
    def __repr__(self):
        print_text = '<Node ({:}, {:}, {:.2f})>'
        print_text = print_text.format(
            self.name,
            '_' if self._game.winner is None else self._game.winner,
            np.nan if self.reward is None else self.reward
        )
        return print_text
    
    @property
    def reward(self):
        return self._reward
    
    @reward.setter
    def reward(self, x):
        self._reward = x
    
    @property
    def size(self):
        return 1 + len(self.descendants)
    
    @property
    def leaves(self):
        if self.is_leaf:
            return (self,)
        else:
            leaves = ()
            for child in self.children:
                leaves += child.leaves
            return leaves
    
    def show(self, max_depth=None):
        if max_depth is None:
            print_text = RenderTree(self)
            print(print_text)
        elif isinstance(max_depth, int):
            print_text = ''
            for pre, _, node in RenderTree(self):
                if (node.depth - self.depth) <= max_depth:
                    print_text += '{:}{:}\n'.format(pre, node)
            print(print_text)
        else:
            raise TypeError('max_depth must be an int or None (whole tree).')
    
    @property
    def game(self):
        return self._game
    
    @property
    def winner(self):
        return self._game.winner
    
    @staticmethod
    def get_unique_coords(game):
        available_coords = game.gameboard.available_coords
        unique_coords = []
        for coord in available_coords:
            duplicated = False
            m, n = game.gameboard.shape
            if game.gameboard.is_reflectional0:
                if (m - 1 - coord[0], coord[1]) in unique_coords:
                    duplicated = True
            if game.gameboard.is_reflectional1:
                if (coord[0], n - 1 - coord[1]) in unique_coords:
                    duplicated = True
            if game.gameboard.is_rotational180:
                if (m - 1 - coord[0], n - 1 - coord[1]) in unique_coords:
                    duplicated = True
            if game.gameboard.is_rotational90:
                if (coord[1], n - 1 - coord[0]) in unique_coords:
                    duplicated = True
                if (m - 1 - coord[1], coord[0]) in unique_coords:
                    duplicated = True
            if not duplicated:
                unique_coords.append(coord)
        return unique_coords
    
    @staticmethod
    def build_tree(node, depth, smart=False):
        if depth <= 0:
            pass
        elif node.game.is_ended:
            pass
        else:
            turn_player = node.game.turn_player
            if smart:
                available_coords = GameTree.get_unique_coords(node.game)
            else:
                available_coords = node.game.gameboard.available_coords
            win_node_found = False
            for coord in available_coords:
                game = node.game.copy()
                game.place_stone(*coord, turn_player)
                new_node = GameTree(
                    name=coord, game=game, parent=node
                )
                if game.winner == turn_player:
                    win_node_found = True
                if smart and win_node_found:
                    # No need to expand other siblings
                    # if winning state of the player was found.
                    pass
                else:
                    GameTree.build_tree(node=new_node, depth=depth - 1, smart=smart)
    
    def build(self, depth, smart=False):
        if self.is_leaf:
            self.build_tree(self, depth=depth, smart=smart)
        else:
            for node in self.leaves:
                self.build_tree(node, depth=depth, smart=smart)
    
    def clean_reward(self):
        self.reward = None
        for node in self.descendants:
            node.reward = None
