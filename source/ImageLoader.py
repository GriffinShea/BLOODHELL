import pygame

class ImageLoader:
	IMAGES = {}

	@classmethod
	def loadImages(cls):
		cls.IMAGES['HEARTUI'] = pygame.image.load("assets//heart_UI.png").convert()
		cls.IMAGES['HEART'] = pygame.image.load("assets//heart.png").convert()
		cls.IMAGES['HEART'].set_colorkey((255, 255, 255))
		
		cls.IMAGES['FIREBALL'] = pygame.image.load("assets//fireball.png").convert()
		cls.IMAGES['FIREBALL'].set_colorkey((255, 255, 255))
		
		cls.IMAGES['KNIGHT'] = {'FRONT': {'WALK': []}, 'BACK': {'WALK': []}}
		cls.IMAGES['KNIGHT']['FRONT']['IDLE'] = pygame.image.load("assets//knight_front_idle.png").convert()
		cls.IMAGES['KNIGHT']['FRONT']['IDLE'].set_colorkey((255, 255, 255))
		cls.IMAGES['KNIGHT']['FRONT']['SWING'] = pygame.image.load("assets//knight_front_swing.png").convert()
		cls.IMAGES['KNIGHT']['FRONT']['SWING'].set_colorkey((255, 255, 255))
		cls.IMAGES['KNIGHT']['BACK']['IDLE'] = pygame.image.load("assets//knight_back_idle.png").convert()
		cls.IMAGES['KNIGHT']['BACK']['IDLE'].set_colorkey((255, 255, 255))
		cls.IMAGES['KNIGHT']['BACK']['SWING'] = pygame.image.load("assets//knight_back_swing.png").convert()
		cls.IMAGES['KNIGHT']['BACK']['SWING'].set_colorkey((255, 255, 255))
		
		for side in cls.IMAGES['KNIGHT']:
			for i in range(6):
				cls.IMAGES['KNIGHT'][side]['WALK'].append(pygame.image.load("assets//knight_" + side.lower() + "_" + str(i) + ".png").convert())
				cls.IMAGES['KNIGHT'][side]['WALK'][i].set_colorkey((255, 255, 255))
		
		cls.IMAGES['KNIGHT']['SWORD'] = pygame.image.load("assets//sword.png").convert()
		cls.IMAGES['KNIGHT']['SWORD'].set_colorkey((255, 255, 255))
		
		cls.IMAGES['DEMON'] = []
		for i in range(6):
			cls.IMAGES['DEMON'].append(pygame.image.load("assets//demon_" + str(i) + ".png").convert())
			cls.IMAGES['DEMON'][i].set_colorkey((255, 255, 255))
		
		cls.IMAGES['SLIME'] = []
		for i in range(4):
			cls.IMAGES['SLIME'].append(pygame.image.load("assets//slime_" + str(i) + ".png").convert())
			cls.IMAGES['SLIME'][i].set_colorkey((255, 255, 255))
		return
