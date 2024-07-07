import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
SCROLL_SPEED = 2
LEVEL_WIDTH = WIDTH * 2  # Each level is twice the screen width

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the player
player = pygame.Rect(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)

# Set up the background
background = pygame.Surface((LEVEL_WIDTH, HEIGHT))
background.fill((0, 0, 0))  # Fill the background with black
background_x = 0

# Set up the current level
current_level = 1

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    # Move the player
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED

    # Ensure the player doesn't move off the screen
    if player.x < 0:
        # Check if the player has reached the left edge of the screen
        if current_level > 1:
            current_level -= 1
            background_x = -LEVEL_WIDTH + WIDTH
            player.x = WIDTH - PLAYER_SIZE  # Reset the player's position to the right edge
    elif player.x > WIDTH - PLAYER_SIZE:
        # Check if the player has reached the right edge of the screen
        current_level += 1
        background_x = 0
        player.x = 0  # Reset the player's position to the left edge

    # Scroll the background
    background_x -= SCROLL_SPEED
    if background_x < -LEVEL_WIDTH:
        background_x = 0

    # Adjust the background scroll position to keep the player visible
    if background_x > 0:
        background_x = 0
    elif background_x < -LEVEL_WIDTH + WIDTH:
        background_x = -LEVEL_WIDTH + WIDTH

    # Draw everything
    screen.blit(background, (background_x, 0))
    pygame.draw.rect(screen, (255, 255, 255), player)

    # Display the current level
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {current_level}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(1000 // 60)