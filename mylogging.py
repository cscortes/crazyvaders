import logbook as LB
import sys 

LB.FileHandler("invaders.log").push_application()
log = LB.Logger("invaders")
