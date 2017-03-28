import numpy as np
import anytree
import uuid
from ..BoardGame import BoardGame


class GameTreeNode(anytree.Node):
    def __init__(self, name, node_id=None, parent=None,
                 game=None, rewards=(1, 0, -1, 0), discount=0.95):
        super().__init__(name=name, parent=parent)
        self._node_id = uuid.uuid4() if node_id is None else node_id
        self._game = game
        self._rewards = rewards
        self._discount = discount
        self._children_simulated = False
    
    def __repr__(self):
        print_text = 'Name: {0:}'
        if self.is_leaf:
            print_text += ', Winner: {1:}'
        print_text += ', Reward: {2:.2f}'
        print_text = '<State ({:}) - id: {{3:}}>'.format(print_text)
        print_text = print_text.format(
            self._name,
            self.winner if self.winner is not None else '_',
            self.reward,
            self._node_id,
        )
        return print_text
        
    
    @property
    def game(self):
        return self._game
    
    @property
    def gameboard(self):
        return self._game.gameboard
    
    @property
    def winner(self):
        return self._game.winner
    
    @property
    def game_ended(self):
        return self._game.is_ended
    
    @property
    def all_nodes(self):
        return (self,) + self.descendants
    
    @property
    def leaves(self):
        return [n for n in self.all_nodes if n.is_leaf]
    
    @property
    def reward(self):
        if self.is_leaf:
            discount = self._discount**(max(self.depth - 1, 0) // 2)
            if self.winner is None:
                r = self._rewards[3]
            elif self.winner == -1:
                r = self._rewards[1]
            elif self.winner == self.root.game.turn_player:
                r = self._rewards[0]
            else:
                r = self._rewards[2]
            return r * discount
        elif self._children_simulated:
            r = [x.reward for x in self.children]
            return sum(r)/len(r)
        else:
            r = [x.reward for x in self.children]
            return max(r) if self.depth % 2 == 0 else min(r)
    
    def show(self):
        print(anytree.RenderTree(self))
    
    def expand(self):
        if self.game_ended:
            pass
        else:
            for move in self.gameboard.available_moves:
                game = self._game.copy()
                game.move(*move, player=game.turn_player)
                child = type(self)(
                    name=move, node_id=len(self.root.descendants), parent=self,
                    game=game, rewards=self._rewards, discount=self._discount
                )
    
    def pruned_expand(self):
        if self.game_ended:
            pass
        else:
            for move in self.gameboard.available_moves:
                game = self._game.copy()
                game.move(*move, player=game.turn_player)
                child = type(self)(
                    name=move, node_id=len(self.root.descendants), parent=self,
                    game=game, rewards=self._rewards, discount=self._discount
                )
                # Similar concept of alpha-beta pruning
                if game.turn % 2 == game.winner:
                    break
    
    def simulate(self, r=10):
        if self.game_ended:
            pass
        else:
            self._children_simulated = True
            for i in range(r):
                game = self._game.copy()
                while game.winner is None:
                    available_moves = game.gameboard.available_moves
                    move = available_moves[np.random.choice(len(available_moves))]
                    game.move(*move, player=game.turn_player)
                child = type(self)(
                    name='{:}_{:}'.format(self._node_id, i),
                    node_id=len(self.root.descendants), parent=self,
                    game=game, rewards=self._rewards, discount=self._discount
                )


class GameTree(object):
    def __init__(self, game, rewards=(1, 0, -1, 0), discount=0.95):
        if not isinstance(game, BoardGame):
            raise('game must be a BoardGame object.')
        self._root = GameTreeNode(
            name='root', node_id=0, parent=None,
            game=game, rewards=rewards, discount=discount
        )
        self._level = [[self._root]]
    
    @property
    def root(self):
        return self._root
    
    @property
    def level(self):
        return self._level
    
    def expand(self, depth=2):
        for _ in range(depth):
            new_level = list()
            for node in self._level[-1]:
                node.expand()
                new_level.extend(node.children)
            self._level.append(new_level)
    
    def expand_simulate(self, depth=2, r=10):
        self.expand(depth=depth)
        new_level = list()
        for node in self._level[-1]:
            node.simulate(r=r)
            new_level.extend(node.children)
        self._level.append(new_level)
    
    def show(self):
        self._root.show()
