#!/bin/python3
# Need to add the GPL3 to every file

import pygame

from lib import invaderutils
from lib.AutoMovingAnimatedSprite import AutoMovingAnimatedSprite
#from lib.Banner import Banner
#from lib.Enemy import Enemy
#from lib.GameBase import *
from lib.GameMachine import GameMachine
from lib.GameObjectKeeper import GameObjectKeeper
#from lib.Hero import Hero
#from lib.HighscoreStore import HighscoreStore
from lib.LineOfNumbers import LineOfNumbers
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
