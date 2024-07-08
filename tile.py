import pygame

class Tile:
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.revealed = False
        self.has_key = False
        self.image = image

    def reveal(self):
        self.revealed = True

    def draw(self, screen):
        if self.revealed:
            color = (255, 255, 255) if self.has_key else (100, 100, 100)
            pygame.draw.rect(screen, color, self.rect)
        else:
            screen.blit(self.image, self.rect.topleft)