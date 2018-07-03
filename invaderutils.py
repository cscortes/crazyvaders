import pygame
import os
from gamestore import GameObjectKeeper, GameBase
import random
import sys
import numpy as np
from mylogging import log 


COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_BLUE  = (6, 3, 41)
COLOR_ORANGE = (255, 100, 0)
COLOR_YELLOW = (255,255,51)

HERO_KILLED_EVENT = pygame.USEREVENT + 1
MODE_FIGHT_EVENT  = pygame.USEREVENT + 2
GAME_END_EVENT    = pygame.USEREVENT + 3


def add_dir(direct, files):
    return [ os.path.join(direct, f) for f in files ]

def hero_dir(files):    
    return add_dir("images/hero", files)

def invader_dir(files):    
    return add_dir("images/invader",  files)

def explosion_dir(files):    
    return add_dir("images/explosion",  files)

def invader_png(n):
    return invader_dir(["enemy{}.png".format(n)])

def hero_png():
    return hero_dir(["hero.png"])

def missile_png():
    return hero_dir(["hero_missile.png"])

def explosion_png():
    return explosion_dir(["stardust_sm_%02d.png" % idx for idx in range(0,10)])

def bomb_png():
    return add_dir("images/invader", ["ebomb.png"])


class QuitProgram(RuntimeError):
    def __init__(self):
        pass

class GameMachine(object):
    clock = None
    game_mode = MODE_FIGHT_EVENT

    def __init__(self, width, height):
        self.width = width
        self.height = height
        GameObjectKeeper.special_setup(Game(width, height), 0)
        GameMachine.clock =  pygame.time.Clock()

    def run(self, collide_fun):
        try:
            while GameMachine.game_mode in [MODE_FIGHT_EVENT, HERO_KILLED_EVENT]:
    
                self.remove_terminated()

                events = pygame.event.get()
                pressed = pygame.key.get_pressed()

                for event in events:
                    self.process_events(event)

                for go in GameObjectKeeper.runables():
                    for event in events:
                        go.process_events(event)
                    go.process_keys(pressed)

                self.collision_detection(collide_fun)

                for go in GameObjectKeeper.runables():
                    go.draw(Game.get_screen())

    
                # Flip the drawing buffers
                pygame.display.flip()
                GameMachine.clock.tick(120)

        except QuitProgram as e_info:
            pass

    def remove_terminated(self):
        for go in GameObjectKeeper.runables():
            if (go.removeme()):
                GameObjectKeeper.remove(go)
                break

    def collision_detection(self, collide_fun):
        for enemy in GameObjectKeeper.enemies():
            for friend in GameObjectKeeper.friendlies():
                if enemy.collide(friend):
                    collide_fun(friend, enemy)
                    self.check_friend_hero(friend)

    def check_friend_hero(self, friend):
        if isinstance(friend, Hero):
            ev = pygame.event.Event( HERO_KILLED_EVENT, {'message': "Hero is dead!"})
            pygame.event.post(ev)


    def process_events(self, evt):
        if evt.type == HERO_KILLED_EVENT:
            self.setup_loser_screen()
            GameMachine.game_mode = HERO_KILLED_EVENT

        if evt.type == GAME_END_EVENT:
            log.info("Bye!")
            GameMachine.game_mode = GAME_END_EVENT

    def setup_loser_screen(self):
        for go in GameObjectKeeper.runables():
            GameObjectKeeper.remove(go)

        bye = AnimatedSprite(300, 350, ["images/game/gameover.png"])
        GameObjectKeeper.setupenemy(bye, 1000)

        pygame.time.set_timer(GAME_END_EVENT, 2500)

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

        if (self.x+self.get_width() > Game.width):
            self.x = Game.width - self.get_width() 
            if (cliprightfunc is not None):
                cliprightfunc()

    def clipy(self, clipbottomfunc = None, cliptopfunc = None):
        if (self.y < 0):
            self.y = 0
            if (cliptopfunc is not None):
                cliptopfunc()

        if (self.y+self.get_height() > Game.height):
            self.y = Game.height + self.get_height()
            if (clipbottomfunc is not None):
                clipbottomfunc()

    def get_width(self):
        return self.picsize[0]

    def get_height(self):
        return self.picsize[1]

class StaticObject(GameObject):
    def __init__(self):
        super().__init__()

    def process_events(self, evt):
        pass

    def process_keys(self, pressed):
        pass

