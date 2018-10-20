from search import *
from copy import deepcopy
import time

b_basic = [["O", "O", "_"],
           ["_", "_", "O"],
           ["_", "_", "_"]]
b1 = [["X","X","O","O","O","O","O","X","X"],
 ["X","X","O","O","O","O","O","X","X"],
 ["O","O","O","O","O","O","O","O","O"],
 ["O","O","O","O","O","O","O","O","O"],
 ["O","O","O","O","_","O","O","O","O"],
 ["O","O","O","O","O","O","O","O","O"],
 ["O","O","O","O","O","O","O","O","O"],
 ["X","X","O","O","O","O","O","X","X"],
 ["X","X","O","O","O","O","O","X","X"]]

b_30 = [["O","O","O","X","X"],
        ["O","O","O","O","O"],
        ["O","_","O","_","O"],
        ["O","O","O","O","O"]]

b2 = [['X','O','O','O','X'],
      ['O','O','O','O','O'],
      ['O','O','_','O','O'],
      ['O','O','O','O','O'],
      ['X','O','O','O','X']]

b3 = [["O","O","O","X"],
 ["O","O","O","O"],
 ["O","_","O","O"],
 ["O","O","O","O"]]

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

    n_column = len( b[0] )
    
    for i in range( 0, n_line ):
        for j in range( 0, n_column ):
            
            if is_empty( b[i][j] ) :
                
                if i != 0 and i != 1:
                    
                    if is_peg(b[i - 1][j]) and is_peg( b[i - 2][j] ):
                        moves.append( make_move( make_pos(i - 2, j), make_pos(i,j) ) )
                    
                if i != n_line - 1 and i != n_line - 2:
                    
                    if is_peg(b[i + 1][j]) and is_peg( b[i + 2][j] ):
                    
                        moves.append( make_move( make_pos(i + 2, j), make_pos(i,j) ) )
                
                if j != 0 and j != 1:
                            
                    if is_peg( b[i][j - 1] ) and is_peg( b[i][j - 2] ):
                        moves.append( make_move( make_pos(i, j - 2), make_pos(i,j) ) )  
                
                if j != n_column - 1 and j != n_column - 2:
                            
                    if is_peg(b[i][j + 1]) and is_peg( b[i][j + 2] ):
                            
                        moves.append( make_move( make_pos(i, j + 2), make_pos(i,j) ) ) 
    
    return moves


#CORNERS
def heuristic_corners(b):

    n_line = len(b)

    n_column = len(b[0])

    num_corners = 0
    """
    for i in range(2):
        for j in range(2):
            line = 0 if i == 0 else n_line-1
            column = 0 if j == 0 else n_column-1
            if is_peg(b[line][column]):
                num_corners += 1
    """

    for i in range(0, n_line):
        for j in range(0, n_column):
            dead_ends = 0

            if is_peg(b[i][j]):

                dead_ends += 1 if i == 0 or i == n_line-1 else 0
                dead_ends += 1 if j == 0 or j == n_column-1 else 0

                if i != 0:

                    if is_blocked(b[i - 1][j]):
                        dead_ends += 1

                if i != n_line - 1:

                    if is_blocked(b[i + 1][j]):
                        dead_ends += 1

                if j != 0:

                    if is_blocked(b[i][j - 1]):
                        dead_ends += 1

                if j != n_column - 1:

                    if is_blocked(b[i][j + 1]):
                        dead_ends += 1

            if dead_ends >= 2:
                num_corners += 1

    return num_corners
""""
Wrong Corners
def heuristic_corners(b):

    n_line = len(b)

    n_column = len(b[0])

    num_corners = 0

    for i in range(2):
        for j in range(2):
            line = 0 if i == 0 else n_line-1
            column = 0 if j == 0 else n_column-1
            if is_peg(b[line][column]):
                num_corners += 1

    for i in range(0, n_line):
        for j in range(0, n_column):
            dead_ends = 0

            if not(is_blocked(b[i][j])):

                if i != 0:

                    if is_blocked(b[i - 1][j]):
                        dead_ends += 1

                if i != n_line - 1:

                    if is_blocked(b[i + 1][j]):
                        dead_ends += 1

                if j != 0:

                    if is_blocked(b[i][j - 1]):
                        dead_ends += 1

                if j != n_column - 1:

                    if is_blocked(b[i][j + 1]):
                        dead_ends += 1

            if dead_ends >= 2:
                num_corners += 1

    return num_corners
"""

