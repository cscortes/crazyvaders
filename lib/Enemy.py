import random

from lib import invaderutils
from lib.AutoMovingAnimatedSprite import AutoMovingAnimatedSprite
from lib.GameObjectKeeper import GameObjectKeeper


class Enemy(AutoMovingAnimatedSprite):

    def __init__(self, ix, iy, filenames, steps=10, movex=1, movey=0, msteps=1, bombclockpts=(1000,2000), lowermove=20, bonus=5):
        super().__init__(ix, iy, filenames, steps)
        self.BOMBCLOCKPTS = bombclockpts
        self.bombclock = self.get_bombtics()
        self.movex = movex
        self.movey = movey
        self.lowermove = lowermove
        self.bonus = bonus

    def get_bombtics(self):
        return random.randint(self.BOMBCLOCKPTS[0], self.BOMBCLOCKPTS[1])

    def cliplefthandler(self):
        self.movex = -self.movex
        self.y += self.lowermove

    def cliprighthandler(self):
        self.movex = -self.movex
        self.y +=  self.lowermove

    def process_keys(self, pressed):
        self.bombclock -= 1

        if (self.bombclock <= 0):
            self.bombclock = self.get_bombtics()
            self.fire_bomb()

    def fire_bomb(self):
        newx = int(self.x + self.get_width()/2 - 10)
        newy = self.y + self.get_height()

        self.mis_steps = 0
        bomb = AutoMovingAnimatedSprite(newx, newy, 
            invaderutils.bomb_png(), 
            movex=0, movey=4, msteps=1)
        GameObjectKeeper.setupenemy(bomb, 45)

    def draw(self, screen):
        self.clipx(self.cliplefthandler, self.cliprighthandler)
        super().draw(screen)

def enemy_little_john(x, y):
    # return Enemy(x, y, invaderutils.invader_png(3), bombclockpts=(400,750), lowermove=100, bonus=5)
	return Enemy(x, y, invaderutils.multi_invader_png(3,5), bombclockpts=(400,750), lowermove=100, bonus=5)

def enemy_fonzy(x,y,movex):
    return Enemy(x, y, invaderutils.multi_invader_png(1,5), bombclockpts=(500,1000), lowermove=60,movex=movex, bonus=20)

def enemy_the_frig(x,y,movex):
    return Enemy(x, y, invaderutils.invader_png(2), bombclockpts=(200,750), lowermove=40, movex=movex, bonus=10)

def enemy_smiling_vader(x,y,movex):
    return Enemy(x, y, invaderutils.invader_png(4), bombclockpts=(75,250), lowermove=60, movex=movex, bonus=35)
