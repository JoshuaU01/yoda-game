import pygame

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

        self.movement_lock = [False, False, False, False]  # left, rigth, up, down
        self.jump_allowed = True
        self.image = image
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
                self.jump_speed = 12
        else:  # Player is jumping
            self.jump_speed -= 1  #TODO gravity / 10.0
            if self.jump_speed > -12:
                self.pos_y -= self.jump_speed * 3
            else:  # Collision or end of jump
                self.jump_allowed = True

    def update_hitbox(self):
        self.hitbox.update(self.pos_x, self.pos_y, self.hitbox_width, self.hitbox_height)

    def draw(self, screen, show_hitbox=False):
        if self.last_move == 0:
            screen.blit(pygame.transform.flip(self.image, True, False), (self.pos_x, self.pos_y))
        if self.last_move == 1:
            screen.blit(self.image, (self.pos_x, self.pos_y))
        if show_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 5)