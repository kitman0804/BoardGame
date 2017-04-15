import numpy as np
from .GameTree import GameTree


def minimax(node, depth, hfunc, use_symmetry=False):
    root_player = node.root_player
    # Current state
    current_game = node.game
    current_gameboard = current_game.gameboard
    current_player = current_game.current_player
    if use_symmetry:
        available_coords = current_gameboard.eqivalent_coords_dict.keys()
    else:
        available_coords = current_gameboard.available_coords
    # Search
    if depth == 0 or current_game.is_ended:
        node.reward = hfunc(game=current_game, player=root_player)
    elif current_player == root_player:
        best_value = -np.inf
        for coord in available_coords:
            game = current_game.copy()
            game.place_stone(*coord, current_player)
            child_node = GameTree(name=coord, game=game, parent=node)
            minimax(
                node=child_node,
                depth=depth-1,
                hfunc=hfunc,
                use_symmetry=use_symmetry
            )
            best_value = max(best_value, child_node.reward)
        node.reward = best_value
    else:
        best_value = np.inf
        for coord in available_coords:
            game = current_game.copy()
            game.place_stone(*coord, current_player)
            child_node = GameTree(name=coord, game=game, parent=node)
            minimax(
                node=child_node,
                depth=depth-1,
                hfunc=hfunc,
                use_symmetry=use_symmetry
            )
            best_value = min(best_value, child_node.reward)
        node.reward = best_value


def alpha_beta(node, depth, hfunc,
               alpha=-np.inf, beta=np.inf, equal_sign=True, use_symmetry=False):
    root_player = node.root.game.turn_player
    # Current state
    current_game = node.game
    current_gameboard = current_game.gameboard
    current_player = current_game.current_player
    if use_symmetry:
        available_coords = current_gameboard.eqivalent_coords_dict.keys()
    else:
        available_coords = current_gameboard.available_coords
    # Search
    if depth == 0 or current_game.is_ended:
        node.reward = hfunc(game=current_game, player=root_player)
    elif current_player == root_player:
        best_value = -np.inf
        for coord in available_coords:
            game = current_game.copy()
            game.place_stone(*coord, current_player)
            child_node = GameTree(name=coord, game=game, parent=node)
            alpha_beta(
                node=child_node,
                depth=depth-1,
                hfunc=hfunc,
                alpha=alpha,
                beta=beta,
                equal_sign=equal_sign,
                use_symmetry=use_symmetry
            )
            best_value = max(best_value, child_node.reward)
            alpha = max(alpha, best_value)
            if beta < alpha:
                break
            if equal_sign and beta == alpha:
                break
        node.reward = best_value
    else:
        best_value = np.inf
        for coord in available_coords:
            game = current_game.copy()
            game.place_stone(*coord, current_player)
            child_node = GameTree(name=coord, game=game, parent=node)
            alpha_beta(
                node=child_node,
                depth=depth-1,
                hfunc=hfunc,
                alpha=alpha,
                beta=beta,
                equal_sign=equal_sign,
                use_symmetry=use_symmetry
            )
            best_value = min(best_value, child_node.reward)
            beta = min(beta, best_value)
            if beta < alpha:
                break
            if equal_sign and beta == alpha:
                break
        node.reward = best_value


def modified_minimax(node, depth, hfunc, use_symmetry=False):
    root_player = node.root.game.turn_player
    # Current state
    current_game = node.game
    current_gameboard = current_game.gameboard
    current_player = current_game.current_player
    if use_symmetry:
        available_coords = current_gameboard.eqivalent_coords_dict.keys()
    else:
        available_coords = current_gameboard.available_coords
    # Search
    if depth == 0 or current_game.is_ended:
        node.reward = hfunc(game=current_game, player=root_player)
    else:
        # Create child nodes and check winner
        win_state_found = False
        for coord in available_coords:
            game = current_game.copy()
            game.place_stone(*coord, current_player)
            child_node = GameTree(name=coord, game=game, parent=node)
            if child_node.game.winner == current_player:
                win_state_found = True
                # No need to search further if current player win
                depth = 1
        # Apply minimax
        if current_player == root_player:
            best_value = -np.inf
            for child_node in node.children:
                modified_minimax(
                    node=child_node,
                    depth=depth-1,
                    hfunc=hfunc,
                    use_symmetry=use_symmetry
                )
                best_value = max(best_value, child_node.reward)
            node.reward = best_value
        else:
            best_value = np.inf
            for child_node in node.children:
                modified_minimax(
                    node=child_node,
                    depth=depth-1,
                    hfunc=hfunc,
                    use_symmetry=use_symmetry
                )
                best_value = min(best_value, child_node.reward)
            node.reward = best_value


def modified_alpha_beta(node, depth, hfunc,
                        alpha=-np.inf, beta=np.inf, use_symmetry=False):
    root_player = node.root.game.turn_player
    # Current state
    current_game = node.game
    current_gameboard = current_game.gameboard
    current_player = current_game.current_player
    if use_symmetry:
        available_coords = current_gameboard.eqivalent_coords_dict.keys()
    else:
        available_coords = current_gameboard.available_coords
    # Search
    if depth == 0 or current_game.is_ended:
        node.reward = hfunc(game=current_game, player=root_player)
    else:
        # Create child nodes and check winner
        win_state_found = False
        for coord in available_coords:
            game = current_game.copy()
            game.place_stone(*coord, current_player)
            child_node = GameTree(name=coord, game=game, parent=node)
            if child_node.game.winner == current_player:
                win_state_found = True
                # No need to search further if current player win
                depth = 1
        if current_player == root_player:
            best_value = -np.inf
            for child_node in node.children:
                modified_alpha_beta(
                    node=child_node,
                    depth=depth-1,
                    hfunc=hfunc,
                    alpha=alpha,
                    beta=beta,
                    use_symmetry=use_symmetry
                )
                best_value = max(best_value, child_node.reward)
                alpha = max(alpha, best_value)
                if beta < alpha:
                    break
            node.reward = best_value
        else:
            best_value = np.inf
            for child_node in node.children:
                modified_alpha_beta(
                    node=child_node,
                    depth=depth-1,
                    hfunc=hfunc,
                    alpha=alpha,
                    beta=beta,
                    use_symmetry=use_symmetry
                )
                best_value = min(best_value, child_node.reward)
                beta = min(beta, best_value)
                if beta < alpha:
                    break
            node.reward = best_value
