import numpy as np
from anytree import Node, RenderTree


class GameTree(Node):
    def __init__(self, name, game_core, parent=None):
        super().__init__(name=name, parent=parent)
        self.game_core = game_core
        self.reward = None
        self.n_sim = 0
    
    def __repr__(self):
        print_text = '<Node ({:}, {:}, {:.2f})>'
        print_text = print_text.format(
            self.name,
            '_' if self.game_core.winner is None else self.game_core.winner,
            np.nan if self.reward is None else self.reward
        )
        return print_text
    
    @property
    def root_player(self):
        return self.root.game_core.current_player
    
    @property
    def player(self):
        return self.game_core.current_player
    
    @property
    def gameboard(self):
        return self.game_core.gameboard
    
    def reset_reward(self):
        self.reward = None
        for node in self.descendants:
            node.reward = None
    
    @property
    def size(self):
        return 1 + len(self.descendants)
    
    @property
    def leaves(self):
        leaves = ()
        if self.is_leaf:
            leaves += (self,)
        else:
            for child in self.children:
                leaves += child.leaves
        return leaves
    
    def cut_tree(self):
        self.parent = None
        return self
    
    def show(self, max_depth=np.inf):
        ref_depth = self.depth
        print_text = ''
        for pre, _, node in RenderTree(self):
            if (node.depth - ref_depth) <= max_depth:
                print_text += pre + node + '\n'
        print(print_text)
