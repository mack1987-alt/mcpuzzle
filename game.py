import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
SCROLL_SPEED = 2
LEVEL_WIDTH = WIDTH * 2  # Each level is twice the screen width
TILE_SIZE = 100  # Size of each tile
NUM_TILE_IMAGES = 5  # Number of different tile images

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.current_level = 1
        self.background_x = 0
        self.player = Player(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)
        self.tile_images = self.load_tile_images()
        self.tiles = self.create_tiles()
        self.place_key()

    def load_tile_images(self):
        tile_images = []
        for i in range(NUM_TILE_IMAGES):
            image = pygame.image.load(f'/home/mcuser/game-test/tile_image{i}.png')
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            tile_images.append(image)
        return tile_images

    def create_tiles(self):
        tiles = []
        for x in range(0, LEVEL_WIDTH, TILE_SIZE):
            for y in range(0, HEIGHT, TILE_SIZE):
                image = random.choice(self.tile_images)
                tiles.append(Tile(x, y, TILE_SIZE, TILE_SIZE, image))
        return tiles

    def place_key(self):
        visible_tiles = [tile for tile in self.tiles if tile.rect.x < WIDTH]
        key_tile = random.choice(visible_tiles)
        key_tile.has_key = True

    def run(self):
        # Main game loop
        while True:
            self.handle_events()  # Handle user input
            self.update()         # Update game state
            self.draw()           # Draw everything on the screen
            self.clock.tick(60)   # Cap the frame rate to 60 FPS

    def handle_events(self):
        # Handle events such as quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_tile_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.check_tile_interaction()

    def check_tile_click(self, pos):
        for tile in self.tiles:
            if tile.rect.collidepoint(pos):
                self.interact_with_tile(tile)

    def check_tile_interaction(self):
        for tile in self.tiles:
            if tile.rect.colliderect(self.player.rect):
                self.interact_with_tile(tile)

    def interact_with_tile(self, tile):
        if tile.has_key:
            tile.reveal()
            self.advance_level()
        else:
            tile.reveal()

    def advance_level(self):
        self.current_level += 1
        self.background_x = 0
        self.player.rect.x = 0
        self.tiles = self.create_tiles()
        self.place_key()

    def update(self):
        # Update game state
        keys = pygame.key.get_pressed()
        self.player.move(keys)  # Move the player based on key input
        self.scroll_background()  # Scroll the background

    def scroll_background(self):
        # Scroll the background to create a sense of movement
        self.background_x -= SCROLL_SPEED
        if self.background_x < -LEVEL_WIDTH:
            self.background_x = 0
        if self.background_x > 0:
            self.background_x = 0
        elif self.background_x < -LEVEL_WIDTH + WIDTH:
            self.background_x = -LEVEL_WIDTH + WIDTH

    def draw(self):
        # Draw everything on the screen
        self.screen.fill((0, 0, 0))
        for tile in self.tiles:
            tile.draw(self.screen)
        self.player.draw(self.screen)
        text = self.font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, keys):
        # Move the player based on key input
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

        # Ensure the player doesn't move off the screen
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self, screen):
        # Draw the player on the screen
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

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

if __name__ == "__main__":
    game = Game()
    game.run()