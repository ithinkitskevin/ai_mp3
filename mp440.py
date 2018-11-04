'''
Compute the value brought by a given move by placing a new token for player
at (row, column). The value is the number of opponent pieces getting flipped
by the move. 

A move is valid if for the player, the location specified by (row, column) is
(1) empty and (2) will cause some pieces from the other player to flip. The
return value for the function should be the number of pieces hat will be moved.
If the move is not valid, then the value 0 (zero) should be returned. Note
here that row and column both start with index 0. 
'''
from copy import deepcopy

def isValid(row, state_y_len, col, state_x_len):
    return row >= 0 and row < state_y_len and col >= 0 and col < state_x_len

def get_move_value(state, player, row, column):
    flipped = 0
    # Your implementation goes here 
    state_y_len = mul = len(state)
    state_x_len = len(state[0])

    poss_dir_list = ((-1,0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1,1), (1,0), (1,-1))
    
    for poss_dir in poss_dir_list:
        # for a direction, check until the very end
        loc_flip = 0
        own_piece_in_way = False

        for ranged in range(1, mul+1):
            new_dir_row = poss_dir[0] * ranged
            new_dir_col = poss_dir[1] * ranged

            app_row = new_dir_row + row
            app_col = new_dir_col + column

            if isValid(app_row, state_y_len, app_col, state_x_len):
                if player == 'B':
                    # Player 1, so look for all whites
                    if state[app_row][app_col] == 'W':
                        loc_flip += 1
                    if state[app_row][app_col] == 'B':
                        own_piece_in_way = True
                        break
                elif player == 'W':
                    # Player 2, so look for all blacks
                    if state[app_row][app_col] == 'B':
                        loc_flip += 1
                    if state[app_row][app_col] == 'W':
                        own_piece_in_way = True
                        break
            else:
                break

        if own_piece_in_way:
            flipped += loc_flip

    return flipped

'''
Execute a move that updates the state. A new state should be crated. The move
must be valid. Note that the new state should be a clone of the old state and
in particular, should not share memory with the old state. 
'''
def execute_move(state, player, row, column):
    new_state = None
    # Your implementation goes here
    new_state = list()
    for r in state:
        tmp_col = list()
        for c in r:
            tmp_col.append(c)
        new_state.append(tmp_col)
    new_state[row][column] = player

    state_y_len = mul = len(state)
    state_x_len = len(state[0])

    poss_dir_list = ((-1,0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1,1), (1,0), (1,-1))

    for poss_dir in poss_dir_list:
        # for a direction, check until the very end
        loc_flip = 0
        own_piece_in_way = False
        loc_move_list = list()

        for ranged in range(1, mul+1):
            new_dir_row = poss_dir[0] * ranged
            new_dir_col = poss_dir[1] * ranged

            app_row = new_dir_row + row
            app_col = new_dir_col + column

            if isValid(app_row, state_y_len, app_col, state_x_len):
                if player == 'B':
                    # Player 1, so look for all whites
                    if state[app_row][app_col] == 'W':
                        loc_move_list.append((app_row, app_col))
                    if state[app_row][app_col] == 'B':
                        own_piece_in_way = True
                        break
                elif player == 'W':
                    # Player 2, so look for all blacks
                    if state[app_row][app_col] == 'B':
                        loc_move_list.append((app_row, app_col))
                    if state[app_row][app_col] == 'W':
                        own_piece_in_way = True
                        break
            else:
                break

        if own_piece_in_way:
            for loc_move in loc_move_list:
                new_state[loc_move[0]][loc_move[1]] = player

    return new_state

'''
A method for counting the pieces owned by the two players for a given state. The
return value should be two tuple in the format of (blackpeices, white pieces), e.g.,

    return (4, 3)

'''
def count_pieces(state):
    blackpieces = 0
    whitepieces = 0
    # Your implementation goes here 
    for row in state:
        for col in row:
            if col == 'W':
                whitepieces += 1
            elif col == 'B':
                blackpieces += 1

    return (blackpieces, whitepieces)

