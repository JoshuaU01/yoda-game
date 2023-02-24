import pygame

class Block:

    def __init__(self, pos, size, image=None): #TODO
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.width = size[0]
        self.height = size[1]
        self.hitbox = pygame.Rect(pos, size)

    def update_hitbox(self):
        self.hitbox.update(self.pos_x, self.pos_y, self.width, self.height)

    def draw(self, screen, draw_border=[0,0,0,0]):
        pygame.draw.rect(screen, (200,50,200), self.hitbox)