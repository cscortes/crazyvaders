import os
import pygame 

# My color definitions, maybe pygame has them somewhere, these may 
# disappear in the future.
#
COLOR_WHITE  = (255,255,255)
COLOR_BLACK  = (0,0,0)
COLOR_BLUE   = (6, 3, 41)
COLOR_ORANGE = (255, 100, 0)
COLOR_YELLOW = (255,255,51)


# Custom event identifers
#
HERO_KILLED_EVENT = pygame.USEREVENT + 1
MODE_FIGHT_EVENT  = pygame.USEREVENT + 2
GAME_END_EVENT    = pygame.USEREVENT + 3

# These values are used all over the place
# can't make up my mind how to handle them
# really could be here or at the beginning 
# of the program.  They started at the beginning
# of the program, but now seem to be better off
# here.  @later

_GAME_WIDTH = None
_GAME_HEIGHT = None

def set_game_dimensions(width, height):
    global _GAME_HEIGHT
    global _GAME_WIDTH
    _GAME_WIDTH = width
    _GAME_HEIGHT = height

def get_game_width():
    return _GAME_WIDTH

def get_game_height():
    return _GAME_HEIGHT

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


