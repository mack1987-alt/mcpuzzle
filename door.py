import pygame

class Door:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0))  # Green color for the door

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)