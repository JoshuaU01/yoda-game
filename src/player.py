import pygame

from character import Character
from bullet import Bullet

from colors import *
from movements import *

class Player(Character):

    def __init__(self, position, size, velocity, image):
        super().__init__(position, size, velocity, image)

        self.is_jumping = False
        self.gravity = 1.6
        self.jump_strength = 30
        self.on_ground = False

        self.last_move = RIGHT
        self.jump_cooldown = 0

        self.take_damage = True
        self.health = 10
        self.bullets = pygame.sprite.Group()
        self.cooldown = 0


    def update(self, enemies, floors, blocks, screen_height):
        self.handle_input()
        self.apply_gravity()
        self.move_and_check_collisions(enemies, floors, blocks)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -8
            self.last_move = LEFT
        if keys[pygame.K_RIGHT]:
            self.velocity.x = 8
            self.last_move = RIGHT
        if keys[pygame.K_UP] and self.on_ground:
            self.jump()

    def jump(self):
        self.velocity.y = -self.jump_strength
        self.is_jumping = True
        self.on_ground = False

    def apply_gravity(self):
        if not self.on_ground:
            self.velocity.y += self.gravity

    def move_and_check_collisions(self, enemies, floors, blocks):
        old_rect = self.rect.copy()

        # Check for collision in horizontal direction
        self.rect.x += self.velocity.x
        if pygame.sprite.spritecollideany(self, enemies) or pygame.sprite.spritecollideany(self, floors) or pygame.sprite.spritecollideany(self, blocks):
            self.rect.x = old_rect.x

        # Check for collision in vertical direction
        self.rect.y += self.velocity.y
        collision_enemy = pygame.sprite.spritecollideany(self, enemies)
        collision_floor = pygame.sprite.spritecollideany(self, floors)
        collision_block = pygame.sprite.spritecollideany(self, blocks)

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
            self.rect.y = old_rect.y
            self.on_ground = True
            self.velocity.y = 0
            if self.rect.bottom > collision_floor.rect.top:
                self.rect.bottom = collision_floor.rect.top
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

    def shoot(self, image_bullet):
        pressed = pygame.key.get_pressed()
        # Remove bullet, if out of display
        for b in self.bullets:
            if b.position.x <= -10 - 16 or b.position.x >= 1450:
                self.bullets.remove(b)

        if self.cooldown <= 0:
            if pressed[pygame.K_a]:
                if len(self.bullets) < 8:
                    self.cooldown = 15
                    if self.last_move == 0:
                        self.bullets.add(Bullet((self.position.x - self.size.x / 20, self.position.y + self.size.y * 0.65), (3, 0), self.last_move, image_bullet))
                    else:
                        self.bullets.add(Bullet((self.position.x + self.size.x * 19/20, self.position.y + self.size.y * 0.65), (3, 0), self.last_move, image_bullet))
        else:
            self.cooldown -= 1

    def die(self):
        if self.health <= 0:
            return True
        return False

    def draw(self, screen, show_hitbox=False):
        if self.last_move == LEFT:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.rect.x, self.rect.y))
        if self.last_move == RIGHT:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        if show_hitbox:
            pygame.draw.rect(screen, RED, self.rect, 5)