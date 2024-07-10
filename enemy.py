import random
import pygame
from constants import *

class Enemy:
  def __init__(self, x, y, width, height):
      self.rect = pygame.Rect(x, y, width, height)
      self.color = (255, 0, 0)  # Red color for enemies
      self.speed = random.randint(1, 3)  # Random speed for each enemy

  def move(self):
      # Simple movement: move left and right
      self.rect.x += self.speed
      if self.rect.right > WIDTH or self.rect.left < 0:
          self.speed = -self.speed

  def draw(self, screen):
      pygame.draw.rect(screen, self.color, self.rect)