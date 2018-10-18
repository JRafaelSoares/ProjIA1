from search import *
from copy import deepcopy
import time

b_basic = [["O", "O", "_"], ["_", "_", "O"], ["_", "_", "_"]]
b1 = [["X","X","O","O","O","O","O","X","X"],
 ["X","X","O","O","O","O","O","X","X"],
 ["O","O","O","O","O","O","O","O","O"],
 ["O","O","O","O","O","O","O","O","O"],
 ["O","O","O","O","_","O","O","O","O"],
 ["O","O","O","O","O","O","O","O","O"],
 ["O","O","O","O","O","O","O","O","O"],
 ["X","X","O","O","O","O","O","X","X"],
 ["X","X","O","O","O","O","O","X","X"]]

def c_peg():
    return "O"

def c_empty():
    return "_"

def c_blocked():
    return "X"

def is_empty(e):
    return e == c_empty()

def is_peg(e):
    return e == c_peg()

def is_blocked(e):
    return e == c_blocked()

# TAI pos
# Tuplo (l, c)
# Type pos
def make_pos(l, c):
    return (l, c)

def pos_l(pos):
    return pos[0]

def pos_c(pos):
    return pos[1]

# TAI move
# Lista [p_initial, p_final]
# Type Move
def make_move(i, f):
    return [i, f]

def move_initial(move):
    return move[0]

def move_final(move):
    return move[1]

def board_moves(b):
    
    moves = []
    
    n_line = len( b )
    
    n_colum = len( b[0] )
    
    for i in range( 0, n_line ):
        for j in range( 0, n_colum ):
            
            if (is_empty( b[i][j] ) ):
                
                if i != 0 and i != 1:
                    
                    if is_peg(b[i - 1][j]) and is_peg( b[i - 2][j] ):
                        moves.append( make_move( make_pos(i - 2, j), make_pos(i,j) ) )
                    
                if i != n_line - 1 and i != n_line - 2:
                    
                    if is_peg(b[i + 1][j]) and is_peg( b[i + 2][j] ):
                    
                        moves.append( make_move( make_pos(i + 2, j), make_pos(i,j) ) )
                
                if j != 0 and j != 1:
                            
                    if is_peg( b[i][j - 1] ) and is_peg( b[i][j - 2] ):
                        moves.append( make_move( make_pos(i, j - 2), make_pos(i,j) ) )  
                
                if j != n_colum - 1 and j != n_colum - 2:
                            
                    if is_peg(b[i][j + 1]) and is_peg( b[i][j + 2] ):
                            
                        moves.append( make_move( make_pos(i, j + 2), make_pos(i,j) ) ) 
    
    return moves

#print(board_moves(b1))
def board_perform_move(b, move):
    
    b_copy = deepcopy(b)
    
    b_copy[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty()
    
    b_copy[pos_l(move_final(move))][pos_c(move_final(move))] = c_peg()

    b_copy[(pos_l(move_initial(move))+pos_l(move_final(move)))//2][(pos_c(move_initial(move))+pos_c(move_final(move)))//2] = c_empty()

    return b_copy

class sol_state:

    def __init__(self, board):
        self.board = board
        self.cost = 0
    
    def __lt__(self, state):
        return True


class solitaire(Problem):

    # TAI content
    # Type Content

    def __init__(self, board):
        self.board = board
        self.initial = sol_state(board)


    def actions(self, state):
        return board_moves(state.board)

    def result(self, state, action):
        return sol_state(board_perform_move(state.board, action))

    def goal_test(self, state):

        n_line = len(state.board)

        n_colum = len(state.board[0])

        num_pegs = 0

        for i in range(0, n_line):
            for j in range(0, n_colum):
                if is_peg(state.board[i][j]):
                    num_pegs += 1

                if num_pegs > 1:
                    return False

        if num_pegs == 1:
            return True
        else:
            return False

    def path_cost(self, c, state1, action, state2):
        return c+1

    def h(self, node):
        return 0


#print(depth_first_tree_search(solitaire(b1)).solution())
#print( "Demorou ", time.time()-start_time, " medida?")
#print(depth_first_graph_search(solitaire(b1)).solution()) WORKS for basic problem
#print(best_first_graph_search(solitaire(b1), f=solitaire(b1).h).solution())
#print(astar_search(solitaire(b1)).solution()) WORKS for basic problem