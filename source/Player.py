import pygame
import math
from Entity import Entity
from Line import Line
from pygame.locals import *
from config import *
from ImageLoader import ImageLoader

class Player(Entity):
	def __init__(self):
		Entity.__init__(self, (0, 0), (0, 0), 25, True, GREEN)
		self.line = Line(self.posXY)
		self.health = 5
		self.accXY = (0, 0)
		self.invincibility = 0
		self.invincible = False
		self.colours = (RED, BLACK, self.colour)
		self.colourTimer = 0
		self.maxVelocity = 15
		self.legImage = ImageLoader.IMAGES['KNIGHT']['FRONT']['WALK'][0]
		self.bodyImage = ImageLoader.IMAGES['KNIGHT']['FRONT']['IDLE']
		self.swordImage = ImageLoader.IMAGES['KNIGHT']['SWORD']
		self.animationCounter = 0
		self.animationFlags = [False, False]
		return
		
	def update(self, keyPressed, mouseXY, mousePressed, terrain):
		self.updateAccXY(keyPressed)
		self.updateVelXY()
		self.velXY = self.checkPassable(terrain)
		self.move()
		self.updateLine(mouseXY, mousePressed)

		if self.invincible:
			self.invincibility -= 1
			self.invincible = self.invincibility > 0				#this line can be commented out for god mode
		return
		
	def updateAccXY(self, keyPressed):
		goLeft = (self.velXY[0] > 0 and (keyPressed[pygame.K_d] == keyPressed[pygame.K_a])) or (not keyPressed[pygame.K_d] and keyPressed[pygame.K_a])
		goRight = (self.velXY[0] < 0 and (keyPressed[pygame.K_a] == keyPressed[pygame.K_d])) or (not keyPressed[pygame.K_a] and keyPressed[pygame.K_d])
		goUp = (self.velXY[1] > 0 and (keyPressed[pygame.K_w] == keyPressed[pygame.K_s])) or (not keyPressed[pygame.K_s] and keyPressed[pygame.K_w])
		goDown = (self.velXY[1] < 0 and (keyPressed[pygame.K_s] == keyPressed[pygame.K_w])) or (not keyPressed[pygame.K_w] and keyPressed[pygame.K_s])
		
		self.accXY = ((goRight - goLeft) * 2, (goDown - goUp) * 2)
		return

	def updateVelXY(self):
		if self.velXY[0] + self.accXY[0] < self.maxVelocity and self.velXY[0] + self.accXY[0] > -self.maxVelocity:
			self.velXY = (self.velXY[0] + self.accXY[0], self.velXY[1])
		if self.velXY[1] + self.accXY[1] < self.maxVelocity and self.velXY[1] + self.accXY[1] > -self.maxVelocity:
			self.velXY = (self.velXY[0], self.velXY[1] + self.accXY[1])
		return

	def updateLine(self, mouseXY, mousePressed):
		if self.line.active:
			self.line.update(self.posXY)
		else:
			if mousePressed[0]:
				self.line.activate(int(math.degrees(math.atan2(mouseXY[1] - WINDOWDIMS[1] // 2, mouseXY[0] - WINDOWDIMS[0] // 2))), INVERTMOUSEBUTTONS * 1)
			if mousePressed[2]:
				self.line.activate(int(math.degrees(math.atan2(mouseXY[1] - WINDOWDIMS[1] // 2, mouseXY[0] - WINDOWDIMS[0] // 2))), INVERTMOUSEBUTTONS * -1)
		return
		
	def damage(self):
		self.health -= 1
		self.invincibility = 2 * FRAMERATE
		self.invincible = True
		return
		
	def draw(self, surface, cameraPos):
		self.updateImages()
		"""
		if self.invincibility:
			self.colourTimer += 1
			if self.colourTimer == 15:
				self.colourTimer = 0
			elif self.colourTimer < 5:
				self.colour = self.colours[0]
			elif self.colourTimer < 10:
				self.colour = self.colours[1]
			else:
				self.colour = self.colours[2]
		"""
		#super().draw(surface, cameraPos)
		
		self.colourTimer += 1
		if self.colourTimer == 8:
			self.colourTimer = 0
		if not (self.invincible and self.colourTimer >= 4):
			if self.animationFlags[1] and self.line.active:
				self.swordImage = pygame.transform.rotate(ImageLoader.IMAGES['KNIGHT']['SWORD'], -self.line.currentAngle)
				surface.blit(self.swordImage, self.swordImage.get_rect(center = (self.posXY[0] + cameraPos[0], self.posXY[1] + cameraPos[1])))
				#self.line.draw(surface, cameraPos)
			surface.blit(self.legImage, (self.posXY[0] - 40 + cameraPos[0], self.posXY[1] + 10 + cameraPos[1]))
			surface.blit(self.bodyImage, (self.posXY[0] - 40 + cameraPos[0], self.posXY[1] - 86 + cameraPos[1]))
			if (not self.animationFlags[1]) and self.line.active:
				self.swordImage = pygame.transform.rotate(ImageLoader.IMAGES['KNIGHT']['SWORD'], -self.line.currentAngle)
				surface.blit(self.swordImage, self.swordImage.get_rect(center = (self.posXY[0] + cameraPos[0], self.posXY[1] + cameraPos[1])))
				#self.line.draw(surface, cameraPos)
				
		return

	def updateImages(self):
		if self.line.active:
			pose = 'SWING'
		else:
			pose = 'IDLE'
		if (self.line.currentAngle > 180 and self.line.active) or self.velXY[1] < 0:
			self.animationFlags[1] = True
			bodySide = 'BACK'
		else:
			self.animationFlags[1] = False
			bodySide = 'FRONT'
		self.bodyImage = ImageLoader.IMAGES['KNIGHT'][bodySide][pose]
	
		flip = False
		if self.velXY == (0, 0):
			self.animationCounter = 0
			self.legImage = ImageLoader.IMAGES['KNIGHT']['FRONT']['WALK'][0]
		else:
			if self.velXY[1] >= 0:
				side = 'FRONT'
				if self.velXY[0] < 0:
					flip = True
			else:
				side = 'BACK'
				if self.velXY[0] > 0:
					flip = True
			
			self.animationCounter += -2 * (not self.animationFlags[0]) + 1
			
			if abs(self.animationCounter) >= 14:
				self.animationFlags[0] = not self.animationFlags[0]
			
			self.legImage = pygame.transform.flip(ImageLoader.IMAGES['KNIGHT'][side]['WALK'][abs(self.animationCounter) // 3 + 1], flip, False)
		return