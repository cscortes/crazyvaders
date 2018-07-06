import pygame

class GameBase(object):

    _FONT_NORMAL   = None
    _FONT_SMALL    = None
    _FONT_XSMALL   = None

    def __init__(self):
        pass

    @classmethod
    def get_font_normal(cls):
        if (cls._FONT_NORMAL is None):
            cls._FONT_NORMAL = pygame.font.SysFont("monospace", 30, bold=1)
        return cls._FONT_NORMAL

    @classmethod
    def get_font_small(cls):
        if (cls._FONT_SMALL is None):
            cls._FONT_SMALL = pygame.font.SysFont("monospace", 22)
        return cls._FONT_SMALL

    @classmethod
    def get_font_xsmall(cls):
        if (cls._FONT_XSMALL is None):
            cls._FONT_XSMALL = pygame.font.SysFont("monospace", 15)
        return cls._FONT_XSMALL
