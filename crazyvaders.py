#!/bin/python3

## Need to add the GPL3 to every file

import pygame
from invaderutils import *
from mylogging import log
from gamestore import HighscoreStore

effect = None
highscorestore = HighscoreStore()
myscoreboard = None

def collide_action(friend, enemy):
    """ TODO: really don't like this routine here.  """

    global effect 

    log.debug("COLLIDED: {0} {1}".format(type(friend),type(enemy)))
    effect.play()

    friend.terminate()
    enemy.terminate()

    explosion = AutoMovingAnimatedSprite(
        enemy.x, enemy.y, 
        explosion_png(), 
        movex=0, movey=-1, msteps=1)
    GameObjectKeeper.setup(explosion, 35)
    myscoreboard.addscore(5)
    highscorestore.set_highscore(myscoreboard.getscore())

def main():
    global effect 
    log.info("Starting game...")

    game = GameMachine(800,800)

    effect = pygame.mixer.Sound('sounds/thump.wav')
    effect.set_volume(0.03)

    setupscore()

    GameObjectKeeper.setupfriendly(Hero(100,710,hero_png(),steps=5, move_steps=2), 50)

    badguys()

    game.run(collide_action)

def setupscore():
    banner = Banner("SCORE", Game.get_font_normal(), pos=(0, 10))
    GameObjectKeeper.setup(banner, 1000)

    global myscoreboard
    myscoreboard = Score( 0, 35, Game.get_font_normal(), COLOR_YELLOW)
    GameObjectKeeper.setup(myscoreboard, 1000)

    banner = Banner("HIGH SCORE", Game.get_font_normal(), pos=(300, 10))
    GameObjectKeeper.setup(banner, 1000)

    banner = Banner("{0:010}".format(highscorestore.get_highscore()), Game.get_font_normal(), pos=(300, 35), color=COLOR_YELLOW)
    GameObjectKeeper.setup(banner, 1000)

    highscorestore.get_highscore()


def badguys():
    for x in range( 0, 800, 100):
        enemy = Enemy(x, 25, invader_png(4), bombclockpts=(100,250), lowermove=30, movex=-3)
        GameObjectKeeper.setupenemy(enemy, 50)

        enemy = Enemy(x-55, 100, invader_png(2), bombclockpts=(1500,3000), lowermove=40)
        GameObjectKeeper.setupenemy(enemy, 50)

        enemy = Enemy(x, 175, invader_png(1), bombclockpts=(1000,2000), lowermove=60,movex=-2)
        GameObjectKeeper.setupenemy(enemy, 50)

        enemy = Enemy(x+25, 250, invader_png(3), bombclockpts=(1000,4000), lowermove=80)
        GameObjectKeeper.setupenemy(enemy, 50)


main()
highscorestore.update()
log.info("Game Done!")



