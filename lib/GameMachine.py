import pygame

from lib import invaderutils
from lib.AnimatedSprite import AnimatedSprite
from lib.AutoMovingAnimatedSprite import AutoMovingAnimatedSprite
from lib.Background import Background
from lib.Banner import Banner
from lib.Enemy import Enemy
from lib.GameBase import GameBase
from lib.GameObjectKeeper import GameObjectKeeper
from lib.Hero import Hero
from lib.HighscoreStore import HighscoreStore
from lib.MyExceptions import QuitProgram
from lib.mylogging import log
from lib.Score import Score
from lib.Transitions import Transitions


class Thump(object):
    effect = None

    def __init__(self):
        if (Thump.effect is None):
            self.setup()
        self.play()

    def setup(self):
        Thump.effect = pygame.mixer.Sound('sounds/thump.wav')
        Thump.effect.set_volume(0.03)
        
    def play(self):
        Thump.effect.play()

class GameMachine(object):
    clock = None
    game_mode = None
    transitions : Transitions = None
    highscorestore : HighscoreStore = None 

    def __init__(self, width, height):
        invaderutils.set_game_dimensions(width, height)
        GameMachine.clock =  pygame.time.Clock()
        GameMachine.game_mode = invaderutils.GAME_STARTED_EVENT
        GameMachine.transitions = Transitions()
        GameMachine.highscorestore = HighscoreStore()
        GameObjectKeeper.special_setup(Background(), 0)

    def teardown(self):
        GameMachine.highscorestore.update()

    def setup(self):
        self.transitions.add(invaderutils.GAME_STARTED_EVENT, invaderutils.MODE_FIGHT_EVENT, 10, self.wave_0)


    def run(self):
        
        GameMachine.game_mode = invaderutils.MODE_FIGHT_EVENT

        try:
            while GameMachine.game_mode in [
                invaderutils.MODE_FIGHT_EVENT, invaderutils.HERO_KILLED_EVENT]:

                self.senario_change(GameMachine.game_mode)

                self.remove_terminated()

                events = pygame.event.get()
                pressed = pygame.key.get_pressed()

                for event in events:
                    self.process_events(event)

                for go in GameObjectKeeper.runables():
                    for event in events:
                        go.process_events(event)
                    go.process_keys(pressed)

                self.collision_detection()

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

    def collision_detection(self):
        for enemy in GameObjectKeeper.enemies():
            for friend in GameObjectKeeper.friendlies():
                if enemy.collide(friend):
                    self.collide_action(friend, enemy)
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

    def collide_action(self, friend, enemy):
        """ TODO: really don't like this routine here.  """

        log.debug("COLLIDED: {0} {1}".format(type(friend),type(enemy)))
        Thump()

        friend.terminate()
        enemy.terminate()

        explosion = AutoMovingAnimatedSprite(
            enemy.x, enemy.y, 
            invaderutils.explosion_png(), 
            movex=0, movey=-1, msteps=1)
        GameObjectKeeper.setup(explosion, 35)
        
        # add to score 
        myscoreboard = GameObjectKeeper.get_by_name("myscoreboard")
        myscoreboard.addscore(5)
        self.highscorestore.set_highscore(myscoreboard.getscore())


    def senario_change(self, game_state):
        wave_func = self.transitions.get_wave(game_state)

        if ( wave_func is not None ):
            wave_func()

    def wave_0(self):
        # Setup Banners for User
        
        banner = Banner("SCORE", GameBase.get_font_normal(), color=invaderutils.COLOR_WHITE, pos=(0, 10))
        GameObjectKeeper.setup(banner, 1000)

        myscoreboard = Score( 0, 35, GameBase.get_font_normal(), invaderutils.COLOR_YELLOW)
        GameObjectKeeper.setup(myscoreboard, 1000, name = "myscoreboard")

        banner = Banner("HIGH SCORE", GameBase.get_font_normal(), color=invaderutils.COLOR_WHITE, pos=(300, 10))
        GameObjectKeeper.setup(banner, 1000)

        banner = Banner("{0:010}".format(GameMachine.highscorestore.get_highscore()), 
        GameBase.get_font_normal(),  pos=(300, 35), color=invaderutils.COLOR_YELLOW)
        GameObjectKeeper.setup(banner, 1000)

        GameMachine.highscorestore.get_highscore()

        # Setup bad guys

        for x in range( 0, 800, 100):
            enemy = Enemy(x, 25, invaderutils.invader_png(4), bombclockpts=(100,250), lowermove=30, movex=-3)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = Enemy(x-55, 100, invaderutils.invader_png(2), bombclockpts=(1500,3000), lowermove=40)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = Enemy(x, 175, invaderutils.invader_png(1), bombclockpts=(1000,2000), lowermove=60,movex=-2)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = Enemy(x+25, 250, invaderutils.invader_png(3), bombclockpts=(1000,4000), lowermove=80)
            GameObjectKeeper.setupenemy(enemy, 50)

        # setup hero

        GameObjectKeeper.setupfriendly(Hero(100, 710, invaderutils.hero_png(), steps=5, move_steps=2), 50)
