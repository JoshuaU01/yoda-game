import pygame

class Bullet:
    def __init__(self, pos_x, pos_y, direction, speed, image):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        self.speed = speed
        self.image = image

        self.hitbox = pygame.Rect(self.pos_x, self.pos_y, 16, 16)

    def move(self):
        if self.direction == 0:
            self.pos_x -= self.speed
        else:
            self.pos_x += self.speed

    def collide(self, sprites):
        hitboxes = [sprite.hitbox for sprite in sprites]  # Convert list of objects into list of their hitboxes
        if collided_hitboxes := [[i, hitboxes[i]] for i in self.hitbox.collidelistall(hitboxes)]:  # Check, if any object collides with the player
            for hitbox in collided_hitboxes:
                if sprites[hitbox[0]].take_damage:
                    sprites[hitbox[0]].health -= 1
            return True
        return False

    def update_hitbox(self):
        self.hitbox.update(self.pos_x, self.pos_y, 16, 16)
    def draw(self, screen, show_hitbox=False):
        screen.blit(self.image, (self.pos_x, self.pos_y))
        if show_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)