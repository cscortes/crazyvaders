from lib.GameBase import GameBase
from lib.mylogging import log

class ObjectMeta(object):
    def __init__(self, ob : GameBase, level : int, friend : bool, enemy : bool, name : str) -> None:
        self.ob = ob
        self.level = level
        self.enemy = enemy
        self.friend = friend
        self.name = name

class GameObjectKeeper(object):
    OBJECT_LIST : list = []

    @classmethod
    def special_setup(cls, ob : GameBase, level : int, friend=False, enemy=False, name=None) -> None:
        """ used only when level is special, like for the game background """
        log.debug("Setup for: {0}".format(ob))
        cls.OBJECT_LIST.append(ObjectMeta(ob, level, friend, enemy, name))
        cls.sortobjects()

    @classmethod
    def setup(cls, ob : GameBase, level : int, friend : bool = False, enemy : bool = False, name : str = None) -> None:
        if (level < 1):
            raise ValueError("Object Level is below 1, must be 1 or greater!")
        cls.special_setup(ob, level, friend, enemy, name)

    @classmethod
    def setupfriendly(cls, ob : GameBase , level : int) -> None:
        cls.setup(ob, level, friend=True)

    @classmethod
    def setupenemy(cls, ob : GameBase, level : int) -> None:
        cls.setup(ob, level, enemy=True)

    @classmethod
    def sortobjects(cls) -> None:
        log.info("Sorting Game Stage ...")
        cls.OBJECT_LIST.sort( key=lambda ob: ob.level)

    @classmethod
    def runables(cls) -> list:
        return [ item.ob for item in cls.OBJECT_LIST ]

    @classmethod
    def friendlies(cls)-> list:
        return [ item.ob for item in cls.OBJECT_LIST if item.friend ]
    
    @classmethod
    def enemies(cls)-> list:
        return [ item.ob for item in cls.OBJECT_LIST if item.enemy ]

    @classmethod
    def get_by_name(cls, ob_name):
        for item in cls.OBJECT_LIST: 
            if item.name == ob_name:
                return item.ob
        return None

    @classmethod
    def remove(cls, ob):
        for item in cls.OBJECT_LIST:
            if (item.ob == ob):
                if (item.level < 1):
                    log.debug("Cant remove special items")
                    return 
                cls.OBJECT_LIST.remove(item)
                log.debug("Removing {}".format(item))
                return
        raise ValueError("Item {0} not found in list.".format(ob))
