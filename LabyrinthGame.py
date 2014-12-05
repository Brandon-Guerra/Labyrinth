import math
import pygame
import math
from pygame.locals import *
from input import Input
from LevelGenerator import LevelGenerator

pygame.init()
WINDOWWIDTH, WINDOWHIEGHT = (1100,750)
screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHIEGHT))
clock = pygame.time.Clock()

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
    clock.tick(90)

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
        self.gameHandler.setMaze(self.levelGenerator.nextLevel())
        self.gameHandler.drawMaze()

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
    self.black = (0, 0, 0)
    self.thickness = 4
    self.length = 34
    self.none = 0
    self.offset = 30
    self.constant = 34
    self.walls = []
    self.start = maze.start
    self.finish = maze.finish
    x = maze.start[0]*self.constant + self.offset + 7
    y = maze.start[1]*self.constant + self.offset + 7
    self.player = Player((x,y))
    self.setMaze(maze)
    self.drawMaze()
    
  def update(self, userInput):
    if K_0 in userInput.unpressedKeys:
      return 'game over'
    if K_1 in userInput.unpressedKeys:
      return 'next level'
    if K_a in userInput.unpressedKeys or K_a in userInput.pressedKeys:
      self.movePlayer(-2,0)
    elif K_d in userInput.unpressedKeys or K_d in userInput.pressedKeys:
      self.movePlayer(2,0)
    elif K_w in userInput.unpressedKeys or K_w in userInput.pressedKeys:
      self.movePlayer(0,-2)
    elif K_s in userInput.unpressedKeys or K_s in userInput.pressedKeys:
      self.movePlayer(0,2)
    if K_EQUALS in userInput.unpressedKeys or K_EQUALS in userInput.pressedKeys:
      self.player.viewRadius += 2
    elif K_MINUS in userInput.unpressedKeys or K_MINUS in userInput.pressedKeys:
      self.player.viewRadius -= 2
    self.drawMaze()
    return 'continue'
  
  def setMaze(self, maze):
    """
    View a maze
    """
    self.finish = maze.finish
    self.start = maze.start
    self.walls = []
    screen.fill((200,200,200))
    # initialize north and west
    for i in range(maze.width):
      if maze.cell[i,0].north:
        self.addWall(True,i,0)
    for i in range(maze.height):
      if maze.cell[0,i].west:
        self.addWall(False,0,i)
    # loop through to draw the rest of the walls
    for i in range(maze.width):
      for j in range(maze.height):
        if maze.cell[i,j].south:
          self.addWall(True,i,j+1)
        if maze.cell[i,j].east:
          self.addWall(False,i+1,j)
    self.drawPlayer()
    self.drawItem(maze.finish)

  def drawMaze(self):
    screen.fill((200,200,200))
    for wall in self.walls:
      pygame.draw.rect(screen, self.black, wall, self.thickness)
    self.drawItem(self.finish)
    self.drawPlayer()
    self.drawDark(20)

  def drawPlayer(self):
    if self.player:
      pygame.draw.rect(screen, self.black, self.player.rect)
      # pygame.draw.circle(screen, self.black, (self.player.rect.x, self.player.rect.y), 1000, 800)

  def drawDark(self,n):
    center = []
    center.append(self.player.rect.x+self.player.rect.width/2)
    center.append(self.player.rect.y+self.player.rect.height/2)
    left = center[0] - self.player.viewRadius
    right = center[0] + self.player.viewRadius
    top = center[1] - self.player.viewRadius
    bottom = center[1] + self.player.viewRadius

    pygame.draw.rect(screen, self.black, Rect(0,0,left,WINDOWHIEGHT))
    pygame.draw.rect(screen, self.black, Rect(right,0,WINDOWWIDTH-right,WINDOWHIEGHT))
    pygame.draw.rect(screen, self.black, Rect(left,0,right - left, top))
    pygame.draw.rect(screen, self.black, Rect(left,bottom,right-left,WINDOWHIEGHT-bottom))

    points = range(n)
    points = map(lambda pt: pt/(len(points) - 1.0),points)
    points = map(lambda pt: pt*math.pi *2/4, points)
    points = map(lambda pt: (math.cos(pt), math.sin(pt)),points)
    points = map(lambda pt: (self.player.viewRadius *pt[0], self.player.viewRadius *pt[1]),points)
    for qudrant in ((1,1),(-1,1),(-1,-1),(1,-1)):
      x_flip = qudrant[0]
      y_flip = qudrant[1]
      edge = center[1] + self.player.viewRadius * y_flip
      for i in xrange(len(points) - 1):
        A = (points[i][0] * x_flip + center[0], points[i][1] * y_flip + center[1])
        B = (points[i+1][0] * x_flip + center[0], points[i+1][1] * y_flip + center[1])
        A_edge = (A[0], edge)
        B_edge = (B[0], edge)
        pygame.draw.polygon(screen,self.black, (A,B,B_edge,A_edge))

  def movePlayer(self, dx, dy):
    if dx != 0:
      self.moveSingleAxis(dx, 0)
    if dy != 0:
      self.moveSingleAxis(0, dy)

  def moveSingleAxis(self, dx, dy):
    self.player.rect.x += dx
    self.player.rect.y += dy

    for wall in self.walls:
      if self.player.rect.colliderect(wall):
        if dx > 0:
          self.player.rect.right = wall.left-3
        if dx < 0:
          self.player.rect.left = wall.right+3
        if dy > 0:
          self.player.rect.bottom = wall.top-3
        if dy < 0:
          self.player.rect.top = wall.bottom+3

  def drawItem(self, coord, type=None):
    x,y = coord
    xAdjust = x*self.constant+self.offset+self.offset/2+3
    yAdjust = y*self.constant+self.offset+self.offset/2+3
    pygame.draw.circle(screen, self.black, (xAdjust, yAdjust),self.offset/2-4,4)

  def addWall(self, isHorizontal, x, y):
    """
    Draw wall for a cell
    """
    if isHorizontal:
      self.walls.append(pygame.Rect(x*self.constant + self.offset, y*self.constant + self.offset, self.length, self.none))
    else:
      self.walls.append(pygame.Rect(x*self.constant + self.offset, y*self.constant + self.offset, self.none, self.length))

class Player:
  def __init__(self,coord):
    self.viewRadius = 100
    self.oilLevel = 100
    x,y = coord
    self.rect = pygame.Rect(x,y,20,20)

if __name__ == "__main__":
  run()