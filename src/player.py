import pygame

import bullet

class Player:

    def __init__(self, pos_x, pos_y, width, height, speed, jump_speed, hitbox_width, hitbox_heigth, image):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        self.jump_speed = jump_speed

        self.hitbox_width = hitbox_width
        self.hitbox_height = hitbox_heigth
        self.hitbox = pygame.Rect(self.pos_x, self.pos_y, self.hitbox_width, self.hitbox_height)
        self.bullets = []
        self.cooldown = 0

        self.movement_lock = [False, False, False, False]  # left, rigth, up, down
        self.jump_allowed = True
        self.jump_intended = False
        self.jump_released = True
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.last_move = 1

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] and not self.movement_lock[0]:
            self.pos_x -= self.speed
            self.last_move = 0
        if pressed[pygame.K_RIGHT] and not self.movement_lock[1]:
            self.pos_x += self.speed
            self.last_move = 1

    def jump(self, gravity: (int, float)):
        pressed = pygame.key.get_pressed()
        if self.jump_allowed:
            if pressed[pygame.K_SPACE]:
                self.jump_allowed = False
                self.jump_speed = 14
        else:  # Player is jumping
            self.jump_speed -= 1  #TODO gravity / 10.0
            if self.jump_speed > -14:
                self.pos_y -= self.jump_speed * 2
            else:  # Collision or end of jump
                self.jump_allowed = True

    def shoot(self):
        pressed = pygame.key.get_pressed()
        if self.cooldown <= 0:
            if pressed[pygame.K_a]:
                self.cooldown = 10
                if self.last_move == 0:
                    self.bullets.append(bullet.Bullet(self.pos_x - self.width / 20, self.pos_y + self.height * 0.65, self.last_move)) #TODO check and change values
                else:
                    self.bullets.append(bullet.Bullet(self.pos_x + self.width * 19/20, self.pos_y + self.height * 0.65, self.last_move)) #TODO check and change values
        else:
            self.cooldown -= 1


    def update_hitbox(self):
        self.hitbox.update(self.pos_x, self.pos_y, self.hitbox_width, self.hitbox_height)

    def draw(self, screen, show_hitbox=False):
        if self.last_move == 0:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.pos_x, self.pos_y))
        if self.last_move == 1:
            screen.blit(self.image, (self.pos_x, self.pos_y))
        if show_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 5)