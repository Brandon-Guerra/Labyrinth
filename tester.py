import pygame
from pygame.locals import *
from Player import Player

def main():
	player = Player()
	pygame.init()
	for event in pygame.event.get():
		if event.type == QUIT:
			return
		elif event.type == KEYDOWN:
			if event.key == K_UP:
				player.moveup()
			if event.key == K_DOWN:
				player.movedown()
		elif event.type == KEYUP:
			if event.key == K_UP or event.key == K_DOWN:
				player.movepos = [0,0]
				player.state = "still"

if __name__ == '__main__': main()