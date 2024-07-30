import pygame

from screen_dimensions import *

class World(pygame.sprite.Sprite):

    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    borders = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    @staticmethod
    def load_image(image_path, size=None):
        image = pygame.image.load(image_path)
        if size:
            image = pygame.transform.scale(image, size)
        return image

    image_player = load_image("media/images/player/ziwomol/ziwomol_v3.png")
    image_enemy = load_image("media/images/template/stickman.png")
    image_background = load_image("media/images/background/map_grass_background.png", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    image_floor = load_image("media/images/background/map_grass_floor.png", size=(SCREEN_WIDTH, 180))
    image_bullet = load_image("media/images/bullet/bullet_small.png")

    def __init__(self, background, size, blocks, enemies, gravity=9.81):
        super().__init__()
