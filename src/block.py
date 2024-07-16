import pygame

from colors import *

class Block(pygame.sprite.Sprite):

    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #self.take_damage = False

    #def update_hitbox(self):
        #self.hitbox.update(self.pos_x, self.pos_y, self.width, self.height)

    #def draw(self, screen, draw_border=[0,0,0,0]):
        #pygame.draw.rect(screen, (200,50,200), self.hitbox)