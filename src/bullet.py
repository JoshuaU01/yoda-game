import pygame

from object import Object
from world import World

from screen_dimensions import *

class Bullet(Object):
    def __init__(self, position, size, speed, direction):
        super().__init__()
        self.image = pygame.transform.scale(World.image_bullet, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.center = (position[0], position[1])
        self.velocity = pygame.math.Vector2(0, 0)

        self.speed = speed
        self.direction = direction
        self.TTL = 80

    def update(self):
        self.move()
        self.check_collisions()
        self.check_TTL()

    def move(self):
        self.velocity.x = self.speed * self.direction
        self.rect.x += self.velocity.x
        #self.rect.y += self.velocity.y #TODO work out self.dirction as vector 1x2?

    def check_collisions(self):
        collision_player = pygame.sprite.spritecollideany(self, World.players)
        collision_enemy = pygame.sprite.spritecollideany(self, World.enemies)
        collision_border = pygame.sprite.spritecollideany(self, World.borders)
        collision_block = pygame.sprite.spritecollideany(self, World.blocks)

        if collision_player or collision_enemy or collision_border or collision_block:
            # TODO apply to all instances which inherit from Character
            # TODO Implement that player can't hit themself
            if collision_player:
                collision_player.lose_lives(1)
            if collision_enemy:
                collision_enemy.lose_lives(1)
            self.kill()

    def check_TTL(self):
        self.TTL -= 1
        if self.TTL <= 0:
            self.kill()