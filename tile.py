import pygame

class Tile:
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.revealed = False
        self.has_artifact = False
        self.has_lore = False
        self.image = image

    def reveal(self):
        self.revealed = True

    def draw(self, screen):
        if self.revealed:
            if self.has_artifact:
                color = (255, 215, 0)  # Gold color for artifact
            elif self.has_lore:
                color = (0, 191, 255)  # Deep sky blue for lore
            else:
                color = (100, 100, 100)  # Gray for revealed tile
            pygame.draw.rect(screen, color, self.rect)
        else:
            screen.blit(self.image, self.rect.topleft)