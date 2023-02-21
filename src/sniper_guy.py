import pygame

import enemy

class SniperGuy(enemy.Enemy):

    def __init__(self, pos_x, pos_y, width, height, speed, jump_speed, hitbox_width, hitbox_heigth, image):
        super(SniperGuy, self).__init__(pos_x, pos_y, width, height, speed, jump_speed, hitbox_width, hitbox_heigth, image)

    def shoot(self):
        pass