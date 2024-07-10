import os
import pygame
import sys
import random
import time
from constants import *
from player import Player
from tile import Tile
from utils import load_tile_images
from door import Door
from enemy import Enemy

class Game:
    def __init__(self):
        print("Initializing py...")
        pygame.init()
        print("Creating time...")
        self.clock = pygame.time.Clock()

        print("Setting up display...")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        print("Setting font...")
        self.font = pygame.font.Font(None, 36)
        print("Initializing backgroud...")
        self.menu_background = pygame.image.load("menu_background.png")
        print("Initializing pause menu variables")
        self.paused = False
        self.pause_options = ["Resume", "Quit to Main Menu"]
        self.pause_selected_option = 0

        print("Loading tile images...")
        self.tile_images = load_tile_images(NUM_TILE_IMAGES, TILE_SIZE)
        print("Creating tile images...")
        self.tiles = self.create_tiles()
        print("Initialize the door...")
        self.door = Door(WIDTH - TILE_SIZE, HEIGHT // 2 - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
        self.door_open = False
        print("Initialize timer...")
        self.time_remaining = LEVEL_TIME_LIMIT

        print("Initializing vars ...")
        self.current_level = 1
        self.max_levels = 10
        self.background_x = 0
        self.state = "TITLE"
        print("Game state: TITLE")
        self.menu_options = ["Play", "Quit"]
        self.selected_option = 0

        print("Creating player object...")
        self.player = Player(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)
        
        print("Creating enemy object...")
        self.enemies = []
        self.num_enemies = 3
        
        print("Initializing items...")
        self.artifacts = []
        self.lore_items = []
        print("Initialize time power-up...")
        self.time_power = None # not using this...
        print("Initialize boss state...")
        self.boss_present = False # probably don't need this.

        print("Initialize the level...")
        self.initialize_level() # run this after everything else
        #input("Press Enter to continue...")

        print("Complete.")
        time.sleep(1)
        os.system('clear')


    def run(self):
        while True:
            if self.state == "TITLE":
                print("Loading title...")
                time.sleep(1)
                os.system('clear')
                self.show_title_screen()
            elif self.state == "MENU":
                print("Loading menu...")
                time.sleep(1)
                os.system('clear')
                self.show_menu()
            elif self.state == "GAME":
                print("Loading game...")
                time.sleep(1)
                os.system('clear')
                self.run_game()
            elif self.state == "GAME_OVER":
                print("Player lost...")
                time.sleep(1)
                os.system('clear')
                self.show_game_over()
            else:
                print("Error: game state not recognized")
                time.sleep(1)
                os.system('clear')
                break  

    def run_game(self):
        while self.current_level <= self.max_levels and self.state == "GAME":
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()
            self.clock.tick(60)
        if self.state == "GAME":
            self.show_ending()
        elif self.state == "GAME_OVER":
            self.show_game_over()

    def show_title_screen(self):
        self.screen.fill((0, 0, 0))
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Temporal Labyrinth", True, (255, 255, 255))
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(2)  # Display for 2 seconds
        self.state = "MENU"

    def show_menu(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.menu_background, (0, 0))

            title_font = pygame.font.Font(None, 72)
            option_font = pygame.font.Font(None, 36)

            title_text = title_font.render("Temporal Labyrinth", True, (255, 255, 255))
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

            for i, option in enumerate(self.menu_options):
                color = (255, 255, 255) if i == self.selected_option else (128, 128, 128)
                option_text = option_font.render(option, True, color)
                self.screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, 300 + i * 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Play
                            self.state = "GAME"
                            running = False
                        elif self.selected_option == 1:
                            print("Quiting...")
                            time.sleep(1)
                            os.system('clear')
                            pygame.quit()
                            sys.exit()

    def show_pause_menu(self):
        pause_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
        pause_surface.fill((0, 0, 0, 128))
        option_font = pygame.font.Font(None, 24)

        for i, option in enumerate(self.pause_options):
            color = (255, 255, 255) if i == self.pause_selected_option else (128, 128, 128)
            option_text = option_font.render(option, True, color)
            pause_surface.blit(option_text, (100 - option_text.get_width() // 2, 20 + i * 30))

        self.screen.blit(pause_surface, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Paused.")
                    self.paused = not self.paused
                    self.pause_selected_option = 0
                elif self.paused:
                    if event.key == pygame.K_UP:
                        self.pause_selected_option = (self.pause_selected_option - 1) % len(self.pause_options)
                    elif event.key == pygame.K_DOWN:
                        self.pause_selected_option = (self.pause_selected_option + 1) % len(self.pause_options)
                    elif event.key == pygame.K_RETURN:
                        if self.pause_selected_option == 0:
                            self.paused = False
                            os.system('clear') # clears pause msg
                        elif self.pause_selected_option == 1:
                            self.state = "TITLE"
                            self.paused = False
                            print("Quiting...")
                            time.sleep(1)
                            os.system('clear')
                            return
                else:
                    if event.key == pygame.K_RETURN:
                        self.check_tile_interaction()
                    elif event.key == pygame.K_SPACE:
                        self.use_time_power()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                self.check_tile_click(event.pos)

    def place_enemies(self):
        self.enemies = []
        for _ in range(self.num_enemies):
            x = random.randint(0, WIDTH - ENEMY_SIZE)
            y = random.randint(0, HEIGHT - ENEMY_SIZE)
            enemy = Enemy(x, y, ENEMY_SIZE, ENEMY_SIZE)
            self.enemies.append(enemy)

    def initialize_level(self):
        self.tiles = self.create_tiles()
        self.place_artifact()
        self.place_lore_items()
        self.set_time_power()
        self.check_boss_appearance()
        self.door_open = False  # Reset door state for the new level
        # Reset the timer
        self.time_remaining = LEVEL_TIME_LIMIT
        self.place_enemies()

    def create_tiles(self):
        tiles = []
        for x in range(0, LEVEL_WIDTH, TILE_SIZE):
            for y in range(0, HEIGHT, TILE_SIZE):
                image = random.choice(self.tile_images)
                tiles.append(Tile(x, y, TILE_SIZE, TILE_SIZE, image))
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

    def set_time_power(self):
        powers = [None, "Slow Time", "Rewind", "Time Stop"]
        self.time_power = powers[self.current_level // 3]

    def check_boss_appearance(self):
        self.boss_present = self.current_level in [5, 10]

    def check_tile_click(self, pos):
        for tile in self.tiles:
            if tile.rect.collidepoint(pos):
                self.interact_with_tile(tile)

    def interact_with_tile(self, tile):
        if tile.has_artifact:
            self.collect_artifact(tile)
        elif tile.has_lore:
            self.collect_lore(tile)
        tile.reveal()

    def collect_artifact(self, tile):
        print(f"Collected artifact from Level {self.current_level}")
        self.artifacts.append(f"Artifact from Level {self.current_level}")
        tile.has_artifact = False
        self.check_all_items_collected()

    def collect_lore(self, tile):
        print(f"Collected lore item from Level {self.current_level}")
        self.lore_items.append(f"Lore from Level {self.current_level}")
        tile.has_lore = False
        self.check_all_items_collected()

    def check_all_items_collected(self):
        if all(not tile.has_artifact and not tile.has_lore for tile in self.tiles):
            self.door_open = True

    def use_time_power(self):
        if self.time_power:
            print(f"Using time power: {self.time_power}")
            # Implement time power effect

    def advance_level(self):
        if self.current_level < self.max_levels:
            self.current_level += 1
            self.initialize_level()
            self.player.rect.topleft = (0, HEIGHT // 2 - PLAYER_SIZE // 2)  # Reset player position
        else:
            self.show_ending()

    def scroll_background(self):
        self.background_x -= SCROLL_SPEED
        if self.background_x < -LEVEL_WIDTH:
            self.background_x = 0
        if self.background_x > 0:
            self.background_x = 0
        elif self.background_x < -LEVEL_WIDTH + WIDTH:
            self.background_x = -LEVEL_WIDTH + WIDTH

    def handle_enemy_collision(self):
        # Implement what happens when the player collides with an enemy
        # For example, lose health, restart level, etc.
        print("Player collided with an enemy!")
        # For now, let's just move the player back to the start
        self.player.rect.topleft = (0, HEIGHT // 2 - PLAYER_SIZE // 2)


    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.scroll_background()
        if self.boss_present:
            self.update_boss()
        if self.door_open and self.player.rect.colliderect(self.door.rect):
            self.advance_level()
        for enemy in self.enemies:
            enemy.move()
            if self.player.rect.colliderect(enemy.rect):
                self.handle_enemy_collision()

        # Update the timer
        self.time_remaining -= 1 / 60  # Assuming 60 FPS
        if self.time_remaining <= 0:
            self.state = "GAME_OVER"

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
        if self.door_open:
            self.door.draw(self.screen)
        self.draw_ui()
        if self.paused:
            self.show_pause_menu()
        for enemy in self.enemies:
            enemy.draw(self.screen)
          
        pygame.display.flip()

    def draw_boss(self):
        # Draw the boss character
        pass

    def draw_ui(self):
        text = self.font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        if self.time_power:
            power_text = self.font.render(f"Power: {self.time_power}", True, (255, 255, 255))
            self.screen.blit(power_text, (10, 50))
        
        # Display the timer
        timer_text = self.font.render(f"Time: {int(self.time_remaining)}", True, (255, 255, 255))
        self.screen.blit(timer_text, (WIDTH - 150, 10))

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(2)  # Display for 2 seconds
        self.state = "MENU"

    def show_ending(self):
        print("Game Over - You've completed the Temporal Labyrinth!")
        print(f"Collected Artifacts: {len(self.artifacts)}")
        print(f"Lore Items Found: {len(self.lore_items)}")
        pygame.quit()
        sys.exit()