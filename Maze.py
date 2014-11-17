# Maze object
# Luke oglesbee
# Created 11/16/14

class Cell:
  def __init__(self, content):
    self.north = False
    self.south = False
    self.east = False
    self.west = False
    self.content = content
  def __str__(self):
    return str(self.content)

class Maze:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.cell = []
    for x in range(height):
      cellRow = []
      for y in range(width):
        cellRow.append(Cell(0))
      self.cell.append(cellRow)
  def __str__(self):
    out  = "\n" + " "*4 + "MAZE -- width: %s, heigth: %s\n\n" % (self.width, self.height)
    out += " "*4
    for i in range(self.width):
      out += "%3s"%i
    out += "\n"+" "*4
    out += "-"*(self.width*3)
    out += "\n"
    row = 0
    for x in self.cell:
      out += "%2s |"%row
      row += 1
      for y in x:
        out += "%3s" % y
      out += "\n"
    return out

m = Maze(20,10)
print m