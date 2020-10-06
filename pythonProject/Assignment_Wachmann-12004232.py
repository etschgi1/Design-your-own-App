# Snake - DYOA at TU Graz WS 2020
# Name:       Wachmann
# Student ID: 12004232

import random

BOARD_WIDTH = 8
BOARD_HEIGHT = 8
SNAKE = ["B2", "B3", "B4", "C4", "D4"]
ORIENTATION = 4
# 2 means the snake’s head looks up
# 3 means the snake’s head looks left
# 4 means the snake’s head looks down
# 5 means the snake’s head looks right.

APPLE = "B6"
APPLE_LIVES = 12
APPLE_GOT_EATEN = False
LIVES = 3
SCORE = 0
BIGGER_SNAKE = False

ALPHA = ["A", "B", "C", "D", "E", "F", "G", "H"]
POSORIENTATION = {1: "+", 2: "∧", 3: "<", 4: "v", 5: ">"}


def _7_submit_score():
    # Store the history

    # "Your name for the history: "
    # "NAME - Score: SCORE- Lives: LIVES - Snake Length: SNAKE_LENGTH\n"
    # history.txt
    # "\n\nHistory:"
    pass


def _6_spawn_apple():
    # Show new apples for 10 rounds
    pass


def _5_detect_collision():
    # Return True if the snake collides with a border or itself
    pass


def _4_move_snake():
    # Let the snake slide
    pass


def _3_is_snake(row, column):
    # return numbers 0-5, accordingly
    global ORIENTATION
    field = row+str(column)
    if field not in SNAKE:
        return 0
    elif field == SNAKE[-1]:
        return ORIENTATION
    else:
        return 1


def _2_is_apple(row, column):
    # return True if the apple is in the given coordinate
    global APPLE
    field = row+str(column)
    return True if field == APPLE else False


def _1_print_game_board():
    global LIVES, APPLE_LIVES, SCORE, ALPHA, POSORIENTATION
    # print the game field
    # "Lives: LIVES - Apple Lives: APPLE_LIVES - Score: SCORE"
    LINE = "----------------------------"
    # "    0  1  2  3  4  5  6  7"
    # field spacing: " " + fieldSymbol + " "
    # empty field symbol: " "
    # apple field symbol: "O"
    # snake body field symbol:  "+"
    # snake up field symbol:    "∧"
    # snake left field symbol:  "<"
    # snake down field symbol:  "v"
    # snake right field symbol: ">"
    print("Lives: {} - Apple Lives: {} - Score: {}".format(LIVES, APPLE_LIVES, SCORE))
    print(LINE)
    emptyrow = " "
    for r in ALPHA:
        print(r+" |", end="")
        for c in range(8):
            if _2_is_apple(r, c):
                print(" O ", end="")
                continue
            if _3_is_snake(r, c) > 0:  # check if there is a snake
                s = _3_is_snake(r, c)
                print(" {} ".format(POSORIENTATION[s]), end="")
                continue
            if c != 7:
                print("   ", end="")
            else:
                print("   "+"|")
    print(LINE)
    print("    0  1  2  3  4  5  6  7")


def main():
    # main function, call other functions here
    _1_print_game_board()
    #print(_3_is_snake("B", 2))


if __name__ == '__main__':
    main()
