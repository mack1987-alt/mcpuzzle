import pygame

def load_tile_images(num_images, tile_size):
    tile_images = []
    for i in range(num_images):
        image = pygame.image.load(f'/home/mcuser/game-test/level_resources/tile_image{i}.png')
        image = pygame.transform.scale(image, (tile_size, tile_size))
        tile_images.append(image)
    return tile_images
