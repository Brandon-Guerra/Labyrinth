import pygame
from pygame.locals import *
from LevelGenerator import LevelGenerator
from Maze import Maze

def main():
	# Initialize screen
	pygame.init()
	screen = pygame.display.set_mode((1054, 714))
	pygame.display.set_caption('Labyrinth')

	#initializing constants for drawing maze
	black = (0, 0, 0)
	thickness = 4
	length = 30
	width = 30
	none = 0

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	#Draw rectangle
	pygame.draw.rect(background, black, (50, 50, 100, 0), thickness)
	pygame.draw.rect(background, black, (50, 50, 0, 100), thickness)

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()

	l = LevelGenerator()
	m = l.nextLevel()

	drawCell(m.cell[0][0])

	def drawCell(cell):
		if cell.north == True:
			pygame.draw.rect(background, black, (length, none, 30, 60))
		if cell.south == True:


	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		pygame.display.flip()


if __name__ == '__main__': main()