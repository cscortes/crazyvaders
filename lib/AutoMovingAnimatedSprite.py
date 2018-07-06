from lib.AnimatedSprite import AnimatedSprite
from lib.mylogging import log

class AutoMovingAnimatedSprite(AnimatedSprite):
    def __init__(self, ix, iy, filenames, steps=10, movex=0, movey=0, msteps=1):
        super().__init__(ix, iy, filenames, steps)
        self.movex = movex 
        self.movey = movey
        self.MSTEPS = msteps
        self.msteps = 0

    def draw(self, screen):
        self.msteps += 1
        if self.msteps >= self.MSTEPS:
            self.mstep = 0
            self.x += self.movex
            self.y += self.movey
            self.clipy(self.clipbottomthandler, self.cliptopthandler)
        super().draw(screen)

    def cliptopthandler(self):
        log.debug("Clip Top called")
        self.terminate()

    def clipbottomthandler(self):
        log.debug("Clip bottom called")
        self.terminate()
