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
	width = 34
	height = 34
	none = 0
	offset = 30
	constant = 34

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()

	def drawMaze(maze):
		"""
	  View a maze
	  """
	  # initialize north and west
		for i in range(maze.width):
			if maze.cell[i,0].north:
				drawWall(True,i,0)
		for i in range(maze.height):
			if maze.cell[0,i].west:
				drawWall(False,0,i)
	  # loop through to draw the rest of the walls
		for i in range(maze.width):
			for j in range(maze.height):
				if maze.cell[i,j].south:
					drawWall(True,i,j+1)
				if maze.cell[i,j].east:
					drawWall(False,i+1,j)

	def drawWall(isHorizontal, x, y):
		"""
		Draw wall for a cell
		"""
		if isHorizontal:
			pygame.draw.rect(background, black, (x*constant + offset, y*constant + offset, width, none), thickness)
		else:
			pygame.draw.rect(background, black, (x*constant + offset, y*constant + offset, none, height), thickness)

	l = LevelGenerator()
	m = l.nextLevel()
	drawMaze(m)

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		pygame.display.flip()

if __name__ == '__main__': main()