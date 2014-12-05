import pygame
from pygame.locals import *
from input import Input
from LevelGenerator import LevelGenerator

pygame.init()
WINDOWWIDTH, WINDOWHIEGHT = (1200,800)
screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHIEGHT))
FPSClock = pygame.time.Clock()

def run():
  stateHandler = StateHandler()
  while True:
    stateHandler.update()

class StateHandler:
  def __init__(self):
    pygame.display.set_caption('Labyrinth')
    screen.fill((255, 255, 255))
    pygame.display.update()
    pygame.time.wait(400)
    self.input = Input()
    self.mode = 'menu'
    self.menu = StartMenu()
    FPSClock.tick(60)

  def update(self):
    self.input.get() #check for quit
    if self.mode == 'menu':
      isDone = self.menu.update(self.input)
      if isDone:
        self.mode = 'game'
        self.gameHandler = GameHandler(self.input)
    elif self.mode == 'game':
      result = self.gameHandler.update()
      if result == 'game over':
        self.mode = 'menu'     
    pygame.display.update()

class StartMenu:
  def __init__(self):
    pass

  def update(self, userInput):
    screen.fill((135, 206, 250))
    if K_SPACE in userInput.unpressedKeys:
      return 'done'

class GameHandler:
  def __init__(self, userInput):
    self.input = userInput

  def update(self):
    screen.fill((0,0,0))

class LevelMenu:
  def __init__(self):
    pass

  def update(self):
    pass


if __name__ == "__main__":
  run()