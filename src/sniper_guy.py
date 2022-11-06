import pygame

import enemy

class SniperGuy(enemy.Enemy):

    def __init__(self, pos_x, pos_y, width, height, speed, jump_speed, hitbox_width, hitbox_heigth, image):
        super(SniperGuy, self).__init__(pos_x, pos_y, width, height, speed, jump_speed, hitbox_width, hitbox_heigth, image)

    def shoot(self):
        pass

    def draw(self, screen, show_hitbox=False):
        screen.blit(self.image, (self.pos_x, self.pos_y))
        if show_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 5)