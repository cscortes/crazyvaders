import pygame

from lib  import invaderutils
from lib.Background import Background
from lib.GameObjectKeeper import GameObjectKeeper
from lib.MyExceptions import QuitProgram
from lib.Hero import Hero
from lib.AnimatedSprite import AnimatedSprite
from lib.mylogging import log


class GameMachine(object):
    clock = None
    game_mode = invaderutils.MODE_FIGHT_EVENT

    def __init__(self, width, height):
        invaderutils.set_game_dimensions(width, height)
        GameObjectKeeper.special_setup(Background(), 0)
        GameMachine.clock =  pygame.time.Clock()

    def run(self, collide_fun):
        try:
            while GameMachine.game_mode in [invaderutils.MODE_FIGHT_EVENT, invaderutils.HERO_KILLED_EVENT]:
    
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
                    go.draw(Background.get_screen())

    
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
            ev = pygame.event.Event( invaderutils.HERO_KILLED_EVENT, {'message': "Hero is dead!"})
            pygame.event.post(ev)


    def process_events(self, evt):
        if evt.type == invaderutils.HERO_KILLED_EVENT:
            self.setup_loser_screen()
            GameMachine.game_mode = invaderutils.HERO_KILLED_EVENT

        if evt.type == invaderutils.GAME_END_EVENT:
            log.info("Bye!")
            GameMachine.game_mode = invaderutils.GAME_END_EVENT

    def setup_loser_screen(self):
        for go in GameObjectKeeper.runables():
            GameObjectKeeper.remove(go)

        bye = AnimatedSprite(300, 350, ["images/game/gameover.png"])
        GameObjectKeeper.setupenemy(bye, 1000)

        pygame.time.set_timer(invaderutils.GAME_END_EVENT, 2500)
