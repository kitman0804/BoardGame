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
    
    def clean_reward(self):
        self.reward = None
        for node in self.descendants:
            node.reward = None
