import pygame
from pygame.locals import *
from LevelGenerator import LevelGenerator

class View:
  def __init__(self):
    """
    Constructor
    """
    self.black = (0, 0, 0)
    self.thickness = 4
    self.width = 30
    self.height = 30
    self.none = 0
    self.offset = 30
    self.constant = 34

  def drawMaze(maze):
    """
    View a maze
    """
    # initialize north and west
    for i in maze.width:
      if maze.cell[i,0].north:
        drawWall(True,i,0)
    for i in maze.height:
      if maze.cell[0,j].west:
        drawWall(False,0,j)
    # loop through to draw the rest of the walls
    for i in maze.width:
      for j in maze.height:
        if maze.cell[i][j].south:
          drawWall(True,i,j+1)
        if maze.cell[i][j].east:
          drawWall(False,i+1,j)

  def drawWall(isHorizontal, x, y):
    """
    Draw wall for a cell
    """
    if isHorizantal:
      pygame.draw.rect(background, black, (x*constant + offset, y*constant + offset, width, none), thickness)
    else:
      pygame.draw.rect(background, black, (x*constant + offset, y*constant + offset, width, none), thickness)
