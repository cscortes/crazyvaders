import pygame

from lib import invaderutils
from lib.AnimatedSprite import AnimatedSprite
from lib.AutoMovingAnimatedSprite import AutoMovingAnimatedSprite
from lib.Background import Background
from lib.Banner import Banner
from lib.Enemy import *
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
    _game_mode = None
    transitions = Transitions()
    highscorestore = HighscoreStore()

    def __init__(self, width, height):
        invaderutils.set_game_dimensions(width, height)
        GameMachine.clock =  pygame.time.Clock()
        GameObjectKeeper.special_setup(Background(), 0)

    def set_game_mode(self, new_mode):
        log.debug("Game mode changed to {}".format(new_mode))
        self._game_mode = new_mode

    def get_game_mode(self):
        return self._game_mode

    def teardown(self):
        GameMachine.highscorestore.update()

    def setup(self):
        self.transitions.add(invaderutils.GAME_STARTED_EVENT, invaderutils.GAME_STARTED_EVENT, 0, self.wave_loading_1)
        self.transitions.add(invaderutils.GAME_STARTED_EVENT, invaderutils.GAME_WAVE_1_EVENT, 2, self.wave_1)
        self.transitions.add(invaderutils.GAME_WAVE_1_EVENT, invaderutils.MODE_FIGHT_1_EVENT, 0, self.wave_fight)

        # self.transitions.add(invaderutils.GAME_STARTED_EVENT, invaderutils.GAME_STARTED_EVENT, 0, self.wave_loading_1)
        # self.transitions.add(invaderutils.GAME_STARTED_EVENT, invaderutils.GAME_WAVE_1_EVENT, 2, self.wave_1)

        self.transitions.add(invaderutils.MODE_FIGHT_1_EVENT, invaderutils.GAME_ENEMIES_DEAD_EVENT, 2, self.wave_loading_2)
        self.transitions.add(invaderutils.GAME_ENEMIES_DEAD_EVENT, invaderutils.GAME_WAVE_2_EVENT, 2, self.wave_2)
        self.transitions.add(invaderutils.GAME_WAVE_2_EVENT, invaderutils.MODE_FIGHT_2_EVENT, 0, self.wave_fight)

        self.transitions.add(invaderutils.MODE_FIGHT_2_EVENT, invaderutils.GAME_ENEMIES_DEAD_EVENT, 2, self.wave_loading_3)
        self.transitions.add(invaderutils.GAME_ENEMIES_DEAD_EVENT, invaderutils.GAME_WAVE_3_EVENT, 2, self.wave_3)
        self.transitions.add(invaderutils.GAME_WAVE_3_EVENT, invaderutils.MODE_FIGHT_3_EVENT, 0, self.wave_fight)

        self.transitions.add(invaderutils.MODE_FIGHT_3_EVENT, invaderutils.GAME_ENEMIES_DEAD_EVENT, 2, self.wave_loading_4)
        self.transitions.add(invaderutils.GAME_ENEMIES_DEAD_EVENT, invaderutils.GAME_WAVE_4_EVENT, 2, self.wave_4)
        self.transitions.add(invaderutils.GAME_WAVE_4_EVENT, invaderutils.MODE_FIGHT_4_EVENT, 0, self.wave_fight)

        self.transitions.add(invaderutils.MODE_FIGHT_4_EVENT, invaderutils.GAME_ENEMIES_DEAD_EVENT, 2, self.wave_loading_5)
        self.transitions.add(invaderutils.GAME_ENEMIES_DEAD_EVENT, invaderutils.GAME_WAVE_5_EVENT, 2, self.wave_5)
        self.transitions.add(invaderutils.GAME_WAVE_5_EVENT, invaderutils.MODE_FIGHT_5_EVENT, 0, self.wave_fight)

        self.transitions.add(invaderutils.MODE_FIGHT_5_EVENT, invaderutils.GAME_ENEMIES_DEAD_EVENT, 2, self.wave_winner)
        self.transitions.add(invaderutils.GAME_ENEMIES_DEAD_EVENT, invaderutils.GAME_END_EVENT, 10, self.wave_quit)

        self.transitions.add(None, invaderutils.HERO_KILLED_EVENT, 4, self.setup_loser_screen)
        self.transitions.add(invaderutils.HERO_KILLED_EVENT, invaderutils.GAME_END_EVENT, 4, self.wave_quit)


    def run(self):
        self.set_game_mode(invaderutils.GAME_STARTED_EVENT)

        try:
            while True:
                self.senario_change()
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
        curr_state = self.get_game_mode()

        # Check to see if we are in FIGHT MODE
        if not ((curr_state > invaderutils.MODE_FIGHT_A_EVENT) and (curr_state < invaderutils.MODE_FIGHT_Z_EVENT)):
            return 

        enemies = GameObjectKeeper.enemies()

        if len(enemies) == 0:
            self.set_game_mode(invaderutils.GAME_ENEMIES_DEAD_EVENT)
            return
        
        for enemy in enemies:
            for friend in GameObjectKeeper.friendlies():
                if enemy.collide(friend):
                    self.collide_action(friend, enemy)
                    self.check_friend_hero(friend)
        

    def check_friend_hero(self, friend):
        if isinstance(friend, Hero):
            # example of firing off  an event
            # ev = pygame.event.Event(invaderutils.HERO_KILLED_EVENT, {'message': "Hero is dead!"})
            # pygame.event.post(ev)
            if friend.removeme():
                self.set_game_mode(invaderutils.HERO_KILLED_EVENT)

    def process_events(self, evt):
        if evt.type == invaderutils.GAME_END_EVENT:
            log.info("Bye!")
            self.set_game_mode(invaderutils.GAME_END_EVENT)


    def collide_action(self, friend, enemy):
        """ TODO: really don't like this routine here.  """
        log.debug("COLLIDED: {0} {1}".format(type(friend),type(enemy)))
        Thump()

        friend.terminate()
        enemy.terminate()

        explosion = AutoMovingAnimatedSprite(enemy.x, enemy.y,invaderutils.explosion_png(), movex=0, movey=-1, msteps=1)
        if (isinstance(friend, Hero)):
            explosion = AutoMovingAnimatedSprite(friend.x, friend.y, invaderutils.hero_explosion_png(), movex=0, movey=-1, msteps=1)
        elif (not isinstance(enemy, Enemy)):
            explosion = AutoMovingAnimatedSprite(enemy.x, enemy.y, invaderutils.missile_explosion_png(), movex=0, movey=-1, msteps=1)

        GameObjectKeeper.setup(explosion, 35)
        
        # add to score 
        if (not isinstance(friend, Hero)):
            myscoreboard = GameObjectKeeper.get_by_name("myscoreboard")
            myscoreboard.addscore(enemy.get_bonus())
            self.highscorestore.set_highscore(myscoreboard.getscore())

    def senario_change(self):
        answer = self.transitions.get_wave(self.get_game_mode())

        if ( answer is not None ):
            (wave_func, param1) = answer
            wave_func(param1)

    def setup_loser_screen(self, parm1):
        self.clear_all_objects()

        bye = AnimatedSprite(200, 320, ["images/game/gameover.png"])
        GameObjectKeeper.setupenemy(bye, 1000)
                
        self.set_game_mode(invaderutils.GAME_END_EVENT)

    def _wave_basics(self):
        self.clear_all_objects()

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

        # setup hero
        GameObjectKeeper.setupfriendly(Hero(100, 710, invaderutils.hero_png(), mis_steps=75, steps=3, move_steps=2), 50)

    def wave_1(self, param):
        log.info("Starting Wave 1")
        self._wave_basics()

        # Setup bad guys
        for x in range( 0, 400, 150):

            enemy = enemy_little_john(x, 50)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_little_john(x+125, 150)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_little_john(x, 250)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_little_john(x+125, 350)
            GameObjectKeeper.setupenemy(enemy, 50)

        self.set_game_mode(invaderutils.MODE_FIGHT_1_EVENT)

    def wave_2(self, param):
        log.info("Starting Wave 2")
        self._wave_basics()

        # Setup bad guys
        for x in range( 0, 750, 75):
            enemy = enemy_fonzy(x, 70, movex=-2)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_fonzy(x, 120, movex=-2)
            GameObjectKeeper.setupenemy(enemy, 50)

        self.set_game_mode(invaderutils.MODE_FIGHT_2_EVENT)

    def wave_3(self, param):
        log.info("Starting Wave 3")
        self._wave_basics()

        # Setup bad guys
        for x in range( 0, 400, 100):

            enemy = enemy_the_frig(x,70,movex=1)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_the_frig(x + 300, 140, movex=-1)
            GameObjectKeeper.setupenemy(enemy, 50)

        self.set_game_mode(invaderutils.MODE_FIGHT_3_EVENT)

    def wave_4(self, param):
        log.info("Starting Wave 4")
        self._wave_basics()

        # Setup bad guys
        for x in range( 0, 720, 75):
            enemy = enemy_smiling_vader(x,70,movex=-3)
            GameObjectKeeper.setupenemy(enemy, 50)

        self.set_game_mode(invaderutils.MODE_FIGHT_4_EVENT)

    def wave_5(self, param):
        log.info("Starting Wave 5")
        self._wave_basics()

        # Setup bad guys
        for x in range( 0, 400, 100):
    
            enemy = enemy_the_frig(x,70,movex=1)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_the_frig(x + 300, 140, movex=-1)
            GameObjectKeeper.setupenemy(enemy, 50)

        for x in range( 0, 720, 75):
            enemy = enemy_smiling_vader(x,70,movex=-3)
            GameObjectKeeper.setupenemy(enemy, 50)

        for x in range( 0, 750, 75):
            enemy = enemy_fonzy(x, 70, movex=-2)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_fonzy(x, 120, movex=-2)
            GameObjectKeeper.setupenemy(enemy, 50)


        for x in range( 0, 400, 150):
    
            enemy = enemy_little_john(x, 50)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_little_john(x+125, 150)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_little_john(x, 250)
            GameObjectKeeper.setupenemy(enemy, 50)

            enemy = enemy_little_john(x+125, 350)
            GameObjectKeeper.setupenemy(enemy, 50)


            # enemy = Enemy(x, 25, invaderutils.invader_png(4), bombclockpts=(100,250), lowermove=30, movex=-3)
            # GameObjectKeeper.setupenemy(enemy, 50)

            # enemy = Enemy(x-55, 100, invaderutils.invader_png(2), bombclockpts=(1500,3000), lowermove=40)
            # GameObjectKeeper.setupenemy(enemy, 50)

            # enemy = Enemy(x, 175, invaderutils.invader_png(1), bombclockpts=(1000,2000), lowermove=60,movex=-2)
            # GameObjectKeeper.setupenemy(enemy, 50)

            # enemy = Enemy(x+25, 275, invaderutils.invader_png(3), bombclockpts=(1000,4000), lowermove=80)
            # GameObjectKeeper.setupenemy(enemy, 50)

        self.set_game_mode(invaderutils.MODE_FIGHT_5_EVENT)

    def wave_loading(self, param1):
        log.info("Starting Wave {} Loading ...".format(param1))
        self.clear_all_objects()

        banner = Banner("Wave {} Loading ...".format(param1), GameBase.get_font_normal(), 
        color=invaderutils.COLOR_WHITE, pos=(250,325))
        GameObjectKeeper.setup(banner, 1000)

    def wave_loading_1(self, param1):
        self.wave_loading(1)
        self.set_game_mode (invaderutils.GAME_WAVE_1_EVENT)
        
    def wave_loading_2(self, param1):
        self.wave_loading(2)
        self.set_game_mode (invaderutils.GAME_WAVE_2_EVENT)

    def wave_loading_3(self, param1):
        self.wave_loading(3)
        self.set_game_mode(invaderutils.GAME_WAVE_3_EVENT)

    def wave_loading_4(self, param1):
        self.wave_loading(4)
        self.set_game_mode(invaderutils.GAME_WAVE_4_EVENT)

    def wave_loading_5(self, param1):
        self.wave_loading(5)
        self.set_game_mode(invaderutils.GAME_WAVE_5_EVENT)

    def wave_fight(self, param1):
        log.info("Fight !")

    def wave_winner(self, parm1):
        log.info("WINNER")
        self.clear_all_objects()

        banner = Banner("Winner!", GameBase.get_font_normal(), 
        color=invaderutils.COLOR_WHITE, pos=(250,325))
        GameObjectKeeper.setup(banner, 1000)
        self.set_game_mode(invaderutils.GAME_END_EVENT)

    def wave_quit(self, param1):
        raise QuitProgram()

    def clear_all_objects(self):
        for go in GameObjectKeeper.runables():
            GameObjectKeeper.remove(go)
