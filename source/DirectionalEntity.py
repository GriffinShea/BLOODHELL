from config import *
from Entity import Entity

class DirectionalEntity(Entity):
	def __init__(self, p, v, d, r, e, c):
		Entity.__init__(self, p, (0, 0), r, e, c)
		self.direction = d
		self.velocity = v
		return
		
	def updateVelXY(self):
		self.velXY = (int(math.cos(math.radians(self.direction)) * self.velocity), int(math.sin(math.radians(self.direction)) * self.velocity))
		return
		
	def cleanAngle(self, angle):
		while angle < 0:
			angle = angle + 360
		while angle >= 360:
			angle = angle - 360
			
		return angle