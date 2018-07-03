import pytest

from gamekeeper import GameObjectKeeper as GOK, GameBase

class MockObject(GameBase):
    ID = 1

    def __init__(self, title = None):
        if (title is None):
            self.title = "MOCK {0}".format(MockObject.ID)
            MockObject.ID += 1
        else:
            self.title = title


    def __repr__(self):
        return "%s" % self.title


class Test_GameKeeper(object):


    def test_setup_and_remove(self):
        GOK.OBJECT_LIST = []

        ob = MockObject() 
        GOK.setup( ob, 1, False, False)

        assert GOK.runables() != []
        GOK.remove(ob)

        assert GOK.runables() == []

    def test_setupfriend(self):
        GOK.OBJECT_LIST = []

        ob = MockObject() 
        GOK.setupfriendly( ob, 1 )

        assert GOK.friendlies() != []

    def test_setupenemy(self):
        GOK.OBJECT_LIST = []

        ob = GameBase() 
        GOK.setupenemy( ob, 1 )
        res = GOK.enemies()

        assert GOK.enemies() != []

    def test_remove3(self):
        GOK.OBJECT_LIST = []

        ob1 = MockObject("game 1") 
        ob2 = MockObject("game 2") 
        ob3 = MockObject("game 3") 
        GOK.setup(ob1, 1, False, False)
        GOK.setupfriendly(ob2, 1)
        GOK.setupenemy(ob3, 1)
        assert GOK.runables() != []
        print(GOK.runables())

        GOK.remove(ob1)
        assert GOK.runables() != []

        GOK.remove(ob2)
        assert GOK.runables() != []

        GOK.remove(ob3)
        print(GOK.runables())
        assert GOK.runables() == []

