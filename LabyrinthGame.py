import math
import pygame
import math
from pygame.locals import *
from input import Input
from LevelGenerator import LevelGenerator

pygame.init()
WINDOWWIDTH, WINDOWHEIGHT = (1100,750)
screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
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
    instruction = subtext.render("press space bar to play or 'esc' to exit", 1, (255, 255, 255))
    description = "Stay in the maze for as long as you can by collection oil. "
    description += 'Move with "w", "a", "s", "d" and increase/decrease your field of view '
    description += 'with the "+"" and "-" keys. Good luck!' 
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
    self.yellow = (255,255,51)
    self.thickness = 4
    self.length = 34
    self.none = 0
    self.offset = 30
    self.constant = 34
    self.walls = []
    self.start = maze.start
    self.finish = Finish(maze.finish)
    self.player = Player(maze.start)
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
      self.player.increaseRadius()
    elif K_MINUS in userInput.unpressedKeys or K_MINUS in userInput.pressedKeys:
      self.player.decreaseRadius()
    self.player.diminishOil()
    if self.player.oilLevel == 0:
      return 'game over'
    if self.player.rect.colliderect(self.finish):
      self.player.addOil()
      return 'next level'

    self.drawMaze()
    return 'continue'
  
  def setMaze(self, maze):
    """
    View a maze
    """
    self.finish = Finish(maze.finish)
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
    self.player.draw()
    self.drawItem(maze.finish)

  def drawMaze(self):
    screen.fill((200,200,200))
    for wall in self.walls:
      pygame.draw.rect(screen, self.black, wall, self.thickness)
    self.player.draw()
    self.finish.draw()
    self.drawDark(20)
    self.drawOilLevel()

  def drawDark(self,n):
    center = []
    center.append(self.player.rect.x+self.player.rect.width/2)
    center.append(self.player.rect.y+self.player.rect.height/2)
    left = center[0] - self.player.viewRadius
    right = center[0] + self.player.viewRadius
    top = center[1] - self.player.viewRadius
    bottom = center[1] + self.player.viewRadius

    pygame.draw.rect(screen, self.black, Rect(0,0,left,WINDOWHEIGHT))
    pygame.draw.rect(screen, self.black, Rect(right,0,WINDOWWIDTH-right,WINDOWHEIGHT))
    pygame.draw.rect(screen, self.black, Rect(left,0,right - left, top))
    pygame.draw.rect(screen, self.black, Rect(left,bottom,right-left,WINDOWHEIGHT-bottom))

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

  def drawOilLevel(self):
    """
    Drawing the current oil level
    """
    pygame.draw.rect(screen, self.yellow, (0, 740, WINDOWWIDTH/200 * self.player.oilLevel, self.none), self.thickness)

class Finish:
  def __init__(self,coord):
    self.color = (0,0,0)
    self.constant = 34
    self.offset = 30
    x = coord[0]*self.constant + self.offset + 7
    y = coord[1]*self.constant + self.offset + 7
    self.rect = pygame.Rect(x,y,20,20)

  def setCoord(self, coord):
    self.rect.x = coord[0]*self.constant + self.offset + 7
    self.rect.y = coord[1]*self.constant + self.offset + 7

  def draw(self):
    left = self.rect.x+2
    right = self.rect.x+self.rect.width-3
    middle = (self.rect.x+self.rect.width/2,self.rect.y+self.rect.height/2+3)
    pygame.draw.circle(screen, self.color, middle, 8)
    pygame.draw.polygon(screen, self.color, ((left,middle[1]),(right,middle[1]),(middle[0],middle[1]-14)))

class Player:
  def __init__(self,coord):
    self.viewRadius = 100
    self.oilLevel = 100
    self.color = (0,0,0)
    self.constant = 34
    self.offset = 30
    x = coord[0]*self.constant + self.offset + 12
    y = coord[1]*self.constant + self.offset + 12
    self.rect = pygame.Rect(x,y,10,10)

  def draw(self):
    img = pygame.Rect(self.rect.x-5,self.rect.y-5,20,20)
    pygame.draw.rect(screen, self.color, img)

  def addOil(self):
    self.oilLevel = min(200,self.oilLevel+50)

  def diminishOil(self):
    self.oilLevel = max(0,self.oilLevel - math.pow(self.viewRadius,1.5)*0.00001)
    print self.oilLevel

  def increaseRadius(self):
    self.viewRadius = min(300,self.viewRadius+2)

  def decreaseRadius(self):
    self.viewRadius = max(50,self.viewRadius-2)

if __name__ == "__main__":
  run()