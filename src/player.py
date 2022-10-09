import pygame

class Player:

    def __init__(self):
        self.pos_x = 300
        self.pos_y = 540
        self.width = 96
        self.height = 128
        self.speed = 10
        self.jump_speed = 0

        self.jump_allowed = True
        self.last_move = 1

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.pos_x -= self.speed
            self.last_move = 0
        if pressed[pygame.K_RIGHT]:
            self.pos_x += self.speed
            self.last_move = 1

    def jump(self, gravity):
        pressed = pygame.key.get_pressed()
        if self.jump_allowed:
            if pressed[pygame.K_UP]:
                self.jump_allowed = False
                self.jump_speed = 10
        else:  # Player is jumping
            self.jump_speed -= 1  #TODO gravity / 10.0
            if self.jump_speed > -10:
                self.pos_y -= self.jump_speed * 4
            else:  # Collision or end of jump
                self.jump_allowed = True



    def draw(self, screen, image, image_reverse):
        if self.last_move == 0:
            screen.blit(image_reverse, (self.pos_x, self.pos_y))
        if self.last_move == 1:
            screen.blit(image, (self.pos_x, self.pos_y))