
from mylogging import log 
import configparser


class GameBase(object):
    def __init__(self):
        pass

class ObjectMeta(object):
    def __init__(self, ob : GameBase, level : int, friend : bool, enemy : bool) -> None:
        self.ob = ob
        self.level = level
        self.enemy = enemy
        self.friend = friend

class GameObjectKeeper(object):
    OBJECT_LIST : list = []

    @classmethod
    def special_setup(cls, ob : GameBase, level : int, friend=False, enemy=False) -> None:
        """ used only when level is special, like for the game background """
        log.debug("Setup for: {0}".format(ob))
        cls.OBJECT_LIST.append(ObjectMeta(ob, level, friend, enemy))
        cls.sortobjects()

    @classmethod
    def setup(cls, ob : GameBase, level : int, friend : bool = False, enemy : bool = False) -> None:
        if (level < 1):
            raise ValueError("Object Level is below 1, must be 1 or greater!")
        cls.special_setup(ob,level,friend,enemy)

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

class HighscoreStore(object):
    
    def __init__(self, filename = "invaders.cnf"):
        self.cnf = configparser.ConfigParser()
        self.cnf.read(filename)
        self.filename = filename

    def get_highscore(self):
        return  int(self.cnf["DEFAULT"].get("highscore","-1"))
        
    def set_highscore(self, score):
        log.debug("SCORE {}".format(score))
        if score > self.get_highscore():
            log.debug("HIGH SCORE BEATEN {} => {}".format(self.get_highscore(), score))
            self.cnf.set("DEFAULT","highscore",str(score))

    def update(self):
        with open(self.filename,"w") as f:
            self.cnf.write(f)

