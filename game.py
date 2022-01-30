import config

check_axis = [(0, 1), (1, 1), (-1, 1), (1, 0)]
def check_game_win(x, y, turn, g, tf=True):
    nlen = [0] * config.CONNECT_NUM
    for axis in check_axis:
        right = 0
        i, j = x, y
        while i >= 0 and j >= 0 and i < config.BOARD_HEIGHT and j < config.BOARD_WIDTH and g[i][j] == turn:
            i += axis[0]
            j += axis[1]
            right += 1
        left = 0
        i, j = x, y
        while i >= 0 and j >= 0 and i < config.BOARD_HEIGHT and j < config.BOARD_WIDTH and g[i][j] == turn:
            i -= axis[0]
            j -= axis[1]
            left += 1
        if left + right - 1 >= config.CONNECT_NUM and tf:
            return True
        nlen[min(config.CONNECT_NUM, left + right - 1) - 1] += 1
    if tf:
        return False
    return nlen

def check_game_over(g):
    for i in range(config.BOARD_WIDTH):
        if g[0][i] == 0: 
            return False
    return True

def render_grid(g):
    print(" ".join([str(i) for i in range(1, config.BOARD_WIDTH + 1)]))
    for row in g:
        srow = [str(i) if i != 0 else "." for i in row]
        print(" ".join(srow))
    print("\n")

def col_height(c, g):
    i = config.BOARD_HEIGHT - 1
    while i >= 0 and g[i][c] != 0:
        i -= 1
    return i
