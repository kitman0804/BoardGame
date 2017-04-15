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
    def root_player(self):
        return self.root.game.current_player
    
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
    
    def show(self, max_depth=np.inf):
        ref = self.depth
        print_text = ''
        for pre, _, node in RenderTree(self):
            if (node.depth - ref) <= max_depth:
                print_text += pre + node + '\n'
        print(print_text)
    
    @property
    def game(self):
        return self._game
    
    def clean_reward(self):
        self.reward = None
        for node in self.descendants:
            node.reward = None
