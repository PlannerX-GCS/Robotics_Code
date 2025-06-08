from ROBOT_ACTIONS import *
from time import sleep, ticks_ms, ticks_diff
from random import randint

easy_speed = 0.2
medium_speed = 0.1
hard_speed = 0.001

def difficulty_selection():
    options = ["easy", "medium", "hard"]
    delays = {"easy": 0.2, "medium": 0.1, "hard": 0.001}
    index = 0
    last_move = ticks_ms()

    while True:
        display_options = [opt.upper() if i == index else opt for i, opt in enumerate(options)]
        
        clean_lcd()
        write_on_lcd("Hash-Dodge", 0, 3)
        line = " ".join(display_options)
        write_on_lcd(line[:16], 1, 0)

        sleep(0.01)
        
        x, y, _ = read_from_joystick()

        if x == 0 and index < 2:
            index += 1
            last_move = ticks_ms()
        elif y == 0 and index > 0:
            index -= 1
            last_move = ticks_ms()

        if ticks_diff(ticks_ms(), last_move) > 3000:
            return delays[options[index]]

game_speed = difficulty_selection()

player_col = 0
score = 0

while True:
    obstacle_col = 15
    game_over = False
    air_obstacle_col = 12 - randint(1, 5)

    for _ in range(16):
        clean_lcd()
        
        score = score+1
        
        write_on_lcd(score, 0, 13)

        jump, _, _ = read_from_joystick()
        player_row = 1 if jump == 1 else 0

        write_on_lcd("^", player_row, player_col)

        write_on_lcd("#", 1, obstacle_col)
        if 0 <= air_obstacle_col <= 15:
            write_on_lcd("#", 0, air_obstacle_col)

        if (player_row == 1 and obstacle_col == player_col) or \
           (player_row == 0 and air_obstacle_col == player_col):
            clean_lcd()
            write_on_lcd("Game Over", 0, 4)
            game_over = True
            break

        sleep(game_speed)
        obstacle_col -= 1
        air_obstacle_col -= 1

    if game_over:
        sleep(2)
        clean_lcd()
        score = 0

