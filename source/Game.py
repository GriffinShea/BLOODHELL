import pygame
from pygame.locals import *
from config import *
from level_info import *
from Player import Player
from Demon import Demon
from Slime import Slime
from Projectile import Projectile
from Pickup import Pickup
from ImageLoader import ImageLoader

class Game:

	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode(WINDOWDIMS)
		pygame.display.set_caption("BLOODHELL")
		
		self.font = pygame.font.SysFont('Comic Sans MS', 48)
		self.pauseText = self.font.render("Game Paused", False, WHITE)
		
		self.clock = pygame.time.Clock()
		self.states = {'titleScreen': True, 'controlScreen': False, 'gameRunning': False, 'pause': False, 'gameOver': False}
		self.running = True
		
		self.titleScreenImage = pygame.transform.scale(pygame.image.load("assets//title_screen.png").convert(), WINDOWDIMS)
		self.controlScreenImage = pygame.transform.scale(pygame.image.load("assets//control_screen.png").convert(), WINDOWDIMS)
		self.endScreenImage = pygame.transform.scale(pygame.image.load("assets//end_screen.png").convert(), WINDOWDIMS)
		
		self.input = {'closeGame': False}
		
		ImageLoader.loadImages()
		return
		
	def startGame(self):
		self.score = 0
		self.player = Player()
		self.demons = []
		self.slimes = []
		self.hearts = []
		self.fireballs = []
		for demonLocation in DEMONLOCATIONS:
			self.demons.append(Demon(demonLocation))
		for slimeLocation in SLIMELOCATIONS:
			self.slimes.append(Slime(slimeLocation))
		for heartLocation in HEARTLOCATIONS:
			self.hearts.append(Pickup(heartLocation))
		
		self.terrain = pygame.image.load(TERRAIN).convert()
		self.map = pygame.image.load(MAP).convert()
		self.player.posXY = PLAYERLOCATION
		return
		
	def takeInput(self):
		self.input['escapeDown'] = False
		self.input['returnDown'] = False
		for event in pygame.event.get():
			if event.type == QUIT:
				self.input['closeGame'] = True
			if event.type == pygame.KEYDOWN:
				self.input['escapeDown'] = event.key == K_ESCAPE
				self.input['returnDown'] = event.key == K_RETURN
				
		self.input['keyPressed'] = pygame.key.get_pressed()
		self.input['mouseXY'] = pygame.mouse.get_pos()
		self.input['mousePressed'] = pygame.mouse.get_pressed()
		return
		
	def updateGame(self):
		self.running = not self.input['closeGame']
	
		#if state is titlescreen
		if self.states['titleScreen']:
			if self.input['returnDown']:
				self.states['titleScreen'] = False
				self.states['controlScreen'] = True
	
		#if state is controlscreen
		elif self.states['controlScreen']:
			if self.input['returnDown']:
				self.states['controlScreen'] = False
				self.states['gameRunning'] = True
				self.startGame()
		
		#if state is pausescreen
		elif self.states['pause']:
			if self.input['escapeDown']:
				self.states['pause'] = False
				self.states['gameRunning'] = True
			if self.input['keyPressed'][pygame.K_q]:
				self.running = False
				
		#if state is in game
		elif self.states['gameRunning']:
			if self.input['escapeDown']:
				self.states['gameRunning'] = False
				self.states['pause'] = True
			else:
				self.updateEntities()
				self.deleteEntities()
				if self.player.health == 0 or self.player.posXY[1] < 130:
					self.score += self.player.health * 100
					self.player.health = 0
					self.states['gameRunning'] = False
					self.states['gameOver'] = True
					
		elif self.states['gameOver']:
			if self.input['returnDown']:
				self.states['gameOver'] = False
				self.states['controlScreen'] = True
			if self.input['keyPressed'][pygame.K_q]:
				self.running = False
		return
		
	def updateEntities(self):
		self.player.update(self.input['keyPressed'], self.input['mouseXY'], self.input['mousePressed'], self.terrain)
			
		for demon in self.demons:
			self.fireballs, self.score = demon.update(self.player, self.fireballs, self.terrain, self.score)
		for slime in self.slimes:
			self.score = slime.update(self.player, self.terrain, self.score)
		for fireball in self.fireballs:
			self.score = fireball.update(self.player, self.terrain, self.score)
		for heart in self.hearts:
			self.score = heart.update(self.player, self.score)
		return
		
	def deleteEntities(self):
		for i in range(len(self.demons)-1, -1, -1):
			if self.demons[i].exist == False:
				self.demons.pop(i)
		
		for i in range(len(self.slimes)-1, -1, -1):
			if self.slimes[i].exist == False:
				self.slimes.pop(i)
		
		for i in range(len(self.fireballs)-1, -1, -1):
			if self.fireballs[i].exist == False:
				self.fireballs.pop(i)
		
		for i in range(len(self.hearts)-1, -1, -1):
			if self.hearts[i].exist == False:
				self.hearts.pop(i)
		return
		
	def renderGame(self):
		screen = pygame.Surface(WINDOWDIMS)
			
		if self.states['titleScreen']:
			screen.blit(self.titleScreenImage, (0, 0))
			
		elif self.states['controlScreen']:
			screen.blit(self.controlScreenImage, (0, 0))
		
		elif self.states['gameRunning'] or self.states['pause']:
			world = pygame.Surface(WINDOWDIMS)
			cameraPos = (WINDOWDIMS[0] // 2 - self.player.posXY[0], WINDOWDIMS[1] // 2 - self.player.posXY[1])
			world.blit(self.map, (cameraPos, WINDOWDIMS))
			self.player.draw(world, cameraPos)
			for demon in self.demons:
				demon.draw(world, cameraPos)
			for slime in self.slimes:
				slime.draw(world, cameraPos)
			for fireball in self.fireballs:
				fireball.draw(world, cameraPos)
			for heart in self.hearts:
				heart.draw(world, cameraPos)
			screen.blit(world, (0, 0))
			self.renderUI(screen)
			if self.states['pause']:
				screen.blit(self.pauseText, (WINDOWDIMS[1] / 2, 0))
			
		elif self.states['gameOver']:
			screen.blit(self.endScreenImage, (0, 0))
			screen.blit(self.font.render(str(self.score), False, WHITE), (550, 800))
			
		self.window.blit(screen, (0, 0))
		pygame.display.flip()
		return
		
	def renderUI(self, surface):
		for i in range(self.player.health):
			surface.blit(ImageLoader.IMAGES['HEARTUI'], (WINDOWDIMS[0] - 50, WINDOWDIMS[1] - 50 - 50 * i))
		surface.blit(self.font.render("Score: " + str(self.score), False, WHITE), (0, 0))