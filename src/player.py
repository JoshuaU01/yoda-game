import pygame

from character import Character
from bullet import Bullet
from world import World

from colors import *
from directions import *

class Player(Character):

    def __init__(self, position, size, speed, image, lives=10):
        super().__init__(position, size, speed, image, lives)

        self.is_jumping = False
        self.gravity = 1.6
        self.jump_strength = 25
        self.on_ground = False

        self.direction = RIGHT
        self.jump_cooldown = 0

        self.take_damage = True
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0


    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.move_and_check_collisions()
        #self.bullets.update()
        self.apply_cooldown()
        self.check_alive()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = - self.speed
            if self.direction == RIGHT:
                self.image = pygame.transform.flip(self.image, True, False)
            self.direction = LEFT
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            if self.direction == LEFT:
                self.image = pygame.transform.flip(self.image, True, False)
            self.direction = RIGHT
        if keys[pygame.K_UP] and self.on_ground:
            self.jump()
        if keys[pygame.K_a]:
            self.shoot()

    def jump(self):
        self.velocity.y = -self.jump_strength
        self.is_jumping = True
        self.on_ground = False

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity.y += self.gravity

    def move_and_check_collisions(self):
        old_rect = self.rect.copy()

        # Check for collision in horizontal direction
        self.rect.x += self.velocity.x
        if pygame.sprite.spritecollideany(self, World.enemies) or pygame.sprite.spritecollideany(self, World.floors) or pygame.sprite.spritecollideany(self, World.blocks):
            self.rect.x = old_rect.x

        # Check for collision in vertical direction
        self.rect.y += self.velocity.y
        collision_enemy = pygame.sprite.spritecollideany(self, World.enemies)
        collision_floor = pygame.sprite.spritecollideany(self, World.floors)
        collision_block = pygame.sprite.spritecollideany(self, World.blocks)

        #TODO reduce code complexity
        if collision_enemy:
            if self.velocity.y > 0:
                self.rect.bottom = collision_enemy.rect.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = collision_enemy.rect.bottom
                self.velocity.y = 0
        elif collision_floor:
            self.rect.bottom = collision_floor.rect.top
            self.velocity.y = 0
            self.on_ground = True

            #self.rect.y = old_rect.y
            #self.on_ground = True
            #self.velocity.y = 0
            #if self.rect.bottom > collision_floor.rect.top:
            #    self.rect.bottom = collision_floor.rect.top
        elif collision_block:
            if self.velocity.y > 0:
                self.rect.bottom = collision_block.rect.top
                self.velocity.y = 0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = collision_block.rect.bottom
                self.velocity.y = 0
        else:
            self.on_ground = False

    def shoot(self):
        if self.cooldown <= 0:
            if len(self.bullets) < 5:
                bullet = Bullet((self.rect.x + self.rect.width * 0.5*(self.direction+1), self.rect.y + self.rect.height * (2/3)), (16, 16), 12, self.direction)
                self.bullets.add(bullet)
                World.all_sprites.add(bullet)
                self.cooldown = 8

    def apply_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, screen, show_hitbox=False):
        if self.direction == LEFT:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.rect.x, self.rect.y))
        if self.direction == RIGHT:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        if show_hitbox:
            pygame.draw.rect(screen, RED, self.rect, 5)