def get_group(groups, pos):
    for x in range(0,len(groups)):
        if pos in groups[x]:
            return groups[x]

    return None

def find_groups(b):

    groups = []

    n_line = len(b)

    n_column = len(b[0])

    for i in range(0, n_line):

        for j in range(0, n_column):
            if is_peg(b[i][j]):

                if i == 0:
                    if j == 0:
                        groups.append([make_pos(i,j)])

                    else:
                        g = get_group(groups, make_pos(i, j-1))

                        if g != None:
                            g.append(make_pos(i,j))

                        else:
                            groups.append([make_pos(i,j)])

                elif j == 0 and i != 0:
                    g = get_group(groups, make_pos(i-1, j))

                    if g != None:
                        g.append(make_pos(i,j))

                    else:
                        groups.append([make_pos(i,j)])

                else:
                    g1 = get_group(groups, make_pos(i-1,j))
                    g2 = get_group(groups, make_pos(i, j-1))

                    if g1 == g2 and g1 != None:
                        g1.append(make_pos(i,j))

                    elif g1 == None and g2 == None:
                        groups.append([make_pos(i,j)])

                    elif g1 != g2 and g1 != None and g2 != None:
                        g1.append(make_pos(i,j))
                        g1 += g2
                        groups.remove(g2)

                    elif g1 != None and g2 == None:
                        g1.append(make_pos(i,j))

                    else:
                        g2.append(make_pos(i,j))

    return len(groups)

def board_perform_move(b, move):
    
    b_copy = deepcopy(b)
    
    b_copy[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty()
    
    b_copy[pos_l(move_final(move))][pos_c(move_final(move))] = c_peg()

    b_copy[(pos_l(move_initial(move))+pos_l(move_final(move)))//2][(pos_c(move_initial(move))+pos_c(move_final(move)))//2] = c_empty()

    return b_copy

def number_of_pegs(board):
    n_line = len(board)

    n_column = len(board[0])

    peg_number = 0

    for i in range(0, n_line):
        for j in range(0, n_column):
            if is_peg(board[i][j]):
                peg_number += 1

    return peg_number

class sol_state:

    def __init__(self, board, pegnum=None):
        __slots__ = 'board'
        self.board = board

        if pegnum != None:
            self.peg_num = pegnum

        else:
            self.peg_num = number_of_pegs(board)
    
    def __lt__(self, state):
        return self.peg_num > state.peg_num

    def getPegNum(self):
        return self.peg_num


class solitaire(Problem):

    # TAI content
    # Type Content

    def __init__(self, board):
        super().__init__(self, sol_state(board))
        self.board = board

    def actions(self, state):
        return board_moves(state.board)

    def result(self, state, action):
        #print(state.getPegNum())
        return sol_state(board_perform_move(state.board, action))

    def goal_test(self, state):

        n_line = len(state.board)

        n_column = len(state.board[0])

        num_pegs = 0

        for i in range(0, n_line):
            for j in range(0, n_column):
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
        return heuristic_corners(node.state.board)

def greedy_search(problem, h=None):
    """f(n) = h(n)"""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)

start = time.time()
#print(heuristic_corners(b3, number_corner(b3)) +find_groups(b3))
#print(depth_first_tree_search(solitaire(b1)).solution())
#print( "Demorou ", time.time()-start_time, " medida?")


#print(depth_first_graph_search(solitaire(b_30)).solution())
#print(best_first_graph_search(solitaire(b_30), f=solitaire(b_30).h).solution())

#print(best_first_graph_search(solitaire(b2), f=solitaire(b2).h))
#print(astar_search(solitaire(b_30),solitaire(b_30).h).solution())


print(greedy_search(solitaire(b_30), h=solitaire(b_30).h).solution())
end = time.time()

print(end-start)