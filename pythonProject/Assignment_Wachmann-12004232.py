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
    global LIVES, SNAKE, SCORE
    # "Your name for the history: "
    username = input("Your name for the history: ")
    if username == "q":
        exit()
    # "NAME - Score: SCORE- Lives: LIVES - Snake Length: SNAKE_LENGTH\n"
    entry = (f"{username} - Score: {SCORE}- Lives: {LIVES}" +
             f" - Snake Length: {len(SNAKE)}\n")
    f = open("history.txt", "r")
    lines = f.readlines()
    f.close()
    if len(lines) > 3:  # to keep only a maximum of 4 entries in total
        del lines[0]
    lines.append(entry)
    # print history
    print("\n\nHistory:")
    f = open("history.txt", "w")
    for line in lines:
        f.write(line)
        print(line, end="")
    f.close()
    lines = []
    exit()


def _6_spawn_apple():
    # Show new apples for 10 rounds
    global APPLE_GOT_EATEN, APPLE_LIVES, LIVES, SNAKE, APPLE
    if APPLE_GOT_EATEN or APPLE_LIVES < 1:
        APPLE_GOT_EATEN = False
        if APPLE_LIVES < 1:
            LIVES -= 1
            if LIVES == 0:
                _7_submit_score()
                exit()
        # spawn new apple
        while True:
            potfield = random.choice(ALPHA)+str(random.choice(range(8)))
            if potfield not in SNAKE and potfield != APPLE:
                APPLE = potfield
                break
        APPLE_LIVES = 12
    APPLE_LIVES -= 1


def _5_detect_collision():
    # Return True if the snake collides with a border or itself
    global SNAKE, APPLE, APPLE_GOT_EATEN, BIGGER_SNAKE
    head = SNAKE[-1]
    body = SNAKE[0:-1]
    # dedect collision with apple
    if head == APPLE:
        APPLE_GOT_EATEN = True
        BIGGER_SNAKE = True
        return False
    # dedect collision with snake
    if head in body:
        return True
    # dedect wall collision
    if head == "Dead Already":
        return True
    a = head[0]
    n = int(head[1:])
    if n < 0 or n > 7:
        return True


def _4_move_snake():
    # Let the snake slide
    global BIGGER_SNAKE, SNAKE, ALPHA
    lastpos = SNAKE[-1]
    ai = ALPHA.index(lastpos[0])
    ni = int(lastpos[1])
    try:
        if ORIENTATION == 2:  # snake moves up
            ai -= 1
            lastpos = str(ALPHA[ai])+lastpos[1]
            if ai < 0:
                raise IndexError("You can't go there!!!")
            SNAKE.append(lastpos)
        elif ORIENTATION == 3:  # snake moves left
            ni -= 1
            lastpos = lastpos[0]+str(ni)
            SNAKE.append(lastpos)
        elif ORIENTATION == 4:  # snake moves down
            ai += 1
            lastpos = str(ALPHA[ai])+lastpos[1]
            SNAKE.append(lastpos)
        elif ORIENTATION == 5:  # snake moves right
            ni += 1
            lastpos = lastpos[0]+str(ni)
            SNAKE.append(lastpos)
        # remove first element of snake
        if not BIGGER_SNAKE:
            del SNAKE[0]
    except IndexError:  # if index out of range
        SNAKE.append("Dead Already")


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
                if c == 7:
                    print("|")
                continue
            if _3_is_snake(r, c) > 0:  # check if there is a snake
                s = _3_is_snake(r, c)
                print(" {} ".format(POSORIENTATION[s]), end="")
                if c == 7:
                    print("|")
                continue
            if c != 7:
                print("   ", end="")
            else:
                print("   "+"|")
    print(LINE)
    print("    0  1  2  3  4  5  6  7")


def main():
    # main function, call other functions here
    global ORIENTATION, SCORE, BIGGER_SNAKE
    keymap = {"w": 2, "a": 3, "s": 4, "d": 5}
    forbiddenmove = "w"
    while True:
        _1_print_game_board()
        _6_spawn_apple()
        userin = input("input [w a s d]: ")
        if userin == "q":
            exit()
        elif userin in keymap.keys():
            neworientation = keymap[userin]
            if userin != forbiddenmove:  # valid round
                ORIENTATION = neworientation
                _4_move_snake()
                if BIGGER_SNAKE:  # deactivate bigger snake after growing once
                    BIGGER_SNAKE = False
                coll = _5_detect_collision()
                if coll:
                    _7_submit_score()
                    exit()
                SCORE += 1

                # get forbidden move
                if ORIENTATION == 2:
                    forbiddenmove = "s"
                elif ORIENTATION == 3:
                    forbiddenmove = "d"
                elif ORIENTATION == 4:
                    forbiddenmove = "w"
                else:
                    forbiddenmove = "a"
            elif userin == forbiddenmove:
                print("INVALID")


if __name__ == '__main__':
    main()
