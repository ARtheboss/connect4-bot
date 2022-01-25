BOARD_WIDTH = 7
BOARD_HEIGHT = 6

N_IN_A_ROW = 4



check_axis = [(0, 1), (1, 1), (-1, 1), (1, 0)]
def check_game_win(x, y, turn, g, tf=True):
    nlen = [0] * 4
    for axis in check_axis:
        right = 0
        i, j = x, y
        while i >= 0 and j >= 0 and i < 6 and j < 7 and g[i][j] == turn:
            i += axis[0]
            j += axis[1]
            right += 1
        left = 0
        i, j = x, y
        while i >= 0 and j >= 0 and i < 6 and j < 7 and g[i][j] == turn:
            i -= axis[0]
            j -= axis[1]
            left += 1
        if left + right - 1 >= 4 and tf:
            return True
        nlen[min(4, left + right - 1) - 1] += 1
    if tf:
        return False
    return nlen

def check_game_over(g):
    for i in range(7):
        if g[0][i] == 0: 
            return False
    return True

def render_grid(g):
    print("1 2 3 4 5 6 7")
    for row in g:
        srow = [str(i) if i != 0 else "." for i in row]
        print(" ".join(srow))
    print("\n")

def col_height(c, g):
    i = 5
    while i >= 0 and g[i][c] != 0:
        i -= 1
    return i
