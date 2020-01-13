import pygame
import random
import math
from DirectionalEntity import DirectionalEntity
from config import *
from ImageLoader import ImageLoader

class Projectile(DirectionalEntity):
	def __init__(self, p, d):
		DirectionalEntity.__init__(self, p, 15, d, 10, True, DORANGE)
		self.collisionCoolDown = FRAMERATE
		self.hitByPlayer = False
		self.updateVelXY()
		self.image = pygame.transform.rotate(ImageLoader.IMAGES['FIREBALL'], -self.direction)
		return
		
	def update(self, player, terrain, score):
		if self.checkBorder(terrain):
			self.exist = False
			
		if self.collideWithLine(player.line.segment) and self.collisionCoolDown > FRAMERATE:
			score += 10
			self.hitByPlayer = True
			self.direction = 2 * player.line.currentAngle - self.direction
			self.direction = self.cleanAngle(self.direction)
			
			if self.direction >= self.cleanAngle(player.line.currentAngle + 120) and self.direction <= self.cleanAngle(player.line.currentAngle + 180):
				self.direction = self.cleanAngle(player.line.currentAngle + 120)
				
			elif self.direction <= self.cleanAngle(player.line.currentAngle + 240) and self.direction >= self.cleanAngle(player.line.currentAngle + 180):
				self.direction = self.cleanAngle(player.line.currentAngle + 240)
				
			self.image = pygame.transform.rotate(ImageLoader.IMAGES['FIREBALL'], -self.direction)
			self.updateVelXY()
			self.collisionCoolDown = 0
		else:
			self.collisionCoolDown += 1
		
		if self.collideWithCircle(player) and not player.invincible:
			self.exist = False
			player.damage()
			
		self.move()
		
		return score
		
	def draw(self, surface, cameraPos):
		surface.blit(self.image, self.image.get_rect(center = (self.posXY[0] + cameraPos[0], self.posXY[1] + cameraPos[1])))