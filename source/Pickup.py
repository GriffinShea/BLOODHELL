from CircleCollider import CircleCollider
from ImageLoader import ImageLoader
from config import *

class Pickup(CircleCollider):
	def __init__(self, p):
		CircleCollider.__init__(self, p, 20, True, RED)
		
	def update(self, player, score):
		if self.collideWithCircle(player):
			player.health = 5
			self.exist = False
			score += 100
		return score
			
	def draw(self, surface, cameraPos):
		surface.blit(ImageLoader.IMAGES['HEART'], (self.posXY[0] + cameraPos[0] - 25, self.posXY[1] + cameraPos[1] - 25))