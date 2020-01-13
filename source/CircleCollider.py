import pygame

class CircleCollider:
	def __init__(self, p, r, e, c):
		self.posXY = p
		self.radius = r
		self.exist = e
		self.colour = c
		return
		
	def draw(self, surface, cameraPos):
		pygame.draw.circle(surface, self.colour, (self.posXY[0] + cameraPos[0], self.posXY[1] + cameraPos[1]), self.radius)
		return
		
	def collideWithLine(self, segments):
		if segments == (((0,0),(0,0)), ((0,0),(0,0))):
			return False
		for seg in segments:
			t = ((self.posXY[0] - seg[0][0]) * (seg[1][0] - seg[0][0]) + (self.posXY[1] - seg[0][1]) * (seg[1][1] - seg[0][1])) / ((seg[1][0] - seg[0][0]) ** 2 + (seg[1][1] - seg[0][1]) ** 2)
			t = max(min(t, 1), 0)
			w_x = seg[0][0] + t * (seg[1][0] - seg[0][0])
			w_y = seg[0][1] + t * (seg[1][1] - seg[0][1])
			d_sqr = (w_x - self.posXY[0]) ** 2 + (w_y - self.posXY[1]) ** 2
			if (d_sqr <= self.radius ** 2):
				return True
			else:
				return False
			
	def collideWithCircle(self, other):
		if (self.posXY[0] - other.posXY[0]) ** 2 + (self.posXY[1] - other.posXY[1]) ** 2 <= (self.radius + other.radius) ** 2:
			return True
		else:
			return False