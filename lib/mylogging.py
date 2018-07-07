import logbook as LB
import sys 

#LB.FileHandler(".crazyinvaders.log").push_application()
LB.StreamHandler(sys.stdout).push_application()
log = LB.Logger("invaders")

