import game 
import copy

import config


def heuristic(g, turn):
    ans = 0
    for i, row in enumerate(g):
        for j, v in enumerate(row):
            if v == 0:
                continue
            r = game.check_game_win(i, j, v, g, tf=False)
            for a, n in enumerate(r):
                ans += (1 - int(v != turn) * 2) * a * a * n
    #print(g, ans)
    return ans

def heuristic2(g, turn):
    ans = 0
    for i, row in enumerate(g):
        for j, v in enumerate(row):
            if v == 0:
                continue
            t = v
            factor = (1 - int(t != turn) * 2)
            for axis in game.check_axis:
                for dir in range(-1, 2, 2):
                    for c in range(config.CONNECT_NUM):
                        ni = i + axis[0] * c * dir
                        nj = j + axis[1] * c * dir
                        if ni >= 0 and nj >= 0 and ni < config.BOARD_HEIGHT and nj < config.BOARD_WIDTH:
                            if g[ni][nj] == t:
                                ans += factor * 2
                            elif g[ni][nj] == 0:
                                ans += factor
                        else:
                            break
    #print(ans, g)
    return ans

def heuristic3(g, turn):
    ans = 0
    for i, row in enumerate(g):
        for j, v in enumerate(row):
            if v == 0:
                continue
            t = v
            factor = (1 - int(t != turn) * 2)
            for axis in game.check_axis:
                for dir in range(-1, 2, 2):
                    for c in range(1, 4):
                        ni = i + axis[0] * c * dir
                        nj = j + axis[1] * c * dir
                        if ni >= 0 and nj >= 0 and ni < config.BOARD_HEIGHT and nj < config.BOARD_WIDTH:
                            if g[ni][nj] == t:
                                ans += factor * 2
                            elif g[ni][nj] == 0:
                                ans += factor
                            else:
                                ans -= factor
                        else:
                            break
    return ans

def relative_heuristic3(g, turn, i, j):
    ans = 0
    t = g[i][j]
    factor = (1 - int(t != turn) * 2)
    for axis in game.check_axis:
        for dir in range(-1, 2, 2):
            for c in range(1, 4):
                ni = i + axis[0] * c * dir
                nj = j + axis[1] * c * dir
                if ni >= 0 and nj >= 0 and ni < config.BOARD_HEIGHT and nj < config.BOARD_WIDTH:
                    if g[ni][nj] == t:
                        ans += factor * 3
                    elif g[ni][nj] == 0:
                        ans += factor
                    else:
                        ans += factor
                else:
                    break
    return ans

def heuristic4_axis_check(g, turn, i, j):
    ans = 0
    t = g[i][j]
    factor = (1 - int(t != turn) * 2)
    for axis in game.check_axis:
        for c in range(1, config.CONNECT_NUM):
            ni = i + axis[0] * c
            nj = j + axis[1] * c
            if ni >= 0 and nj >= 0 and ni < config.BOARD_HEIGHT and nj < config.BOARD_WIDTH:
                if g[ni][nj] == t:
                    ans += factor
                elif g[ni][nj] == 0:
                    ans += 0#factor
                else:
                    break
            else:
                break
        right = c
        for c in range(1, config.CONNECT_NUM):
            ni = i - axis[0] * c
            nj = j - axis[1] * c
            if ni >= 0 and nj >= 0 and ni < config.BOARD_HEIGHT and nj < config.BOARD_WIDTH:
                if g[ni][nj] == t:
                    ans += factor
                elif g[ni][nj] == 0:
                    ans += 0#factor
                else:
                    break
            else:
                break
        left = c
        if left + right >= config.CONNECT_NUM:
            ans += factor * (left + right)
    return ans

def heuristic4(g, turn):
    ans = 0
    for i, row in enumerate(g):
        for j, v in enumerate(row):
            if v == 0:
                continue
            ans += heuristic4_axis_check(g, turn, i, j)
    return ans