'''
Check whether a state is a terminal state. 
'''
def is_terminal_state(state, state_list = None):
    terminal = True
    # Your implementation goes here 
    curr_pieces = count_pieces(state)
    for row_ind, row in enumerate(state):
        for col_ind, col in enumerate(row):
            if col == ' ':
                if (get_move_value(state, 'B', row_ind, col_ind) == 0) and (get_move_value(state, 'W', row_ind, col_ind) == 0):
                    terminal = True
                else:
                    return False
    return terminal

'''
The minimax algorithm. Your implementation should return the best value for the
given state and player, as well as the next immediate move to take for the player. 
''' 
def utility(state, player):
    tmp_pieces = count_pieces(state)
    return tmp_pieces[0] if player == 'B' else tmp_pieces[1]

def getChildren(state, player):
    children_list = list()
    for row_ind, row_data in enumerate(state):
        for col_ind, col in enumerate(row_data):
            if col != ' ':
                continue
            tmp_state = deepcopy(state)
            tmp_state = execute_move(tmp_state, player, row_ind, col_ind)
            children_list.append((tmp_state, row_ind, col_ind))
    return children_list 

def minimax(state, player):
    value = 0
    row = -1
    column = -1

    di = {}
    # Your implementation goes here     
    def maxValue(i, state):
        if i in di:
            d_tmp = di[i]
            d_tmp.append(state)
            di[i] = d_tmp
        else:
            di[i] = [state]
        if is_terminal_state(state):
            return utility(state, player)
        v = -9999
        for a in getChildren(state, player):
            # print(a[0], 'max')
            i+=1
            v = max(v, minValue(i, a[0]))
        return v

    def minValue(i, state):
        if i in di:
            d_tmp = di[i]
            d_tmp.append(state)
            di[i] = d_tmp
        else:
            di[i] = [state]
        if is_terminal_state(state):
            return utility(state, player)
        v = 9999
        for a in getChildren(state, player):
            # print(a[0], 'min')
            i+=1
            v = min(v, maxValue(i, a[0]))
        return v   

    # I KNOW I GOT THE VALUE WRONG HERE BTW
    # IT IS SUPPOSED TO BE get_move_value
    value = -1
    for state in getChildren(state, player):
        state_val = minValue(1, state[0])
        if 0 in di:
            d_tmp = di[0]
            d_tmp.append(state)
            di[0] = d_tmp
        else:
            di[0] = [state]
        if value < state_val:
            value = state_val
            row = state[1]
            column = state[2]

    print(di.keys())
    print(1)
    for i in di[1]:
        print(i)
    print(2)
    for i in di[2]:
        print(i)
    print(3)
    for i in di[3]:
        print(i)
    return value, row, column

'''
This method should call the minimax algorithm to compute an optimal move sequence
that leads to an end game. 
'''
def full_minimax(state, player):
    value = 0
    move_sequence = []
    # Your implementation goes here 
    while True:
        print(state)
        if is_terminal_state(state):
            break
        vrc = minimax(state, player)
        state = execute_move(state,player,vrc[1],vrc[2])
        player = 'B' if player == 'W' else 'W'
        value += vrc[0]
        move_sequence.append((vrc[1],vrc[2]))
    return (value, move_sequence)


'''
The minimax algorithm with alpha-beta pruning. Your implementation should return the
best value for the given state and player, as well as the next immediate move to take
for the player. 
'''
def minimax_ab(state, player, alpha = -10000000, beta = 10000000):
    value = 0
    row = -1
    column = -1
    # Your implementation goes here 
    return (value, row, column)

'''
This method should call the minimax_ab algorithm to compute an optimal move sequence
that leads to an end game, using alpha-beta pruning.
'''
def full_minimax_ab(state, player):
    value = 0
    move_sequence = []
    # Your implementation goes here 
    return (value, move_sequence)


