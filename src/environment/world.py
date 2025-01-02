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

    hitboxes_visible = False
    health_bars_visible = True

    players = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    borders = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    images = dict()

    boundaries = dict()

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
        image = pygame.image.load(image_path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image

    @staticmethod
    def load_images() -> None:
        """
        Loads in all the single images that are not part of a sprite sheet.
        """
        World.images["player"] = World.load_image("media/images/player/ziwomol/ziwomol_v3.png")
        World.images["stickman"] = World.load_image("media/images/template/stickman.png")
        World.images["runner"] = World.load_image("media/images/enemies/runner/runner_v2.png")
        World.images["background"] = World.load_image(
            "media/images/background/map_grass_background.png", size=(World.SCREEN_WIDTH, World.SCREEN_HEIGHT))
        World.images["floor"] = World.load_image(
            "media/images/background/map_grass_floor.png", size=(World.SCREEN_WIDTH, 180))
        World.images["bullet"] = World.load_image("media/images/bullet/bullet_small.png")
        World.images["full_heart"] = World.load_image("media/images/heart/full_heart.png", size=(16, 16))
        World.images["half_heart"] = World.load_image("media/images/heart/half_heart.png", size=(8, 16))

    @staticmethod
    def set_boundaries(left: int, right: int, top: int, bottom: int) -> None:
        """
        Sets the boundaries of the world. A character will die, if they leave them.

        :param left: Left boundary.
        :param right: Right boundary.
        :param top: Upper boundary.
        :param bottom: Lower boundary.
        """
        World.boundaries["left"] = left
        World.boundaries["right"] = right
        World.boundaries["top"] = top
        World.boundaries["bottom"] = bottom

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
