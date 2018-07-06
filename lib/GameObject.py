from lib import invaderutils
from lib.GameBase import GameBase


class GameObject(GameBase):
    def __init__(self):
        self.request_removeme = False

    def process_events(self, evt):
        raise NotImplementedError("Need to implement this")

    def process_keys(self, pressed):
        # Not all objects need to process key presses
        pass
    
    def draw(self, screen):
        raise NotImplementedError("Need to implement this")

    def  __lt__ (self, other):
        return id(self) < id(other )

    def collide(self, other):
        xs = set( range(self.x, self.x + self.get_width()))
        oxs = set( range(other.x, other.x + other.get_width()))

        ys = set( range(self.y, self.y + self.get_height()))
        oys = set( range(other.y, other.y + other.get_height()))

        xset = xs.intersection(oxs)
        yset = ys.intersection(oys)

        return (len(xset) > 0) and (len(yset)>0) 

    def removeme(self):
        return self.request_removeme

    def terminate(self):
        self.request_removeme = True

    def clipx(self, clipleftfunc = None, cliprightfunc = None):
        if (self.x < 0):
            self.x = 0
            if (clipleftfunc is not None):
                clipleftfunc()

        if (self.x+self.get_width() > invaderutils.get_game_width()):
            self.x = invaderutils.get_game_width() - self.get_width() 
            if (cliprightfunc is not None):
                cliprightfunc()

    def clipy(self, clipbottomfunc = None, cliptopfunc = None):
        if (self.y < 0):
            self.y = 0
            if (cliptopfunc is not None):
                cliptopfunc()

        if (self.y+self.get_height() > invaderutils.get_game_height()):
            self.y = invaderutils.get_game_height() + self.get_height()
            if (clipbottomfunc is not None):
                clipbottomfunc()

    def get_width(self):
        return self.picsize[0]

    def get_height(self):
        return self.picsize[1]
