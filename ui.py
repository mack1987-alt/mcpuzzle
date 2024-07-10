# ui.py
import pygame
from constants import *

class UI:
    def __init__(self, font):
        self.font = font

    def draw(self, screen, current_level, player_health, time_remaining, tiles_left, artifacts, lore_items, time_power):
        # Draw the UI background
        pygame.draw.rect(screen, (50, 50, 50), (0, HEIGHT, WIDTH, UI_HEIGHT))

        # Display current level
        level_text = self.font.render(f"Level: {current_level}", True, (255, 255, 255))
        screen.blit(level_text, (10, HEIGHT + 10))

        # Display player health
        health_text = self.font.render(f"Health: {player_health}", True, (255, 255, 255))
        screen.blit(health_text, (10, HEIGHT + 50))

        # Display time remaining
        time_text = self.font.render(f"Time: {int(time_remaining)}", True, (255, 255, 255))
        screen.blit(time_text, (200, HEIGHT + 10))

        # Display tiles left to click on
        tiles_text = self.font.render(f"Tiles Left: {tiles_left}", True, (255, 255, 255))
        screen.blit(tiles_text, (200, HEIGHT + 50))

        # Display artifacts found
        artifacts_text = self.font.render(f"Artifacts: {len(artifacts)}", True, (255, 255, 255))
        screen.blit(artifacts_text, (400, HEIGHT + 10))

        # Display lore items found
        lore_text = self.font.render(f"Lore Items: {len(lore_items)}", True, (255, 255, 255))
        screen.blit(lore_text, (400, HEIGHT + 50))

        # Display time power
        if time_power:
            power_text = self.font.render(f"Power: {time_power}", True, (255, 255, 255))
            screen.blit(power_text, (600, HEIGHT + 10))