def relative_heuristic4(g, turn, i, j):
    ans = heuristic4_axis_check(g, turn, i, j)
    lt = g[i][j]
    g[i][j] = 0
    for axis in game.check_axis:
        for dir in range(-1, 2, 2):
            for c in range(1, config.CONNECT_NUM):
                ni = i + axis[0] * c * dir
                nj = j + axis[1] * c * dir
                if ni >= 0 and nj >= 0 and ni < config.BOARD_HEIGHT and nj < config.BOARD_WIDTH:
                    if g[ni][nj] == 0:
                        continue
                    ans -= heuristic4_axis_check(g, turn, ni, nj)
                else:
                    break
    g[i][j] = lt
    for axis in game.check_axis:
        for dir in range(-1, 2, 2):
            for c in range(1, config.CONNECT_NUM):
                ni = i + axis[0] * c * dir
                nj = j + axis[1] * c * dir
                if ni >= 0 and nj >= 0  and ni < config.BOARD_HEIGHT and nj < config.BOARD_WIDTH:
                    if g[ni][nj] == 0:
                        continue
                    ans += heuristic4_axis_check(g, turn, ni, nj)
                else:
                    break
    return ans

def relative_heuristic4v2(g, turn, i, j):
    ans = 0
    for axis in game.check_axis:
        for dir in range(-1, 2, 2):
            for c in range(1, config.CONNECT_NUM):
                ni = i + axis[0] * c * dir
                nj = j + axis[1] * c * dir
                if ni >= 0 and nj >= 0 and ni < config.BOARD_HEIGHT and nj < config.BOARD_WIDTH:
                    if g[ni][nj] == 0:
                        continue
                    ans -= heuristic4_axis_check(g, turn, ni, nj)
                else:
                    break
    return ans

# 4, 4, 4, 3, 2, 3, 2, 3, 2, 2, 3, 1, 7, 2, 5
# 4 5 6 3 2 1 7 
# 4 3 5 6 5 

heuristic_versions = [heuristic, heuristic2, heuristic3, heuristic4]
relative_heuristic_versions = [relative_heuristic3, relative_heuristic3, relative_heuristic3, relative_heuristic4]

def generate_move(g, turn, hv=3, depth=4):
    bs = -1e9
    bc = 0
    current_h = heuristic_versions[hv](g, turn)
    for col in range(config.BOARD_WIDTH):
        if g[0][col] != 0:
            continue
        score = min_max(g, col, turn, turn, -1e9, 1e9, depth, current_h, hv=hv)
        score[0] -= len(score[1])
        if score[0] > bs:
            bs = score[0]
            bc = col
        
        if config.BOT_STATS:
            print(col + 1, score)
            
    return bc

def min_max(g, last_move, turn, my_turn, alpha, beta, depth, last_h, hv=3):

    g = copy.deepcopy(g)
    ch = game.col_height(last_move, g)
    g[ch][last_move] = turn

    my_h = last_h + relative_heuristic_versions[hv](g, my_turn, ch, last_move)

    if game.check_game_over(g):
        return [0, [0]]

    if game.check_game_win(ch, last_move, turn, g):
        if turn == my_turn:
            return [1000, [1000]]
        else:
            return [-1000, [-1000]]

    if depth == 0:
        return [my_h, [my_h]]

    if turn == 1:
        turn = 2
    else:
        turn = 1

    if turn == my_turn:
        best = [-1e9, []]
    else:
        best = [1e9, []]
    for i in range(config.BOARD_WIDTH):
        if g[0][i] != 0:
            continue
        mmres = min_max(g, i, turn, my_turn, alpha, beta, depth - 1, my_h, hv=hv)
        if turn == my_turn:
            if best[0] - len(best[1]) < mmres[0] - len(mmres[1]):
                best = mmres
            alpha = max(best[0], alpha)
        else:
            if best[0] - len(best[1]) > mmres[0] - len(mmres[1]):
                best = mmres
            beta = min(beta, best[0])
        if beta <= alpha:
            #continue
            break
    best[1].append((my_h, last_move + 1))
    return best


if __name__ == '__main__':
    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 2, 1, 2, 0, 0, 2],
        [1, 1, 2, 2, 1, 1, 2],
    ]
    lh = heuristic4(grid, 2)
    print(lh)
    grid[3][3] = 2
    print(lh + relative_heuristic4(grid, 2, 3, 3), heuristic4(grid, 2))