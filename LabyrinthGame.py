import pygame
from pygame.locals import *
from input import Input
from LevelGenerator import LevelGenerator

pygame.init()
WINDOWWIDTH, WINDOWHIEGHT = (1100,750)
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
        self.gameHandler = GameHandler(self.levelGenerator.nextLevel())
    
    if self.mode == 'game':
      result = self.gameHandler.update(self.input)
      if result == 'game over':
        self.mode = 'menu'
        self.menu = StartMenu()
      elif result == 'next level':
        self.gameHandler.drawMaze(self.levelGenerator.nextLevel())

    pygame.display.update()


class StartMenu:
  def __init__(self):
    screen.fill((0, 0, 0))
    header = pygame.font.Font("fonts/RussoOne-Regular.ttf", 74)
    subtext = pygame.font.SysFont("fonts/RussoOne-Regular.ttf", 30)
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
    self.black = (0, 0, 0)
    self.thickness = 4
    self.width = 34
    self.height = 34
    self.none = 0
    self.offset = 30
    self.constant = 34
    self.player = Player()
    self.drawMaze(maze)
    
  def update(self, userInput):
    if K_0 in userInput.unpressedKeys:
      return 'game over'
    if K_1 in userInput.unpressedKeys:
      return 'next level'
  
  def drawMaze(self, maze):
    """
    View a maze
    """
    screen.fill((200,200,200))
    # initialize north and west
    for i in range(maze.width):
      if maze.cell[i,0].north:
        self.drawWall(True,i,0)
    for i in range(maze.height):
      if maze.cell[0,i].west:
        self.drawWall(False,0,i)
    # loop through to draw the rest of the walls
    for i in range(maze.width):
      for j in range(maze.height):
        if maze.cell[i,j].south:
          self.drawWall(True,i,j+1)
        if maze.cell[i,j].east:
          self.drawWall(False,i+1,j)
    x = maze.start[0]*self.constant+self.offset+self.offset/2+3
    y = maze.start[1]*self.constant+self.offset+self.offset/2+3
    self.player.setCoord((x,y))
    self.drawPlayer()
    self.drawItem(maze.finish)

  def drawItem(self, coord, type=None):
    x,y = coord
    xAdjust = x*self.constant+self.offset+self.offset/2+3
    yAdjust = y*self.constant+self.offset+self.offset/2+3
    pygame.draw.circle(screen, self.black, (xAdjust, yAdjust),self.offset/2-4,4)

  def drawPlayer(self):
    if self.player.coord:
      x,y = self.player.coord
    else:
      print "No coords for player"
      return
    pygame.draw.circle(screen, self.black, (x, y),self.offset/2-4)

  def drawWall(self, isHorizontal, x, y):
    """
    Draw wall for a cell
    """
    if isHorizontal:
      pygame.draw.rect(screen, self.black, (x*self.constant + self.offset, y*self.constant + self.offset, self.width, self.none), self.thickness)
    else:
      pygame.draw.rect(screen, self.black, (x*self.constant + self.offset, y*self.constant + self.offset, self.none, self.height), self.thickness)

class Player:
  def __init__(self):
    self.coord = None
    self.viewRadius = 50
    self.oilLevel = 100

  def move(self,dir):
    if coords == None:
      return false

  def setCoord(self, coord):
    self.coord = coord

if __name__ == "__main__":
  run()