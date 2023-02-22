import pygame

import bullet

class Player():

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
        if self.movement_lock[3]:
            self.jump_allowed = True
            self.jump_speed = 0
        if self.jump_allowed:
            if pressed[pygame.K_SPACE]:
                self.jump_allowed = False
                self.jump_speed = 20
        else:  # Player is jumping
            self.jump_speed -= 1  #TODO gravity / 10.0
            if self.jump_speed > -20:
                self.pos_y -= self.jump_speed * 1.8
            else:  # Collision or end of jump
                self.jump_allowed = True

    def fall(self):
        if not self.movement_lock[3] and self.jump_allowed and self.pos_y <= 530:
            self.jump_speed -= 1
            self.pos_y -= self.jump_speed * 1.8


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

    def collide(self, sprites):
        hitboxes = [sprite.hitbox for sprite in sprites]  # Convert list of objects into list of their hitboxes
        self.movement_lock = [False, False, False, False]  # Assume all collisions as False before checking
        if collided_hitboxes := [hitboxes[i] for i in self.hitbox.collidelistall(hitboxes)]:  # Check, if any object collides with the player
            for hitbox in collided_hitboxes:  # Check collision for every object
                # Check collision on left side
                if hitbox.right - self.speed <= self.hitbox.left <= hitbox.right:
                    self.movement_lock[0] += 1
                    self.pos_x = hitbox.right

                # Check for collision on right side
                if hitbox.left + self.speed >= self.hitbox.right >= hitbox.left:
                    self.movement_lock[1] += 1
                    self.pos_x = hitbox.left - self.width

                # Check for collision on upper side
                if hitbox.bottom - 40 <= self.hitbox.top <= hitbox.bottom:
                    self.jump_speed = 0
                    self.pos_y = hitbox.bottom

                # Check for collision on lower side
                if hitbox.top + 40 >= self.hitbox.bottom >= hitbox.top:
                    self.movement_lock[3] += 1
                    self.pos_y = hitbox.top - self.height

    def update_hitbox(self):
        self.hitbox.update(self.pos_x, self.pos_y, self.hitbox_width, self.hitbox_height)

    def draw(self, screen, show_hitbox=False):
        if self.last_move == 0:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.pos_x, self.pos_y))
        if self.last_move == 1:
            screen.blit(self.image, (self.pos_x, self.pos_y))
        if show_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 5)