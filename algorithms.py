import copy  # Import copy for deep copying game states

def minimax(game, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or game.game_over:  #depth limit or game over
        return game.pits[13] - game.pits[6], None  #evaluate the board

    best_move = None
    if maximizing_player:  #maximize player 2's score
        max_eval = float('-inf')
        for i in range(7, 13):  #iterate over player 2's pits
            if game.pits[i] > 0:  #skip empty pits
                board_copy = copy.deepcopy(game)  #make a copy of the game
                board_copy.make_move(i)  #simulate the move
                eval, _ = minimax(board_copy, depth - 1, False, alpha, beta)
                if eval > max_eval:  #update the best evaluation
                    max_eval = eval
                    best_move = i  #track the best move
                alpha = max(alpha, eval)  #update alpha
                if beta <= alpha:  #alpha-beta pruning
                    break
        return max_eval, best_move
    else:  #minimize player 1's score
        min_eval = float('inf')
        for i in range(6):  #iterate over player 1's pits
            if game.pits[i] > 0:  #skip empty pits
                board_copy = copy.deepcopy(game)  #make a copy of the game
                board_copy.make_move(i)  #simulate the move
                eval, _ = minimax(board_copy, depth - 1, True, alpha, beta)  #recursive call
                if eval < min_eval:  #update the best evaluation
                    min_eval = eval
                    best_move = i  #track the best move
                beta = min(beta, eval)  #update beta
                if beta <= alpha:  #alpha-beta pruning
                    break
        return min_eval, best_move

def greedy_move(game):
    best_move = None
    max_stones = -1
    if game.current_player == 1:  #player 2's turn
        for i in range(7, 13):  #iterate over player 2's pits
            if game.pits[i] > max_stones:  #find the pit with the most stones
                max_stones = game.pits[i]
                best_move = i
    else:  #player 1's turn
        for i in range(6):  #iterate over player 1's pits
            if game.pits[i] > max_stones:  #find the pit with the most stones
                max_stones = game.pits[i]
                best_move = i
    return best_move  #return the best move
