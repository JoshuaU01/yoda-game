import pygame

import enemy

class SniperGuy(enemy.Enemy):

    def __init__(self, image):
        super(SniperGuy, self).__init__(image)
        self.pos_x = 1200
        self.pos_y = 540
        self.width = 96
        self.height = 128

    def shoot(self):
        pass