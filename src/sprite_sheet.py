import pygame
import json

class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.texture_file = pygame.image.load(filename + ".png").convert()
        self.data_file = json.load(open(filename + ".json"))

    def get_sprite(self, name):
        infos = self.data_file["frames"][name]["frame"]
        x, y, width, height = infos["x"], infos["y"], infos["w"], infos["h"]
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.set_colorkey((0, 0, 0))  #TODO Better color key?
        sprite.blit(self.texture_file, (0, 0), (x, y, width, height))
        return sprite