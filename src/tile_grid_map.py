import pygame
import csv
import numpy as np

from world import World
from block import Block


class TileGridMap(pygame.sprite.Sprite):

    block_id_to_name = {
        0: "dirt_block_2_64.png",
        1: "grass_block_1_64.png",
    }

    def __init__(self, map_filename, sprite_sheet, grid_size):
        super().__init__()
        self.map_filename = map_filename
        self.sprite_sheet = sprite_sheet
        self.grid_size = grid_size

    def load_csv(self):
        with open(self.map_filename, newline='\n') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',')
            map_list = [row for row in filereader]
            print(map_list)
            if map_list:
                width = len(map_list)
                heigth = len(map_list[0])
                self.map = np.full((width, heigth), -1, dtype=np.int8)

                for vertical, row in enumerate(map_list):
                    for horizontal, cell in enumerate(row):
                        if str.isdigit(cell):  # TODO Also check if it fits in int8
                            self.map[vertical][horizontal] = int(cell)
                print(self.map[:5, :5])

    def render(self):
        for vertical, row in enumerate(self.map):
            for horizontal, cell in enumerate(row):
                if cell >= 0:
                    spritename = TileGridMap.block_id_to_name[cell]
                    sprite = self.sprite_sheet.get_sprite(spritename)
                    block = Block(
                        sprite, horizontal * self.grid_size, vertical * self.grid_size, self.grid_size, self.grid_size)
                    World.blocks.add(block)
                    World.all_sprites.add(block)
