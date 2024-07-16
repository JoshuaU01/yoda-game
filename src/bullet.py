import pygame

from colors import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, velocity, direction, image):
        super().__init__()
        self.position = pygame.math.Vector2(position[0], position[1])
        self.velocity = pygame.math.Vector2(velocity[0], velocity[1])
        self.direction = direction
        self.image = image
        self.rect = self.image.get_rect()

        self.hitbox = pygame.Rect(self.position.x, self.position.y, 16, 16)

    def move(self):
        if self.direction == 0:
            self.position.x -= self.velocity.x
        else:
            self.position.x += self.velocity.x

    def collide(self, sprites):
        hitboxes = [sprite.hitbox for sprite in sprites]  # Convert list of objects into list of their hitboxes
        if collided_hitboxes := [[i, hitboxes[i]] for i in self.hitbox.collidelistall(hitboxes)]:  # Check, if any object collides with the player
            for hitbox in collided_hitboxes:
                if sprites[hitbox[0]].take_damage:
                    sprites[hitbox[0]].health -= 1
            return True
        return False

    def update_hitbox(self):
        self.hitbox.update(self.position.x, self.position.y, 16, 16)
    def draw(self, screen, show_hitbox=False):
        screen.blit(self.image, (self.position.x, self.position.y))
        if show_hitbox:
            pygame.draw.rect(screen, RED, self.hitbox, 2)