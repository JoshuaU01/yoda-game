import pygame

class Enemy:

    def __init__(self, image):
        self.hitbox = None #TODO
        self.image = image


    def draw(self, screen):
        screen.blit(self.image, (self.pos_x, self.pos_y))