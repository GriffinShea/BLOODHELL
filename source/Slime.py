import pygame
from config import *
from DirectionalEntity import DirectionalEntity
from ImageLoader import ImageLoader

class Slime(DirectionalEntity):

	def __init__(self, p):
		DirectionalEntity.__init__(self, p, 5, 0, 30, True, GREEN)
		self.hitCountDown = 0
		self.health = 3
		self.animationTimer = 0
		return
		
	def update(self, player, terrain, score):
		if abs(self.posXY[0] - player.posXY[0])**2 + abs(self.posXY[1] - player.posXY[1])**2 < 300**2 or self.hitCountDown != 0:
			self.animationTimer += 1
			if self.animationTimer > 19:
				self.animationTimer = 0
			if self.collideWithLine(player.line.segment) and self.hitCountDown == 0:
				score += 50
				self.health -= 1
				self.hitCountDown = 30
			if self.hitCountDown > 0:
				self.hitCountDown -= 1
			if self.collideWithCircle(player):
				self.hitCountDown = 30
				if not player.invincible:
					player.damage()
			self.direction = int(math.degrees(math.atan2(self.posXY[1] - player.posXY[1], self.posXY[0] - player.posXY[0]))) - 180 * (self.hitCountDown == 0)
			self.updateVelXY()
			self.velXY = self.checkPassable(terrain)
			self.move()
			if not (self.health != 0 or self.hitCountDown != 0):
				self.exist = False
				score += 100
		return score
		
	def draw(self, surface, cameraPos):
		surface.blit(pygame.transform.flip(ImageLoader.IMAGES['SLIME'][self.animationTimer // 5], self.velXY[0] > 0, False), (self.posXY[0] - 45 + cameraPos[0], self.posXY[1] - 45 + cameraPos[1]))
		return