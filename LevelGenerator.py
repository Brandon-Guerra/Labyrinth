# Level Generator
# Luke Oglesbee
# Created 11/18/2014

from Maze import Maze
import random

class LevelGenerator:
  def __init__(self):
    """
    Constructor
    """
    self.level = 0
    self.width = 30
    self.height = 20
    self.widthIncrement = 0
    self.heightIncrement = 0
    self.startIndex = None
    self.endIndex = None
    self.currentMaze = None

  def nextLevel(self):
    """
    Creates a new level in the following steps
      1) Update difficulty metrics
      2) Generates a valid maze by calling __generateMaze()
      3) Add content to the maze
    Sets the new maze to currentMAze and returns that maze.
    """
    self.level += 1
    self.width += self.widthIncrement
    self.height += self.heightIncrement
    maze = Maze(self.width, self.height)
    maze = self.__generateMaze(maze)
    del self.currentMaze
    self.currentMaze = maze
    return self.currentMaze

  def currentLevel(self):
    """
    Returns the currentLevel of the LevelGenerator
    """
    return self.currentMaze

  def __generateMaze(self, maze):
    """
    Accepts a maze object expecting that all walls are present.
    Returns a perfect maze.
    """
    visitedCells = []
    walls = []
    # Set start and end index
    start = (random.randint(0,self.width-1),random.randint(0,self.height-1))
    finish = start
    while min(abs(finish[0]-start[0]),abs(finish[1]-start[1])) < min(maze.width/2,maze.height/2):
      finish = (random.randint(0,self.width-1),random.randint(0,self.height-1))
    maze.setStart(start)
    maze.setFinish(finish)
    visitedCells.append(start)
    walls.extend(maze.getWalls(start))
    while walls:
      w = walls.pop(random.randint(0,len(walls)-1))
      if w[1] not in visitedCells and maze.isValidIndex(w[1][0],w[1][1]):
        maze.destroyWall(w[0],w[1])
        visitedCells.append(w[1])
        walls.extend(maze.getWalls(w[1]))
    return maze

  def __str__(self):
    s = ""
    s += "level: %i\n" % self.level
    s += "width: %i\nheight: %i\n" %(self.width, self.height)
    return

l = LevelGenerator()
m = l.nextLevel()
