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
    	# Initialize Pygame
    	pygame.init()

    	# Set up the display
    	self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    	# Create a clock object for managing the game's frame rate
    	self.clock = pygame.time.Clock()

    	# Set up the font for text rendering
    	self.font = pygame.font.Font(None, 36)

    	# Initialize game state variables
    	self.current_level = 1
    	self.max_levels = 10
    	self.background_x = 0

    	# Create the player object
    	self.player = Player(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)

    	# Load tile images and create the tiles
    	self.tile_images = load_tile_images(NUM_TILE_IMAGES, TILE_SIZE)
    	self.tiles = self.create_tiles()

    	# Initialize lists for artifacts and lore items
    	self.artifacts = []
    	self.lore_items = []

    	# Initialize time power-up and boss presence variables
    	self.time_power = None
    	self.boss_present = False

    	# Initialize the level
    	self.initialize_level()

    def initialize_level(self):
        self.tiles = self.create_tiles()
        self.place_artifact()
        self.place_lore_items()
        self.set_level_theme()
        self.set_time_power()
        self.check_boss_appearance()

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

    def place_artifact(self):
        visible_tiles = [tile for tile in self.tiles if tile.rect.x < WIDTH]
        artifact_tile = random.choice(visible_tiles)
        artifact_tile.has_artifact = True
        self.artifacts.append(f"Artifact from Level {self.current_level}")

    def place_lore_items(self):
        # Place 1-3 lore items randomly on the level
        num_lore_items = random.randint(1, 3)
        visible_tiles = [tile for tile in self.tiles if tile.rect.x < WIDTH and not tile.has_artifact]
        for _ in range(num_lore_items):
            if visible_tiles:
                lore_tile = random.choice(visible_tiles)
                lore_tile.has_lore = True
                visible_tiles.remove(lore_tile)

    def set_level_theme(self):
        # Set visual theme based on the current level/time period
        themes = [
            "Ancient Egypt", "Roman Empire", "Medieval Europe",
            "Present Day", "Distant Future"
        ]
        self.current_theme = themes[self.current_level - 1]
        
    # def set_level_theme(self):
        # themes = {
            # "Ancient Egypt": "egypt",
            # "Roman Empire": "roman",
            # "Medieval Europe": "medieval",
            # "Present Day": "present",
            # "Distant Future": "future"
        # }
        # theme_name = themes[self.current_theme]
        # tile_images = load_tile_images(NUM_TILE_IMAGES, TILE_SIZE, theme_name)
        # self.tile_images = tile_images
        # self.tiles = self.create_tiles()
            
    def set_time_power(self):
        # Unlock new time power every 3 levels
        # these are junk powers
        # maybe have invincability, xray, jump, keep time stop
        # add power to add time to clock
        # each level has a timer on it.
        powers = [None, "Slow Time", "Rewind", "Time Stop"]
        self.time_power = powers[self.current_level // 3]

    def check_boss_appearance(self):
        # Boss appears on levels 5 and 10
        self.boss_present = self.current_level in [5, 10]

    def run(self):
        while self.current_level <= self.max_levels:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        self.show_ending()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_tile_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.check_tile_interaction()
                elif event.key == pygame.K_SPACE:
                    self.use_time_power()

    def check_tile_click(self, pos):
        for tile in self.tiles:
            if tile.rect.collidepoint(pos):
                self.interact_with_tile(tile)

    def check_tile_interaction(self):
        for tile in self.tiles:
            if tile.rect.colliderect(self.player.rect):
                self.interact_with_tile(tile)

    def interact_with_tile(self, tile):
        if tile.has_artifact:
            self.collect_artifact(tile)
        elif tile.has_lore:
            self.collect_lore(tile)
        tile.reveal()

    def collect_artifact(self, tile):
        print(f"Collected artifact from {self.current_theme}")
        self.artifacts.append(f"Artifact from {self.current_theme}")
        tile.has_artifact = False
        self.advance_level()

    def collect_lore(self, tile):
        print(f"Collected lore item from {self.current_theme}")
        self.lore_items.append(f"Lore from {self.current_theme}")
        tile.has_lore = False

    def use_time_power(self):
        if self.time_power:
            print(f"Using time power: {self.time_power}")
            # Implement time power effect

    def advance_level(self):
        if self.current_level < self.max_levels:
            self.current_level += 1
            self.initialize_level()
        else:
            self.show_ending()

    def scroll_background(self):
        # Scroll the background to create a sense of movement
        self.background_x -= SCROLL_SPEED
        if self.background_x < -LEVEL_WIDTH:
            self.background_x = 0
        if self.background_x > 0:
            self.background_x = 0
        elif self.background_x < -LEVEL_WIDTH + WIDTH:
            self.background_x = -LEVEL_WIDTH + WIDTH
            
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.scroll_background()
        if self.boss_present:
            self.update_boss()

    def update_boss(self):
        # Implement boss movement and attacks
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        for tile in self.tiles:
            tile.draw(self.screen)
        self.player.draw(self.screen)
        if self.boss_present:
            self.draw_boss()
        self.draw_ui()
        pygame.display.flip()

    def draw_boss(self):
        # Draw the boss character
        # boss_image = 
        pass

    def draw_ui(self):
        text = self.font.render(f"Level: {self.current_level} - {self.current_theme}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        if self.time_power:
            power_text = self.font.render(f"Power: {self.time_power}", True, (255, 255, 255))
            self.screen.blit(power_text, (10, 50))

    def show_ending(self):
        print("Game Over - You've completed the Temporal Labyrinth!")
        print(f"Collected Artifacts: {len(self.artifacts)}")
        print(f"Lore Items Found: {len(self.lore_items)}")
        pygame.quit()
        sys.exit()