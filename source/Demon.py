import math
import random
from Projectile import Projectile
from DirectionalEntity import DirectionalEntity
from config import *
from ImageLoader import ImageLoader

class Demon(DirectionalEntity):
	def __init__(self, p):
		DirectionalEntity.__init__(self, p, 5, 0, 20, True, DRED)
		self.coolDown = random.randint(0, FRAMERATE * 2)
		return
	
	def update(self, player, fireballs, terrain, score):
		if abs(self.posXY[0] - player.posXY[0])**2 + abs(self.posXY[1] - player.posXY[1])**2 < 300**2:
			self.run(player, terrain)
		elif abs(self.posXY[0] - player.posXY[0])**2 + abs(self.posXY[1] - player.posXY[1])**2 < 900**2:
			fireballs = self.shoot(player, fireballs)
		
		if self.collideWithLine(player.line.segment):
			self.exist = False
			score += 200
		for fireball in fireballs:
			if fireball.hitByPlayer:
				if self.collideWithCircle(fireball):
					self.exist = False
					score += 600
		return fireballs, score
		
	def run(self, player, terrain):
		self.direction = self.directionToPoint(player.posXY) + 180
		self.updateVelXY()
		self.velXY = self.checkPassable(terrain)
		self.move()
		return
	
	def shoot(self, player, fireballs):
		if self.coolDown > FRAMERATE * 2:
			self.coolDown = 0
			fireballs.append(Projectile(self.posXY, self.directionToPoint(player.posXY)))		
		self.coolDown += 2
		return fireballs
	
	def directionToPoint(self, posXY):
		return int(math.degrees(math.atan2(self.posXY[1] - posXY[1], self.posXY[0] - posXY[0]))) - 180
		
	def draw(self, surface, cameraPos):
		surface.blit(ImageLoader.IMAGES['DEMON'][(self.coolDown) // 12], (self.posXY[0] - 22 + cameraPos[0], self.posXY[1] - 27 + cameraPos[1]))