import pygame
from constants import WIDTH, HEIGHT, PLAYER_SPEED

class Player:
    def __init__(self, x, y, width, height):
        # Load all player images
        self.images = {
            'left': pygame.transform.scale(pygame.image.load("/home/mcuser/game-test/player-left.png").convert_alpha(), (width, height)),
            'right': pygame.transform.scale(pygame.image.load("/home/mcuser/game-test/player-right.png").convert_alpha(), (width, height)),
            'up': pygame.transform.scale(pygame.image.load("/home/mcuser/game-test/player-up.png").convert_alpha(), (width, height)),
            'down': pygame.transform.scale(pygame.image.load("/home/mcuser/game-test/player-down.png").convert_alpha(), (width, height)),
        }
        # Set initial image (you can choose any direction to start with)
        self.current_image = self.images['down']
        self.rect = self.current_image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, keys):
        moved = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.current_image = self.images['left']
            moved = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.current_image = self.images['right']
            moved = True
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
            self.current_image = self.images['up']
            moved = True
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
            self.current_image = self.images['down']
            moved = True

        # Ensure the player doesn't move off the screen
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

        return moved

    def draw(self, screen):
        screen.blit(self.current_image, self.rect)