"""
Tile-Based Puzzle Game

This program implements a simple tile-based puzzle game using Pygame.

Game Description:
- The game consists of multiple levels, each with a grid of tiles.
- The player can move around the level using arrow keys.
- Each level has a hidden key on one of the tiles.
- The player must find the key by clicking on tiles or moving over them and pressing Enter.
- When the key is found, the player advances to the next level.
- The game continues indefinitely, increasing in level number.

Key Features:
- Randomly generated levels with different tile images
- Player movement with collision detection
- Tile interaction through mouse clicks and keyboard input
- Level progression system
- Scrolling background to create a sense of movement

Controls:
- Arrow keys: Move the player
- Mouse click: Reveal a tile
- Enter key: Interact with the tile the player is standing on

Dependencies:
- Python 3.x
- Pygame library

Author: [mcuser]
Date: [07-07-2024]
Version: 1.0
"""

import pygame
import sys
import random
from constants import *
from player import Player
from tile import Tile
from utils import load_tile_images

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.current_level = 1
        self.background_x = 0
        self.player = Player(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)
        self.tile_images = load_tile_images(NUM_TILE_IMAGES, TILE_SIZE)
        self.tiles = self.create_tiles()
        self.place_key()

    def create_tiles(self):
        # Create an empty list to store the tiles
        tiles = []

        # Loop through the level width
        for x in range(0, LEVEL_WIDTH, TILE_SIZE):
            # Loop through the screen height
            for y in range(0, HEIGHT, TILE_SIZE):
                # Choose a random tile image
                image = random.choice(self.tile_images)

                # Create a new tile with the specified position, size, and image
                tiles.append(Tile(x, y, TILE_SIZE, TILE_SIZE, image))

        # Return the list of tiles
        return tiles

    def place_key(self):
        # Get a list of tiles that are currently visible on the screen
        visible_tiles = [tile for tile in self.tiles if tile.rect.x < WIDTH]

        # Choose a random visible tile to place the key on
        key_tile = random.choice(visible_tiles)

        # Set the has_key attribute of the chosen tile to True
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
            # Check if the user has requested to quit the game
            if event.type == pygame.QUIT:
                pygame.quit()  # Uninitialize all pygame modules
                sys.exit()     # Exit the program

            # Check if the user has clicked the mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_tile_click(event.pos)  # Check if a tile was clicked

            # Check if a key has been pressed down
            elif event.type == pygame.KEYDOWN:
                # Check if the Enter key was pressed
                if event.key == pygame.K_RETURN:
                    self.check_tile_interaction()  # Check if the player is interacting with a tile

    def check_tile_click(self, pos):
        # Loop through the list of tiles
        for tile in self.tiles:
            # Check if the mouse click position is within the tile's rectangle
            if tile.rect.collidepoint(pos):
                # Call the interact_with_tile method with the clicked tile
                self.interact_with_tile(tile)

    def check_tile_interaction(self):
        # Loop through the list of tiles
        for tile in self.tiles:
            # Check if the player's rectangle intersects with the tile's rectangle
            if tile.rect.colliderect(self.player.rect):
                # Call the interact_with_tile method with the interacted tile
                self.interact_with_tile(tile)

    def interact_with_tile(self, tile):
        # If the tile has a key
        if tile.has_key:
            # Reveal the tile
            tile.reveal()
            # Advance to the next level
            self.advance_level()
        # If the tile doesn't have a key
        else:
            # Reveal the tile
            tile.reveal()

    def advance_level(self):
        # Increment the current level
        self.current_level += 1

        # Reset the background position
        self.background_x = 0

        # Reset the player position
        self.player.rect.x = 0

        # Create a new set of tiles
        self.tiles = self.create_tiles()

        # Place a new key
        self.place_key()

    def update(self):
        # Update game state
        keys = pygame.key.get_pressed()
        self.player.move(keys)  # Move the player based on key input
        self.scroll_background()  # Scroll the background

    def scroll_background(self):
        # Scroll the background to create a sense of movement
        self.background_x -= SCROLL_SPEED  # Move the background to the left

        # If the background has moved off the screen to the left,
        # reset its position to the right edge of the screen
        if self.background_x < -LEVEL_WIDTH:
            self.background_x = 0  # Reset to the right edge of the screen

        # If the background has moved off the screen to the right,
        # reset its position to the left edge of the screen
        if self.background_x > 0:
            self.background_x = 0  # Reset to the left edge of the screen

        # If the background is partially off the screen to the left,
        # move it to the right edge of the screen
        elif self.background_x < -LEVEL_WIDTH + WIDTH:
            self.background_x = -LEVEL_WIDTH + WIDTH  # Move to the right edge of the screen

    def draw(self):
        # Fill the screen with a black background
        self.screen.fill((0, 0, 0))

        # Draw each tile
        for tile in self.tiles:
            tile.draw(self.screen)

        # Draw the player
        self.player.draw(self.screen)

        # Draw the level number text
        text = self.font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        # Update the display
        pygame.display.flip()