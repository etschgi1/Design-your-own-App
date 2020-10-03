################################################################################
# Python challenge 2
# Your task is to implement a simple beverage dispenser.
#
# Name: Wachmann Elias
# Matriculation number: 12004232
################################################################################

# your code below here
BEVERAGE_PRICE = 50
VALID_COINS = [1,  2,  5,  10,  20,  50,  100,  200]
NUMBER_OF_TOTAL_COINS = 0
INSERTED_COINS = []


def display_promt():
    """Displays user prompt"""
    global NUMBER_OF_TOTAL_COINS, INSERTED_COINS, VALID_COINS

    upromt = input(f"Currently inserted {NUMBER_OF_TOTAL_COINS}\n" +
                   "Please insert a coin: ")
    try:
        upromt = int(upromt)
    except ValueError:
        print(f"'{upromt}' is clearly not a coin...\nPlease use valid coins only.")
        return
    if upromt in VALID_COINS:
        NUMBER_OF_TOTAL_COINS += upromt
        INSERTED_COINS.append(upromt)
    else:
        print(f"The coin '{upromt}' seemed weird!\n" +
              "Please use valid coins only.")


def check_price():
    """Checks wether or not the correct price is reached"""
    global NUMBER_OF_TOTAL_COINS, BEVERAGE_PRICE

    if NUMBER_OF_TOTAL_COINS == BEVERAGE_PRICE:
        return True
    elif NUMBER_OF_TOTAL_COINS < BEVERAGE_PRICE:
        return False
    else:
        return "FATAL"


def list_coins():
    global INSERTED_COINS
    """Lists als inserted coins if too many were inserted"""
    print("You inserted too many coins:")
    for coin in INSERTED_COINS:
        print(f"  {coin}")
    print("Please start over.")


def run():
    global NUMBER_OF_TOTAL_COINS, INSERTED_COINS
    while True:
        display_promt()
        if check_price() == True:
            print("Thank you for your purchase.\nEnjoy your beverage.")
            break
        elif check_price() == "FATAL":
            list_coins()
            NUMBER_OF_TOTAL_COINS = 0
            INSERTED_COINS = []
            continue


run()
