from config import *
from Game import Game

def main():
	game = Game()
	while game.running:
		game.takeInput()
		game.updateGame()
		game.renderGame()
		print("fps:", game.clock.get_fps())
		game.clock.tick(FRAMERATE)

if __name__ == "__main__":
	main()