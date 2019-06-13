import random

from lib import invaderutils
from lib.AutoMovingAnimatedSprite import AutoMovingAnimatedSprite
from lib.GameObjectKeeper import GameObjectKeeper
from lib.mylogging import log


class Star(AutoMovingAnimatedSprite):

	def __init__(self, steps=10):
		ix = random.randint(0,invaderutils._GAME_WIDTH)
		iy = random.randint(0,invaderutils._GAME_HEIGHT)
		super().__init__(ix, iy, invaderutils.star_png(), steps)
		self.movex = 0
		self.movey = 2

	def return_star_to_top(self):
		self.y = 0
		self.x = random.randint(0,invaderutils._GAME_WIDTH)

	def clipbottomthandler(self):
		self.return_star_to_top()
