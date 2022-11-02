import pygame

import enemy

class SniperGuy(enemy.Enemy):

    def __init__(self, image):
        super(SniperGuy, self).__init__(image)
        self.pos_x = 1200
        self.pos_y = 540
        self.width = 96
        self.height = 128

        self.lock = False
        self.hitbox = pygame.Rect(self.pos_x, self.pos_y, 140, 260)

    def shoot(self):
        pass

    def update_hitbox(self):
        self.hitbox.update(self.pos_x, self.pos_y, 140, 260)

    def draw(self, screen, show_hitbox=False):
        screen.blit(self.image, (self.pos_x, self.pos_y))
        if show_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 5)