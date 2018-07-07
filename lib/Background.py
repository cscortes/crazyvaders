import pygame

from lib import invaderutils
from lib.GameObject import GameObject
from lib.MyExceptions import QuitProgram


class Background(GameObject):
    """@todo: Rethink _SCREEN, maybe should be instance variable -- this is really a singleton object"""
    _SCREEN = None

    def __init__(self):
        super().__init__()

        pygame.init()
        Background._SCREEN = pygame.display.set_mode(
            (invaderutils.get_game_width(), 
            invaderutils.get_game_height())
        )

    def process_events(self, evt):
        """@todo: Maybe all game events should go here??"""
        
        if evt.type == pygame.QUIT:
            raise QuitProgram

    def draw(self, screen):
        # screen should be Solid color
        screen.fill(invaderutils.COLOR_BLUE)

    @classmethod
    def get_screen(cls):
        return cls._SCREEN
