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
    self.levelGenerator = LevelGenerator()
    FPSClock.tick(60)

  def update(self):
    self.input.get() #check for quit
    if self.mode == 'menu':
      isDone = self.menu.update(self.input)
      if isDone:
        self.mode = 'game'
        self.gameHandler = GameHandler("none")
    
    if self.mode == 'game':
      result = self.gameHandler.update(self.input)
      if result == 'game over':
        self.mode = 'menu'
        self.menu = StartMenu()
    pygame.display.update()

class StartMenu:
  def __init__(self):
    screen.fill((0, 0, 0))
    header = pygame.font.SysFont("serif", 74)
    subtext = pygame.font.SysFont("sansserif", 30)
    titletext = header.render("Labyrinth", 1, (255, 255, 255))
    instruction = subtext.render("press space bar to play", 1, (255, 255, 255))
    description = "Use the arrow keys to move around. "
    description += "Make your way out of the maze before you run out of oil."
    destext = subtext.render(description, 1, (255, 255, 255))
    titlepos = titletext.get_rect()
    titlepos.centerx = screen.get_rect().centerx
    titlepos.centery = screen.get_rect().centery - 60
    instpos = instruction.get_rect()
    instpos.centerx = screen.get_rect().centerx
    instpos.centery = screen.get_rect().centery
    despos = destext.get_rect()
    despos.centerx = screen.get_rect().centerx
    despos.centery = screen.get_rect().centery + 37
    screen.blit(titletext, titlepos)
    screen.blit(instruction, instpos)
    screen.blit(destext, despos)

  def update(self, userInput):
    if K_SPACE in userInput.unpressedKeys:
      return 'done'

class GameHandler:
  def __init__(self, maze):
    screen.fill((200,200,200))
    

  def update(self, userInput):
    if K_0 in userInput.unpressedKeys:
      return 'game over'
    if K_1 in userInput.unpressedKeys:
      return 'next level'


if __name__ == "__main__":
  run()