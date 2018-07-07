#!/bin/python3
# Need to add the GPL3 to every file

from lib import invaderutils
from lib.GameMachine import GameMachine
from lib.mylogging import log

def main():
    log.info("Starting game ...")

    game = GameMachine(800,800)
    game.setup()
    game.run()
    game.teardown()

    log.info("... Game Done!")

main()

print("Have a good one!  -- Luis")
