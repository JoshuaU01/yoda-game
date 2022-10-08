import pygame

class Player:

    def __init__(self):
        self.pos_x = 300
        self.pos_y = 540
        self.width = 96
        self.height = 128
        self.speed = 5

        self.last_move = 1

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.pos_x -= self.speed
            self.last_move = 0
        if pressed[pygame.K_RIGHT]:
            self.pos_x += self.speed
            self.last_move = 1

    def draw_player(self, screen, image, image_reverse):
        if self.last_move == 0:
            screen.blit(image_reverse, (self.pos_x, self.pos_y))
        if self.last_move == 1:
            screen.blit(image, (self.pos_x, self.pos_y))