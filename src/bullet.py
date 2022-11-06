import pygame

class Bullet:
    def __init__(self, pos_x, pos_y, direction):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        self.speed = 2  #TODO change to parameter

        self.image = pygame.image.load("media/images/bullet/bullet_small.png")
        #self.image = pygame.transform.scale(pygame.image.load("media/images/bullet/bullet.png"), (18, 18)) #TODO

    def move(self):
        if self.direction == 0:
            self.pos_x -= self.speed
        else:
            self.pos_x += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.pos_x, self.pos_y))