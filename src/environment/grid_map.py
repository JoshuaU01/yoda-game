from typing import Optional

import pygame
import csv
import numpy as np

from src.environment.world import World
from src.assets.objects.block import Block
from src.environment.sprite_sheet import SpriteSheet


class GridMap(pygame.sprite.Sprite):
    """
    A 2D map that is made up of rectangular tiles.
    """

    block_id_to_name = {
        0: "dirt_block_01.png",
        1: "dirt_block_02.png",
        2: "dirt_block_03.png",
        3: "dirt_block_04.png",
        4: "grass_block_01.png",
        5: "grass_block_02.png",
        6: "grass_block_03.png",
        7: "grass_block_04.png",
        8: "grass_block_05.png",
        9: "grass_block_06.png",
        10: "grass_block_07.png",
        11: "grass_block_08.png",
    }

    def __init__(self, map_filename: str, sprite_sheet: SpriteSheet, grid_size: int) -> None:
        """
        Creates an instance of this class.

        Args:
            map_filename (str): The relative path to the map file.
            sprite_sheet (SpriteSheet): The sprite sheet used for the map build.
            grid_size (int): The size of the tiles that the map is made of.
        """
        super().__init__()
        self.map_filename = map_filename + ".csv"
        self.sprite_sheet = sprite_sheet
        self.grid_size = grid_size
        self.map = None
        self.blocks = []

    def load_csv(self) -> Optional[np.ndarray]:
        """
        Loads in the information from the map file and organizes it into a numpy array.

        Returns:
            Optional[np.ndarray]: A 2D numpy array containing the map information as integers.
        """
        with open(self.map_filename, newline='\n') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',')
            map_list = [row for row in filereader]

            if map_list:
                width = len(map_list)
                heigth = len(map_list[0])
                self.map = np.full((width, heigth), -1, dtype=np.int8)

                for vertical, row in enumerate(map_list):
                    for horizontal, cell in enumerate(row):
                        if str.isdigit(cell):  # TODO Also check if it fits in int8
                            self.map[vertical, horizontal] = int(cell)
        return self.map

    def build(self) -> list[Block]:
        """
        Builds the map with blocks.

        Returns:
            list[Block]: All blocks that have been created for this map in a list.
        """
        for vertical, row in enumerate(self.map):
            for horizontal, cell in enumerate(row):
                if cell >= 0:  # For any sprite that is not air
                    spritename = GridMap.block_id_to_name[cell]
                    sprite = self.sprite_sheet.get_sprite(spritename)
                    block = Block(
                        sprite, horizontal * self.grid_size, vertical * self.grid_size, self.grid_size, self.grid_size)
                    self.blocks.append(block)
        return self.blocks

    def render(self) -> None:
        """
        Prepares the map blocks for the screen by adding them to the sprite groups.
        """
        World.all_sprites.add(*self.blocks)
        World.blocks.add(*self.blocks)
