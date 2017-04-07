## BoardGame

Board games in Python with UI.

Games included in current version:
- [Tic-Tac-Toe](https://en.wikipedia.org/wiki/Tic-tac-toe)
- [Connect Four](https://en.wikipedia.org/wiki/Connect_Four)

### Prerequisites

System requirement:
- Python 3
  - [Anaconda (Recommened)](https://www.continuum.io/downloads)
  - [www.python.org](https://www.python.org/downloads/)

Required packages:
- [Numpy](http://www.numpy.org/)
- [anytree](http://anytree.readthedocs.io/en/latest/)
- [PyQt5](https://pypi.python.org/pypi/PyQt5/5.8.1)

### How to start a game

1. Download the repository [here](https://github.com/kitman0804/BoardGame/archive/master.zip) (and unzip it if needed).
2. Open your console.
3. Change your directory to downloaded folder.
4. Run `python -m play_ui game_code_below`.
    - Tic-Tac-Toe: `tictactoe`.
    - Connect Four: `connectfour`.
5. Have fun!

### AI/Algorithms

#### Tree search algorithms

- Minimax
  - [Wikipedia](https://en.wikipedia.org/wiki/Minimax)
- Minimax with Alpha-Beta Pruning
  - [Wikipedia](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
  - [Example with Animation](http://inst.eecs.berkeley.edu/~cs61b/fa14/ta-materials/apps/ab_tree_practice/)
- Minimax with Modified Alpha-Beta Pruning (No equal sign.)

#### Heuristic

- Simple score for Win/Draw/Lose/Game not ended.
- Simulation.

### What's next

- Add more games, e.g. Gomoku, Connect6.
- Make use of Machine Learning in the heuristic.
- Add Monte Carlo Tree Search.
- Improve searching speed.

### Credits

- Material design icons from [www.flaticon.com](http://www.flaticon.com/packs/material-design).
- Buddies who brought me to this area.
