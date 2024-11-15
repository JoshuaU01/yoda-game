import pygame
import json


class SpriteSheet:
    """
    Contains an image of multiple sprites and metadata
    """

    def __init__(self, filename: str) -> None:
        """
        Creates an instance of this class.

        Args:
            filename (str): The relative path to the spritesheet file.
        """
        self.filename = filename
        self.texture_file = pygame.image.load(filename + ".png").convert_alpha()
        self.data_file = json.load(open(filename + ".json"))

    def get_sprite(self, name: str) -> pygame.Surface:
        """
        Retrieves an image of the specified sprite

        Args:
            name (str): The name of the wanted sprite.

        Returns:
            pygame.Surface: The image of the wanted sprite.
        """
        infos = self.data_file["frames"][name]["frame"]
        x, y, width, height = infos["x"], infos["y"], infos["w"], infos["h"]
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.texture_file, (0, 0), (x, y, width, height))
        return sprite