class Game(GameObject):
    FONT_NORMAL   = None
    FONT_SMALL    = None
    FONT_XSMALL   = None
    screen = None
    width = 0
    height = 0

    def __init__(self, width: int, height: int) -> None:
        super().__init__()

        pygame.init()
        Game.screen = pygame.display.set_mode((width, height))
        Game.width = width
        Game.height = height

    def process_events(self, evt):
        if evt.type == pygame.QUIT:
            raise QuitProgram

    def draw(self, screen):
        # screen should be blank
        screen.fill(COLOR_BLUE)

    @classmethod
    def get_font_normal(cls):
        if (cls.FONT_NORMAL is None):
            cls.FONT_NORMAL = pygame.font.SysFont("monospace", 30, bold=1)
        return cls.FONT_NORMAL

    @classmethod
    def get_font_small(cls):
        if (cls.FONT_SMALL is None):
            cls.FONT_SMALL = pygame.font.SysFont("monospace", 22)
        return cls.FONT_SMALL

    @classmethod
    def get_font_xsmall(cls):
        if (cls.FONT_XSMALL is None):
            cls.FONT_XSMALL = pygame.font.SysFont("monospace", 15)
        return cls.FONT_XSMALL

    @classmethod
    def get_screen(cls):
        return cls.screen

class MovingBox(GameObject):
    STEP = 10 
    def __init__(self, ix = 30, iy = 30, iwidth=60, iheight=60, iblue=True):
        super().__init__()
        self.is_blue = iblue
        self.x = ix
        self.y = iy
        self.width = iwidth
        self.height = iheight

    def process_events(self, evt):
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
            self.is_blue = not self.is_blue

        # render text
        if self.is_blue: self.color = COLOR_BLUE
        else: self.color = COLOR_ORANGE

    def process_keys(self, pressed):
        if pressed[pygame.K_UP]: 
            self.fire_missile()

        if pressed[pygame.K_LEFT]: self.x -= self.STEP
        if pressed[pygame.K_RIGHT]: self.x += self.STEP

    def fire_missile(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

class LineOfNumbers(StaticObject):
    def __init__(self, ix, iy, fontrequested, color = COLOR_WHITE):
        super().__init__()
        self.x = ix
        self.y = iy
        self.numbers = self.create_bag_numbers(fontrequested, color)
        
    def create_bag_numbers(self, font, color = COLOR_WHITE):
        bag = []
        for i in range(0,10):
            bag.append(font.render("%d" % i, 1, color))
        return bag 

    def draw(self, screen):
        for i in range(0, 20):
           screen.blit(self.numbers[i % 10],   (self.x  + i * 20, self.y))

class Banner(StaticObject):
    RENDERED : dict = {}

    def __init__(self, word, fontrequested, pos = (0,0), color = COLOR_WHITE, spacing=20):
        super().__init__()
        self.pos = pos
        self.word = word
        self.font = fontrequested
        self.color = color
        self.spacing = spacing
    
    def draw(self, screen):
        for idx, ch in enumerate(self.word):
            offset =  np.add(self.pos , (idx*self.spacing, 0))
            screen.blit(self.get_rendr(ch), offset)

    def get_rendr(self, ch):
        if not ch in Banner.RENDERED.keys():
            Banner.RENDERED[ch] = self.font.render(ch, 1, self.color)

        return Banner.RENDERED[ch]

class Score(LineOfNumbers):
    def __init__(self, ix, iy, fontrequested, color = COLOR_WHITE, score=0):
        super().__init__(ix, iy, fontrequested, color)
        self.score = score

    def draw(self, screen):
        tempscore = "%010d" % self.score

        for i in range(0, 10):
            val = int(tempscore[i])
            screen.blit(self.numbers[val],   (self.x  + i * 20, self.y))

    def addscore(self, bonus:int) -> None:
        self.score += bonus
        self.mis_steps = 0

    def getscore(self) -> int:
        return self.score

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
#            self.clipx()
            self.clipy(self.clipbottomthandler, self.cliptopthandler)
        super().draw(screen)

    def cliptopthandler(self):
        log.debug("Clip Top called")
        self.terminate()

    def clipbottomthandler(self):
        log.debug("Clip bottom called")
        self.terminate()

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
        if (self.x < 40):
            self.x = 0+40

        if (self.x+self.get_width() + 40 > Game.width):
            self.x = Game.width - self.get_width() -40 


    def fire_missile(self):
        self.mis_steps = 0

        newx = int(self.x + self.get_width()/2)
        newy = self.y

        missile = AutoMovingAnimatedSprite(
            newx, newy,
            missile_png(), movex=0, movey=-4, 
            msteps=1)
        GameObjectKeeper.setupfriendly(missile, 45)


class Enemy(AutoMovingAnimatedSprite):

    def __init__(self, ix, iy, filenames, steps=10, movex=1, movey=0, msteps=1, bombclockpts=(1000,2000), lowermove=20):
        super().__init__(ix, iy, filenames, steps)
        self.BOMBCLOCKPTS = bombclockpts
        self.bombclock = self.get_bombtics()
        self.movex = movex
        self.movey = movey
        self.lowermove = lowermove

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
            bomb_png(), 
            movex=0, movey=4, msteps=1)
        GameObjectKeeper.setupenemy(bomb, 45)

    def draw(self, screen):
        self.clipx(self.cliplefthandler, self.cliprighthandler)
        super().draw(screen)
