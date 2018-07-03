from invaderutils import *
import pytest

from gamekeeper import GameObjectKeeper as GOK, GameBase

class tfont(object):
    
    def render(self, x, y,z ):
        print("Called render with: {0} {1} {2}".format(x,y,z))
        return {'render': (x,y,z)}

class tscreen(object):
    line : list = []

    def blit(self, x, y):
        print("Called blit with: {0} {1}".format(x,y))
        tscreen.line.append(x['render'][0])

class Test_Score(object):

    def test_Draw(self):
        s = Score( 0,0, tfont(),score=54321)
        screen = tscreen() 
        s.draw(screen)
        assert ['0','0','0','0','0','5','4','3','2','1'] == tscreen.line


class Test_terminate(object):

    def test_friend_terminate(self):
        GOK.OBJECT_LIST = []

        hero = Hero(300,500,96,96,[])
        GOK.setupfriendly(hero, 50)

        GOK.remove(hero)
        assert GOK.runables() == []

    def test_friend_missile_terminate(self):
        GOK.OBJECT_LIST = []

        missile = AutoMovingAnimatedSprite(0,0, 20, 50, [], movex=0, movey=-4, msteps=1)
        GOK.setupfriendly(missile, 45)

        GOK.remove(missile)
        assert GOK.runables() == []



    

