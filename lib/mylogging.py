import logbook as LB

LB.FileHandler(".crazyinvaders.log").push_application()
log = LB.Logger("invaders")

