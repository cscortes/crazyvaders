import pygame
from lib.AnimatedSprite import AnimatedSprite
from lib.AutoMovingAnimatedSprite import AutoMovingAnimatedSprite
from lib import invaderutils
from lib.GameObjectKeeper import GameObjectKeeper

class Hero(AnimatedSprite):
    MIS_STEPS = 0  # Number of waits before we trigger another missile
    mis_steps = 0
    MOVE_STEPS = 0 # Number of waits before we allow another move
    move_steps = 0

    def __init__(self, ix, iy, filenames, steps=1, move_steps=1, mis_steps=50):
        """What is steps, and msteps?? """

        super().__init__(ix, iy, filenames, steps)
        Hero.MIS_STEPS = mis_steps
        Hero.MOVE_STEPS = move_steps

        self.effect = pygame.mixer.Sound('sounds/thump.wav')
        self.effect.set_volume(0.03)


    def process_events(self, evt):
        if (self.mis_steps >= Hero.MIS_STEPS):
            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                self.fire_missile()

    def process_keys(self, pressed):
        """constantly being called"""

        self.mis_steps += 1
        self.move_steps += 1

        if (self.mis_steps >= Hero.MIS_STEPS):
            if pressed[pygame.K_UP]: 
                self.fire_missile()

        if (self.move_steps >= Hero.MOVE_STEPS):
            self.move_steps = 0
            if pressed[pygame.K_LEFT]: 
                self.x -= self.STEPS
            if pressed[pygame.K_RIGHT]: 
                self.x += self.STEPS

        self.myclipx()

    def myclipx(self):
        """ Keeps the ship from hanging out at the edge where aliens can't
        shoot it. """
        if (self.x < 40):
            self.x = 0+40

        if (self.x+self.get_width() + 40 > invaderutils.get_game_width()):
            self.x = invaderutils.get_game_width() - self.get_width()-40 

    def fire_missile(self):
        self.mis_steps = 0

        newx = int(self.x + self.get_width()/2)
        newy = self.y

        missile = AutoMovingAnimatedSprite(
            newx, newy,
            invaderutils.missile_png(), movex=0, movey=-4, 
            msteps=1)
        GameObjectKeeper.setupfriendly(missile, 45)
