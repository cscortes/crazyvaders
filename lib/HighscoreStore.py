import configparser
from lib.mylogging import log

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
