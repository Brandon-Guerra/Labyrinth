import pygame, sys
from pygame.locals import *

class Input:
  def __init__(self):
    self.pressedKeys = []
    self.unpressedKeys = []
    self.justPressedKeys = []
  
  def get(self):
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key not in self.pressedKeys:
          self.justPressedKeys.append(event.key)
        self.pressedKeys.append(event.key)
      elif event.type == KEYUP:
        for key in self.pressedKeys:
          if event.key == key:
            self.pressedKeys.remove(key)
          self.unpressedKeys.append(key)
      elif event.type == QUIT:
        pygame.event.post(event)

    self.checkForQuit()

  def checkForQuit(self):
    for event in pygame.event.get(QUIT):
      pygame.quit()
      sys.exit()
    if K_ESCAPE in self.unpressedKeys:
      pygame.quit()
      sys.exit()