from CircleCollider import CircleCollider
from config import *

class Entity(CircleCollider):
	def __init__(self, p, v, r, e, c):
		CircleCollider.__init__(self, p, r, e, c)
		self.velXY = v

	def move(self):
		self.posXY = (self.posXY[0] + self.velXY[0], self.posXY[1] + self.velXY[1])

	def checkSidesBorder(self):
		if self.posXY[0] + self.velXY[0] + self.radius > MAPDIMS[0] or self.posXY[0] + self.velXY[0] - self.radius < 0:
			return True
		else:
			return False
		
	def checkTopBottum(self):
		if self.posXY[1] + self.velXY[1] + self.radius > MAPDIMS[1] or self.posXY[1] + self.velXY[1] - self.radius < 0:
			return True
		else:
			return False

	def checkPassable(self, terrain):
		if terrain.get_at((self.posXY[0] + self.velXY[0] + self.radius, self.posXY[1] + self.velXY[1])) != BLACK or terrain.get_at((self.posXY[0] + self.velXY[0] - self.radius, self.posXY[1] + self.velXY[1])) != BLACK or terrain.get_at((self.posXY[0] + self.velXY[0], self.posXY[1] + self.velXY[1] + self.radius)) != BLACK or terrain.get_at((self.posXY[0] + self.velXY[0], self.posXY[1] + self.velXY[1] - self.radius)) != BLACK:
			self.velXY = (0, 0)
		return self.velXY
			
	def checkBorder(self, terrain):
		if terrain.get_at((self.posXY[0] + self.velXY[0] + self.radius, self.posXY[1] + self.velXY[1])) == WHITE or terrain.get_at((self.posXY[0] + self.velXY[0] - self.radius, self.posXY[1] + self.velXY[1])) == WHITE:
			return True
		elif terrain.get_at((self.posXY[0] + self.velXY[0], self.posXY[1] + self.velXY[1] + self.radius)) == WHITE or terrain.get_at((self.posXY[0] + self.velXY[0], self.posXY[1] + self.velXY[1] - self.radius)) == WHITE:
			return True
		else:
			return False