import pygame

def load_tile_images(num_images, tile_size):
    tile_images = []
    for i in range(num_images):
        image = pygame.image.load(f'/home/mcuser/game-test/tile_image{i}.png')
        image = pygame.transform.scale(image, (tile_size, tile_size))
        tile_images.append(image)
    return tile_images

"""
def load_tile_images(num_images, tile_size, theme):
    tile_images = []
    for i in range(num_images):
        if theme == "Ancient Egypt":
            image_path = f'/home/mcuser/game-test/egypt/tile_image{i}.png'
        elif theme == "Roman Empire":
            image_path = f'/home/mcuser/game-test/roman/tile_image{i}.png'
        elif theme == "Medieval Europe":
            image_path = f'/home/mcuser/game-test/medieval/tile_image{i}.png'
        elif theme == "Present Day":
            image_path = f'/home/mcuser/game-test/present/tile_image{i}.png'
        elif theme == "Distant Future":
            image_path = f'/home/mcuser/game-test/future/tile_image{i}.png'
        else:
            raise ValueError("Invalid theme")

        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (tile_size, tile_size))
        tile_images.append(image)
    return tile_images
"""