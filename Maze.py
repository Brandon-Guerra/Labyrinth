# Maze object
# Luke oglesbee
# Created 11/16/14

class Cell:
  def __init__(self, content):
    """
    Construcotr
    """
    self.north = True
    self.south = True
    self.east = True
    self.west = True
    self.content = content 

  def __str__(self):
    """
    To string
    """
    return str(self.content)

class Maze:
  def __init__(self, width, height):
    """
    Constructor
    """
    self.width = width
    self.height = height
    self.start = None
    self.finish = None
    self.cell = {}
    for x in range(width):
      for y in range(height):
        self.cell[x,y] = Cell("_")

  def buildWall(self, aIndex, bIndex):
    """
    Adds a wall between two cells if it is possible
    aIndex and bIndex are tuples of (x,y) values
    """
    return self.__wallHelper(aIndex, bIndex, True)

  def destroyWall(self, aIndex, bIndex):
    """
    Removes a wall betwen two cells if it is possible.
    aIndex and bIndex are tuples of (x,y) values
    Returns True for success and False for error
    """
    return self.__wallHelper(aIndex, bIndex, False)

  def setContent(self, content, coord):
    """
    Set the content of a cell
    """
    x = coord[0]
    y = coord[1]
    self.cell[x,y].content = content

  def setStart(self, coord):
    self.start = coord
    x,y = coord
    self.cell[x,y].content = "start"

  def setFinish(self, coord):
    self.finish = coord
    x,y = coord
    self.cell[x,y].content = "finish"

  

  def getWalls(self, coords):
    """
    Get walls
    """
    x = coords[0]
    y = coords[1]
    if not self.isValidIndex(x,y):
      return False
    c = self.cell[x,y]
    walls = []
    if c.north:
      walls.append(((x,y),(x,y-1)))
    if c.south:
      walls.append(((x,y),(x,y+1)))
    if c.east:
      walls.append(((x,y),(x+1,y)))
    if c.west:
      walls.append(((x,y),(x-1,y)))
    return walls

  def isValidIndex(self, x, y):
    """
    Checks if particular index is in the game board range
    """ 
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      return False
    return True
  
  def __wallHelper(self, aIndex, bIndex, isBuild):
    """
    Helper function for buildWall and destroyWall
    Contains dat logic doh
    """
    #Bounds check for the border
    if not self.isValidIndex(aIndex[0],aIndex[1]):
      return False
    if not self.isValidIndex(bIndex[0],bIndex[1]):
      return False
    #Find wall to alter
    xDif = aIndex[0] - bIndex[0]
    yDif = aIndex[1] - bIndex[1]
    if xDif == 1 and yDif == 0:
      self.cell[aIndex[0],aIndex[1]].west = isBuild
      self.cell[bIndex[0],bIndex[1]].east = isBuild
    elif xDif == -1 and yDif == 0:
      self.cell[bIndex[0],bIndex[1]].west = isBuild
      self.cell[aIndex[0],aIndex[1]].east = isBuild
    elif yDif == 1 and xDif == 0:
      self.cell[aIndex[0],aIndex[1]].north = isBuild
      self.cell[bIndex[0],bIndex[1]].south = isBuild
    elif yDif == -1 and xDif == 0:
      self.cell[bIndex[0],bIndex[1]].north = isBuild
      self.cell[aIndex[0],aIndex[1]].south = isBuild
    else:
      return False
    if True:
      a = self.cell[aIndex[0],aIndex[1]]
      b = self.cell[bIndex[0],bIndex[1]]
      # print "-- a (%s,%s)--" % (aIndex[0],aIndex[1])
      # print "N: %s\nS: %s\nE: %s\nW: %s\n" % (a.north, a.south, a.east, a.west)
      # print "-- b (%s,%s)--" % (bIndex[0],bIndex[1])
      # print "N: %s\nS: %s\nE: %s\nW: %s\n" % (b.north, b.south, b.east, b.west)
    return True





