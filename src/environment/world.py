from typing import Optional

import pygame


class World(pygame.sprite.Sprite):
    """
    A class for global variables and functions.
    """

    RUNNING = True
    FULLSCREEN = False

    SCREEN_WIDTH = 1440  # display_info.current_w
    SCREEN_HEIGHT = 800  # display_info.current_h

    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    borders = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    @staticmethod
    def load_image(image_path: str, size: Optional[tuple[int, int]] = None) -> pygame.Surface:
        """
        Loads an image from its relative path and returns it.

        Args:
            image_path (str): The relative path to the image file.
            size (Optional[tuple[int, int]]): If specified, the image will be resized to this size.

        Returns:
            pygame.Surface: The loaded image.
        """
        image = pygame.image.load(image_path)
        if size:
            image = pygame.transform.scale(image, size)
        return image

    image_player = load_image("media/images/player/ziwomol/ziwomol_v3.png")
    image_stickman = load_image("media/images/template/stickman.png")
    image_runner = load_image("media/images/enemies/runner/runner_v2.png")
    image_background = load_image(
        "media/images/background/map_grass_background.png", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    image_floor = load_image("media/images/background/map_grass_floor.png", size=(SCREEN_WIDTH, 180))
    image_bullet = load_image("media/images/bullet/bullet_small.png")
    image_full_heart = load_image("media/images/heart/full_heart.png", size=(16, 16))
    image_half_heart = load_image("media/images/heart/half_heart.png", size=(8, 16))

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """
        super().__init__()


class Colors:
    """
    This class contains the 8bit RGB representation of the colors used in the game.
    """

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    BROWN = (128, 128, 128)


class Directions:
    """
    This class contains the integer representation of the directions.
    """

    LEFT = -1
    RIGHT = 1
