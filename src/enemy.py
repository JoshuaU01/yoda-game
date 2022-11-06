import pygame

class Enemy:

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
        self.image = image

    def update_hitbox(self):
        self.hitbox.update(self.pos_x, self.pos_y, self.hitbox_width, self.hitbox_height)

    def draw(self, screen):
        screen.blit(self.image, (self.pos_x, self.pos_y))