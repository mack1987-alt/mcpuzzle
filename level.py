import pygame
import random
from constants import *
from tile import Tile
from utils import load_tile_images

class Level:
    def __init__(self, level_number):
        self.current_level = level_number
        self.tile_maps = {
            1: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            2: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            3: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            4: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            5: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            6: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            7: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            8: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            9: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            10: [
                [1, 2, 1, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0],
                [2, 1, 0, 2, 1, 2, 1, 0],
                [0, 2, 1, 1, 1, 2, 1, 0],
                [1, 0, 2, 0, 1, 2, 1, 0]
            ],
            # Add more levels as needed
        }
        self.tiles = []
        self.artifacts = []
        self.lore_items = []
        self.current_theme = None

    def load_level(self, level_number):
        self.current_level = level_number
        self.set_level_theme()
        self.tile_images = load_tile_images(NUM_TILE_IMAGES, TILE_SIZE, self.current_theme)
        self.tiles = self.create_tiles()
        self.place_artifact()
        self.place_lore_items()

    def set_level_theme(self):
        themes = ["Ancient Egypt", "Medieval Europe", "Present Day", "Distant Future"]
        self.current_theme = themes[(self.current_level - 1) % len(themes)]

    def create_tiles(self):
        tile_map = self.tile_maps[self.current_level]
        tiles = []
        for y, row in enumerate(tile_map):
            for x, tile_type in enumerate(row):
                image = self.tile_images[tile_type]
                tiles.append(Tile(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, image))
        return tiles

    def place_artifact(self):
        visible_tiles = [tile for tile in self.tiles if tile.rect.x < WIDTH]
        artifact_tile = random.choice(visible_tiles)
        artifact_tile.has_artifact = True
        self.artifacts.append(f"Artifact from Level {self.current_level}")

    def place_lore_items(self):
        num_lore_items = random.randint(1, 3)
        visible_tiles = [tile for tile in self.tiles if tile.rect.x < WIDTH and not tile.has_artifact]
        for _ in range(num_lore_items):
            if visible_tiles:
                lore_tile = random.choice(visible_tiles)
                lore_tile.has_lore = True
                visible_tiles.remove(lore_tile)

    def get_time_power(self):
        powers = [None, "Slow Time", "Rewind", "Time Stop"]
        return powers[self.current_level // 3]

    def check_boss_appearance(self):
        return self.current_level in [5, 10]

    def check_tile_click(self, pos, player):
        for tile in self.tiles:
            if tile.rect.collidepoint(pos):
                self.interact_with_tile(tile, player)

    def check_tile_interaction(self, player):
        for tile in self.tiles:
            if tile.rect.colliderect(player.rect):
                self.interact_with_tile(tile, player)

    def interact_with_tile(self, tile, player):
        if tile.has_artifact:
            self.collect_artifact(tile)
        elif tile.has_lore:
            self.collect_lore(tile)
        tile.reveal()

    def collect_artifact(self, tile):
        print(f"Collected artifact from {self.current_theme}")
        self.artifacts.append(f"Artifact from {self.current_theme}")
        tile.has_artifact = False

    def collect_lore(self, tile):
        print(f"Collected lore item from {self.current_theme}")
        self.lore_items.append(f"Lore from {self.current_theme}")
        tile.has_lore = False

    def all_lore_collected(self):
        return all(not tile.has_lore for tile in self.tiles)

    def update_boss(self):
        # Implement boss movement and attacks
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Fill the screen with a solid color
        for tile in self.tiles:
            tile.draw(screen)

    def draw_boss(self, screen):
        # Draw the boss character
        pass