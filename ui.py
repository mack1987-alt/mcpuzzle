import pygame

class UI:
    def __init__(self, font):
        self.font = font

    def draw(self, screen, current_level, current_theme, time_power):
        text = self.font.render(f"Level: {current_level} - {current_theme}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        if time_power:
            power_text = self.font.render(f"Power: {time_power}", True, (255, 255, 255))
            screen.blit(power_text, (10, 50))