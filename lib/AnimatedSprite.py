import pygame
from lib.StaticObject import StaticObject

class AnimatedSprite(StaticObject):
    def __init__(self, ix, iy, filenames, steps=10):
        super().__init__()
        self.count = 0
        self.images = []
        for f in filenames:
            self.images.append(pygame.image.load(f))
        self.x = ix 
        self.y = iy
        self.STEPS = steps
        self.steps = 0
        self.picsize = self.images[0].get_size()

    def draw(self, screen):
        image = self.images[self.count]
        screen.blit(image, (self.x, self.y))

        self.steps += 1
        if (self.steps >= self.STEPS):
            self.count = self.count + 1
            self.count = self.count % len(self.images)
            self.steps = 0
