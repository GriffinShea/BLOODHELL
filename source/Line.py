import pygame
import math

class Line:
	def __init__(self, o):
		self.originXY = o
		self.length = 100
		self.segment = (((0,0),(0,0)), ((0,0),(0,0)))
		self.active = False
		self.maxAngle = 0
		self.currentAngle = 0
		self.direction = 0
		return
		
	def update(self, o):
		self.originXY = o
		self.currentAngle += self.direction * 8
		while self.currentAngle < 0:
			self.currentAngle = self.currentAngle + 360
			self.maxAngle = self.maxAngle + 360
		while self.currentAngle >= 360:
			self.currentAngle = self.currentAngle - 360
			self.maxAngle = self.maxAngle - 360
		if (self.currentAngle > self.maxAngle and self.direction == 1) or (self.currentAngle < self.maxAngle and self.direction == -1):
			self.active = False
			self.segment = (((0,0),(0,0)), ((0,0),(0,0)))
			return

		# ...and the end of the line...
		eol_x0 = self.originXY[0] + math.cos(math.radians(self.currentAngle-5)) * self.length
		eol_y0 = self.originXY[1] + math.sin(math.radians(self.currentAngle-5)) * self.length
		
		# ...and the end of the line...
		eol_x1 = self.originXY[0] + math.cos(math.radians(self.currentAngle+5)) * self.length
		eol_y1 = self.originXY[1] + math.sin(math.radians(self.currentAngle+5)) * self.length
		
		# ...and then add that line to the list
		self.segment =  ((self.originXY, (eol_x0, eol_y0)), (self.originXY, (eol_x1, eol_y1)))
		return

	def draw(self, surface, cameraPos):
		pygame.draw.aaline(surface, (255, 255, 255), (self.segment[0][0][0] + cameraPos[0], self.segment[0][0][1] + cameraPos[1]), (self.segment[0][1][0] + cameraPos[0], self.segment[0][1][1] + cameraPos[1]))
		pygame.draw.aaline(surface, (255, 255, 255), (self.segment[1][0][0] + cameraPos[0], self.segment[1][0][1] + cameraPos[1]), (self.segment[1][1][0] + cameraPos[0], self.segment[1][1][1] + cameraPos[1]))
		return
		
	def activate(self, angle, d):
		self.direction = d
		self.maxAngle = angle + self.direction * 45
		self.currentAngle = angle - self.direction * 45
		self.active = True
		return