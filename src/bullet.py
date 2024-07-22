import pygame

from world import World

from screen_dimensions import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, size, speed, direction):
        super().__init__()
        self.image = pygame.transform.scale(World.image_bullet, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1])
        self.velocity = pygame.math.Vector2(0, 0)

        self.speed = speed
        self.direction = direction

    def update(self):
        self.move()
        self.check_collisions()
        self.check_boundaries()

    def move(self):
        self.velocity.x = self.speed * self.direction
        self.rect.x += self.velocity.x
        #self.rect.y += self.velocity.y #TODO work out self.dirction as vector 1x2?

    def check_collisions(self):
        collision_enemy = pygame.sprite.spritecollideany(self, World.enemies)
        collision_floor = pygame.sprite.spritecollideany(self, World.floors)
        collision_block = pygame.sprite.spritecollideany(self, World.blocks)

        if collision_enemy or collision_floor or collision_block:
            if collision_enemy:  #TODO apply to all instances which inherit from Character
                collision_enemy.lose_lives(1)
            self.kill()

    def check_boundaries(self):
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()