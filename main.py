import game
import bot

import time

import config

grid = [[0 for _ in range(config.BOARD_WIDTH)] for _ in range(config.BOARD_HEIGHT)]

turn = 2
last_spot = (0, 0)
nmoves = 0
while not game.check_game_over(grid) and not game.check_game_win(last_spot[0], last_spot[1], turn, grid):
    nmoves += 1
    if turn == 1:
        turn = 2
    else:
        turn = 1
    game.render_grid(grid)
    ch, col = -1, -1
    while ch < 0 or col < 0 or col >= config.BOARD_WIDTH:
        if (turn == 1 and config.PLAYER_STARTS) or (turn == 2 and not config.PLAYER_STARTS):
            #col = bot.generate_move(grid, turn, hv=3, depth=5)
            col = int(input(f'Player {turn} column: ')) - 1
        else:
            if config.BOT_STATS:
                t0 = time.time()
            col = bot.generate_move(grid, turn, hv=config.HEURISTIC_TYPE, depth=config.BOT_DEPTH)
            if config.BOT_STATS:
                print(time.time() - t0, nmoves)
        if col < 0 or col >= config.BOARD_WIDTH:
            continue
        ch = game.col_height(col, grid)
    grid[ch][col] = turn
    last_spot = (ch, col)

if game.check_game_over(grid):
    print(f"Tie in {nmoves} turns!")
else:
    game.render_grid(grid)
    print(f'Player {turn} wins in {nmoves} turns!')